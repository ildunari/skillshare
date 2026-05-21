# curl.md heavy-site benchmark — 2026-05-13

Use this as routing guidance for Hermes/AutoCLI URL-to-markdown work.

## Summary

`curl.md` is a strong first-pass markdown reducer for documentation, public forums, normal code-hosting pages, Apple docs, and PubMed/search-result style pages when query strings are encoded correctly. It is not a universal browser replacement.

## Good fits

- Documentation pages: Anthropic docs, Apple SwiftUI docs, normal API references.
- Public forum/thread pages: LPSG-style public thread pages produced useful markdown.
- Normal GitHub repositories: standard repo pages worked well.
- PubMed: works for query pages when the target query is encoded into the path segment.

## Weak or blocked fits

- X/Twitter: returned empty shells; use `x_twitter`/`xurl` first.
- Reddit: often returned verification or blocked shells.
- YouTube: can return 429/rate-limit pages; use video/transcript-specific tools instead.
- GitHub repos with dots in the repo name, e.g. `wevm/curl.md`: observed upstream 404 behavior; try normal browser/web extraction or GitHub CLI fallback.

## Rate limits

Observed/current docs at benchmark time:

- Anonymous standard fetch: `100/hour`.
- Authenticated standard fetch: `1,000/hour`.
- Anonymous `objective=` narrowing: `3/hour`.
- Authenticated `objective=` narrowing: `10/hour`.
- Paid usage can skip those limits.

Useful headers include `x-ratelimit-limit`, `x-ratelimit-remaining`, `x-ratelimit-reset`, `retry-after`, `x-tokens-count`, `x-tokens-saved`, and `x-cache`.

## Auth on Mac Studio

The authenticated curl.md token for Hermes is stored in 1Password:

```bash
op item get 'curl.md API Token - Hermes Mac Studio' --vault CLI --reveal --fields credential
```

Prefer:

```bash
export CURLMD_API_KEY="$(op item get 'curl.md API Token - Hermes Mac Studio' --vault CLI --reveal --fields credential)"
npx -y curl.md@0.1.1 https://example.com
```

Hermes also has a `curlmd_fetch` tool that reads `CURLMD_API_KEY` or the 1Password item automatically when available.

## Query-string gotcha

Do not send target query strings as curl.md API query params by accident. Encode the query into the target URL path segment:

```text
https://curl.md/pubmed.ncbi.nlm.nih.gov/%3Fterm=PLGA+drug+delivery
```

## Routing rule

Use `curlmd_fetch` for clean markdown first-pass extraction on likely-good static/public pages. If it stalls, rate-limits, returns blocked/weak content, or hits a known weak site, switch to the site-specific tool (`x_twitter`, GitHub CLI, video/transcript tooling), browser automation, or regular `curl`/HTML inspection.
