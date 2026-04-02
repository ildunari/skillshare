# Standard MCP server reference

Complete patterns for building a standard (non-App) MCP server with Streamable HTTP transport.

## Table of contents

- Package.json and dependencies
- Server factory pattern
- Main entry point with Express
- Tool registration with Zod
- structuredContent for rich responses
- Tool annotations
- Error handling
- Pagination
- Authentication patterns
- Stdio transport (local servers)

---

## Package.json

```json
{
  "name": "my-mcp-server",
  "private": true,
  "type": "module",
  "scripts": {
    "build": "tsc",
    "serve": "tsx main.ts",
    "dev": "tsx watch main.ts"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.26.0",
    "express": "^4.21.0",
    "cors": "^2.8.5",
    "zod": "^3.24.0"
  },
  "devDependencies": {
    "typescript": "^5.7.0",
    "tsx": "^4.19.0",
    "@types/express": "^5.0.0",
    "@types/cors": "^2.8.0",
    "@types/node": "^22.0.0"
  }
}
```

## tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist"
  },
  "include": ["*.ts"]
}
```

---

## Server factory pattern

Every Streamable HTTP server MUST use a factory function. Creating a single shared `McpServer` instance causes state collisions when multiple clients connect concurrently.

```typescript
// server.ts
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

export function createServer(): McpServer {
  const server = new McpServer({
    name: "My MCP Server",
    version: "1.0.0",
  });

  // --- Register tools ---

  server.tool(
    "search_items",
    {
      description: "Search for items by keyword",
      inputSchema: {
        query: z.string().describe("Search query"),
        limit: z.number().min(1).max(100).default(10).describe("Max results"),
      },
      annotations: {
        readOnlyHint: true,
        destructiveHint: false,
        idempotentHint: true,
        openWorldHint: true,
      },
    },
    async ({ query, limit }) => {
      const results = await searchItems(query, limit);

      return {
        content: [
          { type: "text", text: `Found ${results.length} items for "${query}"` },
        ],
        structuredContent: {
          query,
          results,
          total: results.length,
        },
      };
    }
  );

  return server;
}
```

---

## Main entry point

```typescript
// main.ts
import { createMcpExpressApp } from "@modelcontextprotocol/sdk/server/express.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import cors from "cors";
import type { Request, Response } from "express";
import { createServer } from "./server.js";

const port = parseInt(process.env.PORT ?? "3001", 10);

const app = createMcpExpressApp({ host: "0.0.0.0" });
app.use(cors());

app.all("/mcp", async (req: Request, res: Response) => {
  const server = createServer();
  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: undefined, // Stateless mode
  });

  res.on("close", () => {
    transport.close().catch(() => {});
    server.close().catch(() => {});
  });

  try {
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
  } catch (error) {
    console.error("MCP error:", error);
    if (!res.headersSent) {
      res.status(500).json({
        jsonrpc: "2.0",
        error: { code: -32603, message: "Internal server error" },
        id: null,
      });
    }
  }
});

const httpServer = app.listen(port, () => {
  console.log(`MCP server listening on http://localhost:${port}/mcp`);
});

