# Electron App → CLI Conversion Prompts

Individual prompts for converting each Electron app on this system into a programmable CLI.
Each prompt is self-contained and references `[skill:electron-to-cli]` and `[skill:agent-browser]`
for the methodology, plus `[skill:discord]` as the reference implementation.

---

## Inventory

### All Electron Apps (sorted by recent usage)

| App | Version | Location | Last Used | Priority |
|-----|---------|----------|-----------|----------|
| Codex (OpenAI) | 26.318.11754 | /Applications/AI/ | Today | High |
| Discord | 0.0.381 | /Applications/AI/ | Today | Done (CLI built) |
| 1Password | 8.12.8 | /Applications/ | Today | High |
| Obsidian | 1.11.7 | /Applications/ | Today | High |
| Claude | 1.1.7714 | /Applications/AI/ | Today | Medium |
| Craft Agents | 0.7.10 | /Applications/AI/ | Today | Skip (it's us) |
| Cursor | 2.6.19 | /Applications/AI/ | Today | Medium |
| VS Code | 1.110.1 | /Applications/AI/ | Today | Medium |
| Factory | 0.31.0 | /Applications/AI/ | 2 days ago | Low |
| Google Antigravity | 1.19.6 | /Applications/AI/ | 3 days ago | Low |
| Pencil | 1.1.33 | /Applications/AI/ | 3 days ago | Low |
| Upscayl | 2.15.0 | /Applications/AI/ | 11 days ago | Low |
| Termius | 9.37.2 | /Applications/ | 3 weeks ago | Low |
| Superset | 1.1.2 | /Applications/AI/ | Never | Skip |
| Maestro | 0.15.2 | /Applications/ | Never | Skip |

### Non-Electron Apps Worth CLI Wrapping

| App | Type | Location | Notes |
|-----|------|----------|-------|
| Telegram | Native macOS | /Applications/ | No CDP — use Bot API or tdlib |
| ChatGPT | Native (Swift) | /Applications/AI/ | No CDP — use OpenAI API |
| Craft | Native (Swift) | /Applications/AI/ | Has MCP source already |

---

## Priority 1: Codex (OpenAI)

```
Use [skill:electron-to-cli] and [skill:agent-browser] to convert the OpenAI Codex app into
a programmable CLI tool. Reference [skill:discord] as the working example of this methodology.

### Context
- App: /Applications/AI/Codex.app (Electron, v26.318.11754)
- This is OpenAI's Codex CLI/agent desktop app
- The user uses it daily

### Phase 1: Reconnaissance

1. Quit and relaunch with CDP on port 9231:
   osascript -e 'tell application "Codex" to quit'
   open -a "Codex" --args --remote-debugging-port=9231
   sleep 5

2. Use `agent-browser --cdp 9231` (NOT connect) to:
   - Snapshot the UI structure
   - Check for internal APIs: eval for window globals, native bridges, webpack modules
   - Check localStorage for auth tokens (use the iframe trick from the electron-to-cli skill)
   - Install the fetch interceptor pattern to capture Authorization headers
   - Probe for local servers (Codex may run a local API server)

3. Codex-specific things to check:
   - Does it use the OpenAI API directly? If so, the user's OpenAI API key may be
     accessible through the app's config or localStorage
   - Does it have a local task/session database?
   - What's the internal model selection mechanism?
   - Are there WebSocket connections for streaming?
   - Check ~/Library/Application Support/ for Codex data directories
   - Check if there's already a `codex` CLI binary bundled in the app

4. Test the OpenAI REST API with any discovered credentials:
   - GET https://api.openai.com/v1/models
   - GET https://api.openai.com/v1/assistants (if applicable)

### Phase 2: Architecture

Since Codex likely wraps the OpenAI API, the CLI should probably:
- Primary: OpenAI REST API via curl (fast, well-documented)
- Secondary: CDP for app-specific UI features

Expected commands:
```
codex tasks                    # List recent tasks/sessions
codex run "prompt"             # Run a new Codex task
codex status <task_id>         # Check task status
codex output <task_id>         # Get task output
codex models                   # List available models
codex config                   # Show current config
codex history                  # Task history
codex me                       # Account info
```

### Phase 3-4: Build CLI + Craft Agent Integration

Follow the standard template from [skill:electron-to-cli] Phase 3-4.
Install to /opt/homebrew/bin/codex-cli (avoid conflict with any existing codex binary).
Create source at sources/codex/ and skill at skills/codex/.
Use --json, --no-input, --limit flags matching discord/bird/gog patterns.
Token in macOS Keychain (service: codex-cli-token).
```

---

## Priority 2: 1Password

```
Use [skill:electron-to-cli] and [skill:agent-browser] to convert 1Password into a
programmable CLI tool. Reference [skill:discord] as the working example.

### Context
- App: /Applications/1Password.app (Electron, v8.12.8)
- The user uses it daily for password management
- 1Password ALREADY has an official CLI (`op`) — check if it's installed first!

### Phase 1: Reconnaissance

1. FIRST check if the 1Password CLI is already installed:
   which op && op --version
   If `op` exists, skip most of this and just create a Craft Agent source/skill wrapper.

2. If `op` is NOT installed:
   - Quit and relaunch with CDP on port 9232:
     osascript -e 'tell application "1Password" to quit'
     open -a "1Password" --args --remote-debugging-port=9232
   - Snapshot the UI
   - Check for internal APIs and auth mechanisms
   - 1Password uses a local agent socket — check for:
     ~/Library/Group Containers/*/1Password/t/agent.sock
     ~/.1password/agent.sock
   - Check for the 1Password Connect API or CLI

3. 1Password-specific considerations:
   - Security is paramount — NEVER log or cache master passwords or vault contents
   - The 1Password CLI uses biometric auth or service accounts
   - The desktop app communicates via a local socket, not REST
   - Check for browser extension communication channels

### Phase 2: Architecture

If `op` CLI exists:
- Create a thin wrapper skill that documents common `op` patterns
- Source + skill in Craft Agent, no need for a custom CLI

If `op` doesn't exist:
- Recommend installing it: `brew install 1password-cli`
- The Electron CDP approach is NOT recommended for password managers
  (security risk of token extraction, screen captures of sensitive data)
- A custom CLI around the 1Password Connect API is the safer alternative

Expected commands (wrapping `op`):
```
1pass items                    # List items (op item list)
1pass get <item>               # Get item details (op item get)
1pass search "query"           # Search vault
1pass totp <item>              # Get TOTP code
1pass vaults                   # List vaults
1pass signin                   # Sign in
```

### Phase 3-4: Build + Integrate

If wrapping `op`: create a Bash wrapper with friendlier names and --json output.
Install to /opt/homebrew/bin/1pass.
Create source at sources/1password/ and skill at skills/1password/.
CRITICAL: Never store vault contents, passwords, or secrets in the CLI output
unless --json is explicitly requested. Default to showing item names only.
```

---

## Priority 3: Obsidian

```
Use [skill:electron-to-cli] and [skill:agent-browser] to convert Obsidian into a
programmable CLI tool. Reference [skill:discord] as the working example.

### Context
- App: /Applications/Obsidian.app (Electron, v1.11.7)
- The user uses it daily for notes (vault at ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Brain/)
- Obsidian notes are plain markdown files — direct filesystem access is the primary path
- The user already accesses the vault via Read/Grep/Glob tools

### Phase 1: Reconnaissance

1. Since Obsidian notes are plain markdown, the FILESYSTEM is the primary API.
   No need for CDP in most cases. But explore what CDP adds:

2. Quit and relaunch with CDP on port 9233:
   osascript -e 'tell application "Obsidian" to quit'
   open -a "Obsidian" --args --remote-debugging-port=9233

3. Use agent-browser --cdp 9233 to:
   - Snapshot the UI (see which vault is open, current note, sidebar)
   - Check for Obsidian's internal API:
     - window.app (Obsidian's main API object)
     - window.app.vault (vault access)
     - window.app.workspace (workspace/pane management)
     - window.app.metadataCache (frontmatter, tags, links)
     - window.app.plugins (installed plugins)
   - Check for the Obsidian Local REST API plugin
     (community plugin that exposes HTTP API on localhost)

4. Obsidian-specific APIs to probe:
   - app.vault.getMarkdownFiles() — all notes
   - app.vault.read(file) — read a note
   - app.vault.modify(file, content) — write a note
   - app.metadataCache.getCache(path) — frontmatter, tags, links
   - app.workspace.getActiveFile() — current note
   - Check if Obsidian URI protocol is available: obsidian://

### Phase 2: Architecture

Hybrid approach:
- Primary: Direct filesystem (fast, no app dependency, works with vault synced via iCloud)
- Secondary: Obsidian internal API via CDP (for metadata, graph, workspace state)
- Tertiary: Obsidian URI scheme (for opening notes in the app)

Expected commands:
```
obsidian notes [--folder X]     # List notes (filesystem)
obsidian read <note>            # Read a note
obsidian write <note> "content" # Create/update note
obsidian search "query"         # Full-text search (grep)
obsidian tags                   # List all tags (metadata cache or frontmatter parse)
obsidian links <note>           # Show backlinks/forward links
obsidian recent [--limit N]     # Recently modified notes
obsidian today                  # Today's daily note
obsidian open <note>            # Open in Obsidian app (URI scheme)
obsidian graph                  # Graph stats (node count, connections)
obsidian plugins                # List installed plugins
obsidian screenshot [file]      # Screenshot Obsidian (CDP)
```

### Phase 3-4: Build + Integrate

The vault path is: ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Brain/
Build a Bash CLI that primarily uses filesystem operations (find, grep, cat).
For metadata operations, fall back to CDP eval on Obsidian's window.app API.
Install to /opt/homebrew/bin/obsidian-cli (avoid conflict with the obsidian URI handler).
Create source at sources/obsidian-cli/ and skill at skills/obsidian-cli/.
Support --json, --no-input, --limit flags.
```

---

## Priority 4: Claude Desktop

```
Use [skill:electron-to-cli] and [skill:agent-browser] to convert the Claude Desktop app
into a programmable CLI tool. Reference [skill:discord] as the working example.

### Context
- App: /Applications/AI/Claude.app (Electron, v1.1.7714)
- This is Anthropic's official Claude desktop app
- The user already has Claude Code CLI — this is about the desktop app specifically
- The Claude desktop app has MCP server support built in

### Phase 1: Reconnaissance

1. Quit and relaunch with CDP on port 9234:
   osascript -e 'tell application "Claude" to quit'
   open -a "Claude" --args --remote-debugging-port=9234

2. Use agent-browser --cdp 9234 to:
   - Snapshot the UI (conversations list, current conversation)
   - Check window globals and internal APIs
   - Check for conversation storage (likely SQLite in ~/Library/Application Support/Claude/)
   - Probe localStorage for auth tokens
   - Install fetch interceptor to capture the Anthropic API token

3. Claude-specific things to check:
   - Does the app use api.anthropic.com or a different endpoint?
   - What's the conversation storage format? (SQLite? JSON files?)
   - Can we access conversation history programmatically?
   - Are MCP server configs accessible?
   - Check ~/Library/Application Support/Claude/ for databases and config
   - Is there a claude.ai session cookie we can reuse?

4. Important: The user already has the `claude` CLI (Claude Code). This CLI should
   focus on desktop-app-specific features:
   - Conversation history browsing
   - Conversation export
   - MCP server management
   - Project management
   - Artifact extraction

### Phase 2: Architecture

- Primary: SQLite/filesystem for conversation history (fast offline access)
- Secondary: Anthropic API for new conversations (if API key available)
- Tertiary: CDP for app-specific UI (opening conversations, screenshots)

Expected commands:
```
claude-app conversations        # List conversations
claude-app read <conv_id>       # Read a conversation
claude-app export <conv_id>     # Export conversation as markdown
claude-app search "query"       # Search conversations
claude-app projects             # List projects
claude-app mcps                 # List configured MCP servers
claude-app artifacts <conv_id>  # Extract artifacts from conversation
claude-app open <conv_id>       # Open in Claude app (CDP)
claude-app screenshot [file]    # Screenshot (CDP)
```

### Phase 3-4: Build + Integrate

Install to /opt/homebrew/bin/claude-app (avoid conflict with claude CLI).
Create source at sources/claude-app/ and skill at skills/claude-app/.
Focus on what Claude Code CANNOT do — conversation history, artifact management,
project browsing, MCP config management.
```

---

## Priority 5: Cursor

```
Use [skill:electron-to-cli] and [skill:agent-browser] to convert Cursor into a
programmable CLI tool. Reference [skill:discord] as the working example.

### Context
- App: /Applications/AI/Cursor.app (Electron, v2.6.19)
- Cursor is a VS Code fork with AI features
- The user uses it regularly as a code editor
- Cursor may already have a CLI (`cursor` command)

### Phase 1: Reconnaissance

1. FIRST check if Cursor has a CLI already:
   which cursor && cursor --version
   Check if Cursor installs a shell command like VS Code does.

2. Quit and relaunch with CDP on port 9235:
   osascript -e 'tell application "Cursor" to quit'
   open -a "Cursor" --args --remote-debugging-port=9235

3. Use agent-browser --cdp 9235 to:
   - Snapshot the UI
   - Check for internal APIs (Cursor extends VS Code's API)
   - Check for Cursor-specific AI features accessible via API
   - Look for conversation/chat history storage
   - Check ~/Library/Application Support/Cursor/ for databases

4. Cursor-specific things to check:
   - AI chat history (where is it stored?)
   - Cursor rules (.cursorrules files)
   - Model selection and API key configuration
   - Composer history
   - Tab completion/prediction settings

### Phase 2: Architecture

Cursor is primarily a code editor — a CLI wrapper should focus on
the AI-specific features that differentiate it from VS Code:

Expected commands:
```
cursor-ai chats                 # List AI chat sessions
cursor-ai chat <id>             # Read a chat session
cursor-ai composers             # List composer sessions
cursor-ai rules                 # List/show cursor rules
cursor-ai models                # List configured models
cursor-ai config                # Show AI configuration
cursor-ai history               # Recent AI interactions
cursor-ai open <file>           # Open file in Cursor
cursor-ai project <dir>         # Open project in Cursor
```

### Phase 3-4: Build + Integrate

Install to /opt/homebrew/bin/cursor-ai.
Create source at sources/cursor/ and skill at skills/cursor/.
Focus exclusively on AI features — don't duplicate VS Code CLI functionality.
```

---

## Priority 6: VS Code

```
Use [skill:electron-to-cli] and [skill:agent-browser] to convert VS Code into a
programmable CLI tool. Reference [skill:discord] as the working example.

### Context
- App: /Applications/AI/Visual Studio Code.app (Electron, v1.110.1)
- VS Code already has the `code` CLI — check if installed
- The user uses it regularly

### Phase 1: Reconnaissance

1. Check existing CLI:
   which code && code --version
   VS Code almost certainly has `code` CLI already installed.

2. If `code` exists, focus on what it DOESN'T cover:
   - Extension management beyond install/uninstall
   - Workspace/project history
   - Settings search and modification
   - Recent files list
   - Git integration status across workspaces

3. If deeper access needed, relaunch with CDP on port 9236:
   open -a "Visual Studio Code" --args --remote-debugging-port=9236

   Check for:
   - vscode.workspace API via CDP
   - Extension API access
   - Settings storage (~/Library/Application Support/Code/)

### Phase 2: Architecture

Since `code` CLI exists, create a complementary wrapper:

Expected commands:
```
vsc recent                      # Recently opened files/workspaces
vsc extensions [--json]         # List extensions with details
vsc settings "search_term"     # Search settings
vsc set <key> <value>          # Change a setting
vsc workspaces                  # List recent workspaces
vsc snippets                    # List user snippets
vsc keybindings "search"       # Search keybindings
vsc open <file_or_dir>         # Open in VS Code (wraps `code`)
```

### Phase 3-4: Build + Integrate

Install to /opt/homebrew/bin/vsc.
Create source at sources/vscode/ and skill at skills/vscode/.
This is a complementary tool — use `code` CLI where it already works,
add value where it doesn't.
```

---

## Telegram (Native — NOT Electron)

```
Use [skill:electron-to-cli] methodology adapted for a native macOS app.
Also reference [skill:agent-browser] and [skill:discord] as examples.

### Context
- App: /Applications/Telegram.app (NATIVE macOS, NOT Electron)
- This means NO CDP access — cannot use --remote-debugging-port
- Telegram Desktop is built with Qt/native frameworks
- The user has a phone workspace at ~/.craft-agent-phone/ that may use Telegram

### Phase 1: Reconnaissance (Adapted for Native App)

Since Telegram is not Electron, CDP is not available. Alternative recon:

1. Check for existing Telegram CLIs and APIs:
   - Is there a TELEGRAM_BOT_TOKEN in the environment or Keychain?
     env | grep -i telegram
     security find-generic-password -s "telegram" 2>/dev/null
   - Check the phone workspace for existing Telegram integration:
     ls ~/.craft-agent-phone/ 2>/dev/null
     cat ~/.craft-agent-phone/*/config.json 2>/dev/null
   - Check for tdlib or telethon installations:
     pip3 list 2>/dev/null | grep -i tele
     brew list | grep -i tele

2. Check Telegram's local data:
   - ~/Library/Group Containers/*.Telegram/ (sandboxed data)
   - ~/Library/Application Support/Telegram Desktop/ (if exists)
   - Look for session files, database files, exported data

3. Explore automation alternatives:
   - AppleScript/JXA: Does Telegram support AppleScript?
     osascript -e 'tell application "Telegram" to get name'
   - Accessibility API: Can we read/control the UI via macOS accessibility?
     Use [skill:macos-automator] for AppleScript/Accessibility approaches
   - Telegram Bot API: https://api.telegram.org/bot<TOKEN>/
     This is the cleanest path if a bot token is available

4. Check Telegram API options:
   - Bot API (REST, simple, limited to bot-visible chats)
   - TDLib (full client library, complex but complete)
   - Telethon/Pyrogram (Python MTProto clients, user account access)
   - MTProto directly (very complex, not recommended)

### Phase 2: Architecture Decision

**If bot token available (preferred):**
- Primary: Telegram Bot API via curl (REST, fast, reliable)
- Commands limited to bot-visible chats but very stable
- This is the recommended path for automation

**If user account access needed:**
- Use Telethon (Python) as the backend
- Wrap in a Bash CLI that calls a Python helper script
- Requires initial phone number verification
- Full access to all chats, contacts, media

**If neither available:**
- Use AppleScript/Accessibility API via [skill:macos-automator]
- Most limited but requires no setup
- Can read visible text, send messages via UI automation

Expected commands:
```
telegram chats                     # List all chats
telegram messages <chat> [--limit] # Read messages
telegram send <chat> "text"        # Send a message
telegram search "query"            # Search messages
telegram contacts                  # List contacts
telegram unread                    # Unread messages
telegram me                       # Current user info
telegram media <chat>              # List media in chat
telegram stickers                  # List sticker packs
telegram forward <msg_id> <chat>   # Forward a message
```

### Phase 3-4: Build + Integrate

Determine the auth approach first, then build accordingly.
Install to /opt/homebrew/bin/telegram.
Create source at sources/telegram/ and skill at skills/telegram/.
Support --json, --no-input, --limit flags.

If using Bot API: token in macOS Keychain (service: telegram-cli-token).
If using Telethon: session file in ~/.telegram-cli/ with appropriate permissions.
```

---

## Lower Priority Apps

### Factory (AI coding agent)

```
Use [skill:electron-to-cli] and [skill:agent-browser] to explore Factory.
App: /Applications/AI/Factory.app (Electron, v0.31.0)

This is Factory AI's desktop app (Droid agent). The user already has the `droid` CLI
at /Users/kosta/.local/bin/droid — check if a desktop CLI wrapper adds value beyond
what `droid` already provides.

Recon with CDP on port 9237. Focus on:
- Session/task history that `droid` CLI doesn't expose
- Model configuration and API key management
- Git worktree management UI
- Any internal APIs beyond what `droid exec` covers

If `droid` already covers everything, just create a Craft Agent skill that documents
`droid` usage patterns instead of building a new CLI.
```

### Google Antigravity (Gemini)

```
Use [skill:electron-to-cli] and [skill:agent-browser] to explore Google Antigravity.
App: /Applications/AI/Google - Antigravity.app (Electron, v1.19.6)

This appears to be Google's Gemini/AI desktop app. Recon with CDP on port 9238.

Focus on:
- What Google APIs does it use? (Gemini API, Google AI Studio?)
- Auth token extraction (Google OAuth tokens)
- Conversation history storage
- Is there a local API or just the web wrapper?

If it's just a web wrapper around gemini.google.com, a CLI may not add much value —
the Gemini API via curl would be more useful. Consider creating a `gemini` CLI
that uses the Gemini API directly instead.
```

### Pencil (Prototyping)

```
Use [skill:electron-to-cli] and [skill:agent-browser] to explore Pencil.
App: /Applications/AI/Pencil.app (Electron, v1.1.33)

Pencil appears to be a design/prototyping tool. Recon with CDP on port 9239.

Focus on:
- Project/file management (list, open, export)
- Export capabilities (PNG, SVG, PDF)
- Template management
- Whether it has an API or is purely UI-driven

Design tools are often UI-heavy with no API — CDP/screenshot may be the
primary interface. Lower priority unless the user specifically needs automation.
```

### Upscayl (Image upscaling)

```
Use [skill:electron-to-cli] and [skill:agent-browser] to explore Upscayl.
App: /Applications/AI/Upscayl.app (Electron, v2.15.0)

Upscayl is an AI image upscaler. Recon with CDP on port 9240.

Focus on:
- Can we trigger upscaling programmatically?
- What models are available?
- Input/output folder configuration
- Batch processing capability

Expected commands:
  upscayl process <image> [--model X] [--scale N] [--output dir]
  upscayl models
  upscayl batch <folder> [--model X]

Upscayl likely wraps Real-ESRGAN or similar — check if the underlying model
binary is accessible directly, which would be faster than CDP automation.
```

### Termius (SSH client)

```
Use [skill:electron-to-cli] and [skill:agent-browser] to explore Termius.
App: /Applications/Termius.app (Electron, v9.37.2)

The user already uses SSH directly (ssh mini, etc.) and has native terminal
access. Termius adds value through:
- Host/connection management
- SFTP integration
- Port forwarding presets
- Snippet library

Recon with CDP on port 9241. Focus on:
- Can we export/import host configurations?
- Snippet management
- Is there a local database of saved connections?
- Check ~/Library/Application Support/Termius/ for data

This is lower priority since native SSH already works. A CLI would mainly
help manage Termius's host library and snippets programmatically.
```
