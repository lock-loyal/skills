---
name: browser-use
description: Automates browser interactions for web testing, form filling, screenshots, and data extraction. Use when the user needs to navigate websites, interact with web pages, fill forms, take screenshots, or extract information from web pages.
allowed-tools: Bash(browser-use:*)
---

# Browser Automation with browser-use CLI

The `browser-use` command provides fast, persistent browser automation. It maintains browser sessions across commands, enabling complex multi-step workflows.

## Prerequisites

Before using this skill, `browser-use` must be installed and configured. Run diagnostics to verify:

```bash
browser-use doctor
```

For more information, see https://github.com/browser-use/browser-use/blob/main/browser_use/skill_cli/README.md

## Core Workflow

1. **Navigate**: `browser-use --browser real --profile "Profile 3" open <url>` - Opens URL using Profile 3 (starts browser if needed)
2. **Inspect**: `browser-use state` - Returns clickable elements with indices
3. **Interact**: Use indices from state to interact (`browser-use click 5`, `browser-use input 3 "text"`)
4. **Verify**: `browser-use state` or `browser-use screenshot` to confirm actions
5. **Repeat**: Browser stays open between commands

## Browser Modes

```bash
browser-use --browser real --profile "Profile 3" open <url>  # Default: Real Chrome with Profile 3
browser-use --browser real --profile "Default" open <url>   # Real Chrome with specific profile
browser-use --browser chromium open <url>                   # Headless Chromium (no profile)
browser-use --browser chromium --headed open <url>          # Visible Chromium window
```

- **real**: Uses a real Chrome binary with your actual Chrome profile (cookies, logins, extensions). Default is "Profile 3"
- **chromium**: Fast, isolated, headless by default. Use when you don't need profile data

## Essential Commands

```bash
# Navigation
browser-use --browser real --profile "Profile 3" open <url>   # Navigate to URL (uses Profile 3 by default)
browser-use --browser chromium open <url>                     # Navigate without profile
browser-use back                                              # Go back
browser-use scroll down                                       # Scroll down (--amount N for pixels)

# Page State (always run state first to get element indices)
browser-use state                         # Get URL, title, clickable elements
browser-use screenshot                    # Take screenshot (base64)
browser-use screenshot path.png           # Save screenshot to file

# Interactions (use indices from state)
browser-use click <index>                 # Click element
browser-use type "text"                   # Type into focused element
browser-use input <index> "text"          # Click element, then type
browser-use keys "Enter"                  # Send keyboard keys
browser-use select <index> "option"       # Select dropdown option

# Data Extraction
browser-use eval "document.title"         # Execute JavaScript
browser-use get text <index>              # Get element text
browser-use get html --selector "h1"      # Get scoped HTML

# Wait
browser-use wait selector "h1"            # Wait for element
browser-use wait text "Success"           # Wait for text

# Session
browser-use sessions                      # List active sessions
browser-use close                         # Close current session
browser-use close --all                   # Close all sessions
```

For complete command reference, see [references/commands.md](references/commands.md)

## Common Workflows

### Authenticated Browsing with Profiles

Profile 3 is used by default, so you're already authenticated on sites you've logged into (e.g. Gmail, GitHub, internal tools).

**Default behavior:** `browser-use --browser real --profile "Profile 3" open <url>` automatically uses your Profile 3 login sessions.

#### Using a different profile

If you need to use a different profile instead of Profile 3:

```bash
# List available local Chrome profiles
browser-use -b real profile list
# → Default: Person 1 (user@gmail.com)
# → Profile 1: Work (work@company.com)
# → Profile 3: Personal (personal@gmail.com)

# Browse with a specific profile
browser-use --browser real --profile "Profile 1" open https://github.com
```

#### Check profile cookies

```bash
browser-use -b real profile cookies "Profile 3"
# → youtube.com: 23
# → google.com: 18
# → github.com: 2
```

#### Fine-grained cookie control

```bash
# Export cookies to file, manually edit, then import to another session
browser-use --browser real --profile "Profile 3" cookies export /tmp/cookies.json
browser-use cookies import /tmp/cookies.json
```

## Global Options

| Option | Description |
|--------|-------------|
| `--session NAME` | Use named session (default: "default") |
| `--browser MODE` | Browser mode: chromium, real |
| `--headed` | Show browser window (chromium mode) |
| `--profile NAME` | Browser profile name. Works with `open` — does NOT work with `run` |
| `--json` | Output as JSON |
| `--mcp` | Run as MCP server via stdin/stdout |

**Session behavior**: All commands without `--session` use the same "default" session. The browser stays open and is reused across commands. Use `--session NAME` to run multiple browsers in parallel.

## Tips

1. **Always run `browser-use -b real --profile "Profile 3" state` first** to see available elements and their indices
2. **Use `--headed` for debugging** to see what the browser is doing
3. **Sessions persist** — the browser stays open between commands
4. **Use `--json`** for programmatic parsing
5. **Python variables persist** across `browser-use python` commands within a session
6. **CLI aliases**: `bu`, `browser`, and `browseruse` all work identically to `browser-use`

## Troubleshooting

**Run diagnostics first:**
```bash
browser-use doctor
```

**Browser won't start?**
```bash
browser-use close --all                                               # Close all sessions
browser-use --browser real --profile "Profile 3" --headed open <url>  # Try with visible window
```

**Element not found?**
```bash
browser-use state                     # Check current elements
browser-use scroll down               # Element might be below fold
browser-use state                     # Check again
```

**Session issues?**
```bash
browser-use sessions                                                      # Check active sessions
browser-use close --all                                                   # Clean slate
browser-use --browser real --profile "Profile 3" open <url>               # Fresh start
```

## Cleanup

**Always close the browser when done:**

```bash
browser-use close                     # Close browser session
browser-use close --all               # Close all sessions
```