// Graceful shutdown
const shutdown = () => {
  console.log("\nShutting down...");
  httpServer.close(() => process.exit(0));
};
process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);
```

---

## Tool registration patterns

### Basic tool with Zod schema

```typescript
server.tool(
  "get_user",
  {
    description: "Retrieve a user by ID",
    inputSchema: {
      userId: z.string().describe("The user's unique identifier"),
    },
    annotations: { readOnlyHint: true },
  },
  async ({ userId }) => {
    const user = await fetchUser(userId);
    if (!user) {
      return {
        isError: true,
        content: [{ type: "text", text: `User ${userId} not found. Check the ID and try again.` }],
      };
    }
    return {
      content: [{ type: "text", text: `User: ${user.name} (${user.email})` }],
      structuredContent: user,
    };
  }
);
```

### Tool with pagination

```typescript
server.tool(
  "list_items",
  {
    description: "List items with pagination. Returns up to `limit` items starting from `cursor`.",
    inputSchema: {
      cursor: z.string().optional().describe("Pagination cursor from previous response"),
      limit: z.number().min(1).max(50).default(20),
    },
    annotations: { readOnlyHint: true },
  },
  async ({ cursor, limit }) => {
    const { items, nextCursor } = await getItems(cursor, limit);

    return {
      content: [
        { type: "text", text: `Returned ${items.length} items${nextCursor ? ". More available." : "."}` },
      ],
      structuredContent: {
        items,
        nextCursor: nextCursor ?? null,
        hasMore: !!nextCursor,
      },
    };
  }
);
```

### Destructive tool with confirmation pattern

```typescript
server.tool(
  "delete_item",
  {
    description: "Permanently delete an item. This cannot be undone.",
    inputSchema: {
      itemId: z.string(),
      confirm: z.literal(true).describe("Must be true to confirm deletion"),
    },
    annotations: {
      readOnlyHint: false,
      destructiveHint: true,
      idempotentHint: true,
    },
  },
  async ({ itemId, confirm }) => {
    await deleteItem(itemId);
    return {
      content: [{ type: "text", text: `Deleted item ${itemId}.` }],
    };
  }
);
```

---

## Error handling

Return actionable errors that guide the model toward a fix:

```typescript
// Bad: vague error
return { isError: true, content: [{ type: "text", text: "Request failed" }] };

// Good: actionable error
return {
  isError: true,
  content: [{
    type: "text",
    text: `API returned 403 Forbidden for endpoint /users/${userId}. The API key may lack read permissions. Check that the MYSERVICE_API_KEY environment variable has the "users:read" scope.`
  }],
};
```

---

## Stdio transport (local servers)

For Claude Desktop or local-only usage, use stdio instead of HTTP:

```typescript
// main.ts (stdio variant)
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { createServer } from "./server.js";

async function main() {
  const server = createServer();
  await server.connect(new StdioServerTransport());
}

main().catch((e) => { console.error(e); process.exit(1); });
```

Configure in `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "npx",
      "args": ["tsx", "/absolute/path/to/main.ts"],
      "env": {
        "MY_API_KEY": "..."
      }
    }
  }
}
```

Always use absolute paths — Claude Desktop's working directory is undefined on macOS.

---

## Authentication patterns

### API key via environment variable

```typescript
const API_KEY = process.env.MY_SERVICE_API_KEY;
if (!API_KEY) {
  console.error("MY_SERVICE_API_KEY environment variable is required");
  process.exit(1);
}

// Use in tool handlers
async function callApi(endpoint: string) {
  return fetch(`https://api.example.com${endpoint}`, {
    headers: { Authorization: `Bearer ${API_KEY}` },
  });
}
```

### OAuth for Claude.ai connectors

Claude.ai supports OAuth for connectors. Your server implements the standard OAuth 2.0 flow. The connector configuration in Claude Settings accepts client ID and secret. See Claude's connector docs for the full flow.

---

## Response formatting

Prefer structured data in `structuredContent` and concise summaries in `content`:

```typescript
// The model sees this (content):
content: [{ type: "text", text: "Found 3 open issues labeled 'bug'" }]

// Clients that support it also get this (structuredContent):
structuredContent: {
  issues: [
    { id: 42, title: "Login fails on Safari", labels: ["bug"], state: "open" },
    { id: 57, title: "CSV export truncated", labels: ["bug"], state: "open" },
    { id: 63, title: "Dark mode contrast", labels: ["bug", "a11y"], state: "open" },
  ],
  query: { labels: ["bug"], state: "open" },
  total: 3,
}
```

This gives the model enough text to reason about the results while giving structured clients (including MCP App Views) typed access to the data.
