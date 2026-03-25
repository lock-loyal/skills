---
name: opencli
description: Use when a task should be executed through the installed `opencli` CLI to access supported websites or desktop apps through existing adapters. Trigger on requests like "use opencli", "check X/Twitter/xtwitter, Reddit, Grok, Bilibili, arXiv/arxiv papers, or finance quotes/news from the terminal", or "read or automate WeChat, Codex, Cursor, or Notion with opencli".
---

# OpenCLI

Use `opencli` for tasks that map to an existing installed adapter. Keep this skill focused on consuming built-in adapters; do not treat `explore`, `synthesize`, `generate`, `install`, or `register` as the default workflow.

## Quick Start

1. Run `opencli list` to confirm the adapter exists.
2. Run `opencli <adapter> --help` before using a specific adapter.
3. Classify the adapter before acting:
   - `public`: no login or local app session required
   - browser-backed: requires Chrome login and often Browser Bridge
   - desktop app: requires app-specific setup such as CDP or Accessibility
4. Prefer read-only commands first.
5. Read the matching adapter doc under `./adapters/` for exact prerequisites and examples.

## Mode Selection

Use this routing logic before running commands:

- If the target is a public source such as `arxiv`, `wikipedia`, `hackernews`, or `bbc`, use the adapter directly.
- If the target is a browser-authenticated site such as `reddit`, `twitter`, `youtube`, or `weread`, verify Chrome session and adapter prerequisites first.
- If the target is a desktop app such as `codex`, `cursor`, `notion`, `wechat`, or `feishu`, read the adapter doc first and follow its setup exactly.
- If local docs and the live CLI disagree on adapter names, commands, or flags, trust `opencli list` and `opencli <adapter> --help`.

## Adapter References

Use these local docs instead of copying adapter command tables into this skill:

- Overview: [./adapters/index.md](./adapters/index.md)
- Browser example: [./adapters/browser/reddit.md](./adapters/browser/reddit.md)
- Browser example: [./adapters/browser/twitter.md](./adapters/browser/twitter.md)
- Desktop example: [./adapters/desktop/codex.md](./adapters/desktop/codex.md)
- Desktop example: [./adapters/desktop/chatgpt.md](./adapters/desktop/chatgpt.md)

Notable live-doc mismatch:

- The local Discord doc uses `opencli discord ...`, but the installed CLI currently exposes `opencli discord-app ...`. Verify live adapter names before acting.

## Examples

```bash
opencli arxiv search "transformer attention" --limit 5
opencli reddit hot --limit 5 -f json
opencli codex status
opencli codex read
```

## Safety And Recovery

- Treat commands such as `send`, `post`, `comment`, `reply`, `write`, `delete`, `like`, and `follow` as mutating.
- Use mutating commands only when the user explicitly asks for that action.
- When prerequisites are unclear, inspect the selected adapter doc first.
- For browser-backed adapters, mention Browser Bridge and login requirements only when the selected adapter doc requires them.
