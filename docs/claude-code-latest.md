# Claude Code 最新設定リファレンス
_自動同期: 2026-05-22 06:54:59_  |  _CLI バージョン: v2.1.148_

---

## 最新モデル ID

- `claude-opus-4-6`
- `claude-sonnet-4-6`

## フックイベント

- `Notification`
- `PermissionDenied`
- `PermissionRequest`
- `PostToolUse`
- `PostToolUseFailure`
- `PreToolUse`
- `SessionEnd`
- `SessionStart`
- `Setup`
- `Stop`
- `StopFailure`
- `SubagentStop`
- `UserPromptExpansion`
- `UserPromptSubmit`

## settings.json キー

- `apiKeyHelper`
- `cleanupPeriodDays`
- `env`
- `forceLoginMethod`
- `forceLoginOrgUUID`
- `hooks`
- `includeCoAuthoredBy`
- `model`
- `permissions`
- `preferredNotifChannel`
- `spinnerTipsEnabled`
- `theme`
- `verbose`

## 公式ドキュメント抜粋: Settings

```
Documentation Index 
 Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt 
 Use this file to discover all available pages before exploring further. 
 Claude Code offers a variety of settings to configure its behavior to meet your needs. You can configure Claude Code by running the /config command when using the interactive REPL, which opens a tabbed Settings interface where you can view status information and modify configuration options. ​ Configuration scopes 
 Claude Code uses a scope system to determine where configurations apply and who they’re shared with. Understanding scopes helps you decide how to configure Claude Code for personal use, team collaboration, or enterprise deployment. ​ Available scopes 
 Scope 
 Location 
 Who it affects 
 Shared with team? 
 
 Managed 
 Server-managed settings, plist / registry, or system-level managed-settings.json 
 All users on the machine 
 Yes (deployed by IT) 
 
 User 
 ~/.claude/ directory 
 You, across all projects 
 No 
 
 Project 
 .claude/ in repository 
 All collaborators on this repository 
 Yes (committed to git) 
 
 Local 
 .claude/settings.local.json 
 You, in this repository only 
 No (gitignored) 
 
 ​ When to use each scope 
 Managed scope is for: Security policies that must be enforced organization-wide 
 Compliance requirements that can’t be overridden 
 Standardized configurations deployed by IT/DevOps 
 User scope is best for: Personal preferences you want everywhere (themes, editor settings) 
 Tools and plugins you use across all projects 
 API keys and authentication (stored securely) 
 Project scope is best for: Team-shared settings (permissions, hooks, MCP servers) 
 Plugins the whole team should have 
 Standardizing tooling across collaborators 
 Local scope is best for: Personal overrides for a specific project 
 Testing configurations before sharing with the team 
 Machine-specific settings that won’t work for others 
 ​ How scopes interact 
 When the same setting appears in multiple scopes, Claude Code applies them in priority order: Managed (highest) - can’t be overridden by anything 
 Command line arguments - temporary session overrides 
 Local - overrides project and user settings 
 Project - overrides user settings 
 User (lowest) - applies when nothing else specifies the setting 
 For example, if your user settings set spinnerTipsEnabled to true and
```

## 公式ドキュメント抜粋: Hooks

```
Documentation Index 
 Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt 
 Use this file to discover all available pages before exploring further. 
 For a quickstart guide with examples, see Automate workflows with hooks . Hooks are user-defined shell commands, HTTP endpoints, or LLM prompts that execute automatically at specific points in Claude Code’s lifecycle. Use this reference to look up event schemas, configuration options, JSON input/output formats, and advanced features like async hooks, HTTP hooks, and MCP tool hooks. If you’re setting up hooks for the first time, start with the guide instead. ​ Hook lifecycle 
 Hooks fire at specific points during a Claude Code session. When an event fires and a matcher matches, Claude Code passes JSON context about the event to your hook handler. For command hooks, input arrives on stdin. For HTTP hooks, it arrives as the POST request body. Your handler can then inspect the input, take action, and optionally return a decision. Events fall into three cadences: once per session ( SessionStart , SessionEnd ), once per turn ( UserPromptSubmit , Stop , StopFailure ), and on every tool call inside the agentic loop ( PreToolUse , PostToolUse ): The table below summarizes when each event fires. The Hook events section documents the full input schema and decision control options for each one. Event 
 When it fires 
 
 SessionStart 
 When a session begins or resumes 
 
 Setup 
 When you start Claude Code with --init-only , or with --init or --maintenance in -p mode. For one-time preparation in CI or scripts 
 
 UserPromptSubmit 
 When you submit a prompt, before Claude processes it 
 
 UserPromptExpansion 
 When a user-typed command expands into a prompt, before it reaches Claude. Can block the expansion 
 
 PreToolUse 
 Before a tool call executes. Can block it 
 
 PermissionRequest 
 When a permission dialog appears 
 
 PermissionDenied 
 When a tool call is denied by the auto mode classifier. Return {retry: true} to tell the model it may retry the denied tool call 
 
 PostToolUse 
 After a tool call succeeds 
 
 PostToolUseFailure 
 After a tool call fails 
 
 PostToolBatch 
 After a full batch of parallel too
```

## 公式ドキュメントページ一覧 (llms.txt より抜粋)

```
# Claude Code Docs

> Official documentation for Claude Code, Anthropic's agentic coding tool available in the terminal, IDE, desktop app, and browser. Covers installation, configuration, skills, subagents, hooks, MCP, the Agent SDK, and reference material.

## Docs

- [Set up Claude Code for your organization](https://code.claude.com/docs/en/admin-setup.md): A decision map for administrators deploying Claude Code, covering API providers, managed settings, policy enforcement, usage monitoring, and data handling.
- [How the agent loop works](https://code.claude.com/docs/en/agent-sdk/agent-loop.md): Understand the message lifecycle, tool execution, context window, and architecture that power your SDK agents.
- [Use Claude Code features in the SDK](https://code.claude.com/docs/en/agent-sdk/claude-code-features.md): Load project instructions, skills, hooks, and other Claude Code features into your SDK agents.
- [Track cost and usage](https://code.claude.com/docs/en/agent-sdk/cost-tracking.md): Learn how to track token usage, estimate costs, and configure prompt caching with the Claude Agent SDK.
- [Give Claude custom tools](https://code.claude.com/docs/en/agent-sdk/custom-tools.md): Define custom tools with the Claude Agent SDK's in-process MCP server so Claude can call your functions, hit your APIs, and perform domain-specific operations.
- [Rewind file changes with checkpointing](https://code.claude.com/docs/en/agent-sdk/file-checkpointing.md): Track file changes during agent sessions and restore files to any previous state
- [Intercept and control agent behavior with hooks](https://code.claude.com/docs/en/agent-sdk/hooks.md): Intercept and customize agent behavior at key execution points with hooks
- [Hosting the Agent SDK](https://code.claude.com/docs/en/agent-sdk/hosting.md): Deploy and host Claude Agent SDK in production environments
- [Connect to external tools with MCP](https://code.claude.com/docs/en/agent-sdk/mcp.md): Configure MCP servers to extend your agent
```

## CHANGELOG (最新 4 リリース)

# Changelog

## 2.1.148

- Fixed the Bash tool returning exit code 127 on every command for some users (a regression introduced in 2.1.147)

## 2.1.147

- Pinned background sessions (`Ctrl+T` in `claude agents`) now stay alive when idle, are restarted in place to apply Claude Code updates, and are shed under memory pressure only after non-pinned sessions
- Renamed `/simplify` to `/code-review`. It now reports correctness bugs at a chosen effort level (e.g., `/code-review high`); pass `--comment` to post findings as inline GitHub PR comments. The old cleanup-and-fix behavior has been removed
- Improved auto-updater: retries transient network failures, reports specific error categories and OS error codes on failure, and shows the current version when an update fails
- Improved diff rendering performance for large file edits
- Prompt history no longer records consecutive duplicate entries — recalling a prompt with arrow-up and submitting it again won't add another copy
- Fixed enterprise login restrictions (`forceLoginOrgUUID` and `forceLoginMethod` managed-settings) not being enforced against third-party-provider and API-key sessions
- Fixed `&` in `!` command output displaying as `&amp;`, which broke copy-pasting URLs from commands like `gcloud auth login` on headless machines
- Fixed unknown slash commands silently doing nothing in headless/SDK mode — they now show an error message
- Fixed `/help` rendering a broken tab header and showing only one command per page on small terminals when not in fullscreen mode
- Fixed shell snapshot dropping user functions whose names start with a single underscore, which broke aliases referencing them
- Fixed plugin agents that declare multiple `Agent(...)` types in `tools:` frontmatter dropping all but the last entry
- Fixed hook `if` conditions like `PowerShell(git push*)` never matching — only `PowerShell(*)` worked
- Fixed PowerShell tool dropping output for commands that rely on the default formatter
- Fixed: on Windows, "Yes, and don't ask again" for a PowerShell script invocation now writes a rule that actually matches on subsequent runs
- Fixed PowerShell tool failing on Windows with exit code 1 when `pwsh` is installed via winget or the Microsoft Store
- Fixed `/effort` opening with the slider on the wrong level — it now starts at your current effort
- Fixed paginating MCP servers dropping resources, templates, and prompts past page 1
- Fixed full-screen strobing in attached background sessions on Windows Terminal while Claude is streaming
- Fixed: on Windows, removing a background-job worktree no longer follows NTFS junctions into the main repo
- Fixed `/background` refusing sessions whose only typed input was a skill or custom slash command
- Fixed auto mode suppressing `AskUserQuestion` when the user or a skill explicitly relies on it; the auto-mode classifier now sees the user's answers as intent signal
- Fixed `/theme` "New custom theme" and color editor dialogs not responding to Esc
- Fixed an uncaught exception at the end of streaming sessions when running via the Agent SDK
- Fixed a rare hang when waiting for scroll to settle on Windows
- Fixed stale and doubled rows in the agent view list on Windows when background session results contain wide (CJK) characters
- Fixed pasted text being delivered to agents as an unreadable `[Pasted text #N]` placeholder instead of the actual content
- Fixed plugin component counts in `claude plugin details` and `/plugin` being doubled when a plugin's manifest listed paths overlapping its default directories
- Fixed backgrounded sessions re-prompting for tool permissions you already granted with "don't ask again"
- Fixed GNOME Terminal right-click and middle-click paste not inserting text
- Fixed `CLAUDE_CODE_SUBAGENT_MODEL` not applying to teammate processes spawned by agent teams
- Fixed slash commands followed by a tab or newline being treated as an unknown command
- Fixed several spacing and layout glitches in the `/plugin`, `/status`, `/mobile`, `/sandbox`, and `/permissions` menus
- Fixed stripped images prompting the model to repeatedly re-read media that was no longer present

## 2.1.145

- Added `claude agents --json` to list live Claude sessions as JSON for scripting (tmux-resurrect, status bars, session pickers)
- Added `agent_id` and `parent_agent_id` attributes to `claude_code.tool` OTEL spans, and fixed trace parenting so background subagent spans nest under the dispatching Agent tool span
- Status line JSON input now includes GitHub repo and PR information when detected
- `/plugin` Discover and Browse screens now show a plugin's commands, agents, skills, hooks, and MCP/LSP servers before installation
- `claude agents` terminal tab title now shows the awaiting-input count so an alt-tabbed window tells you when an agent needs attention
- Slash command and @-mention suggestion list now supports mouse hover and click in fullscreen mode
- Stop and SubagentStop hook input now includes `background_tasks` and `session_crons` fields
- Fixed a permission-prompt bypass where bare variable assignments to non-allowlisted environment variables in Bash commands were auto-approved
- Fixed MCP prompt slash commands showing raw server validation errors when a required argument is omitted — the error now names the missing argument and shows expected usage
- Fixed the spinner and elapsed-time display freezing until a keypress after the terminal was resized or refocused
- Fixed the cross-project resume hint failing in default Windows PowerShell 5.1 — Windows now uses `;` as the command separator
- Fixed voice push-to-talk not working in the agent view's reply pane
- Fixed task lists rendering in random order when several tasks are created at once
- Fixed stale "Failed to install Anthropic marketplace" banner showing when the marketplace is already installed
- Fixed the PR badge in the footer not updating immediately after `gh pr create` and other PR-state-changing commands run in-session
- Fixed Agent Teams teammates with non-ASCII names failing every API call due to invalid header encoding
- Fixed `/review` using a deprecated `projectCards` GraphQL query that errored on repos with Classic Projects
- Fixed `claude plugin validate` not flagging `skills:` entries that point at a file instead of a directory — the error now suggests the parent directory
- Fixed an infinite loop where a skill using `context: fork` could repeatedly re-invoke itself instead of running
- Improved the Read tool to return a truncated first page with a "PARTIAL view" notice instead of a hard error when a whole-file read exceeds the token limit

## 2.1.144

- Added `/resume` support for background sessions — sessions started via `claude --bg` or agent view now appear alongside interactive ones, marked with `bg`
- Added elapsed duration to background subagent completion notifications (e.g. "Agent completed · 3h 2m 5s")
- The `/plugin` browse and discover panes now show when a plugin was last updated
- `/model` now changes the model for the current session only; press `d` in the model picker to set a default for new sessions
- Renamed "extra usage" to "usage credits" across CLI copy; `/extra-usage` is now `/usage-credits` (old name still works)
- Fixed startup hanging up to 75s when `api.anthropic.com` is unreachable (captive portal, firewall, VPN issues) — side-channel API calls now time out after 15s
- Fixed garbled terminal output after a missed window-resize event (e.g. dragging a VS Code split-pane divider) — now self-heals on the next frame instead of requiring Ctrl+L
- Fixed progressive terminal display corruption (stale/garbled glyphs) that could appear in very long sessions and only cleared on terminal resize or restart
- Reduced terminal rendering glitches in VS Code by reducing spinner animation color count
- Fixed macOS background sessions crashing with "exit 1 before init" when the project lives under a Full Disk Access-protected folder (regression in 2.1.143)
- Fixed an unrecoverable conversation when reading a file whose image extension doesn't match its contents (e.g. HTML saved as .png) — now falls back to text
- Fewer spurious tool errors during search: `head`/`tail` file views now satisfy the read-before-edit check, and a "no matches" result (exit code 1) from `egrep`, `fgrep`, `git grep`, or `git diff` is no longer reported as a command failure
- Fixed `/branch` failing with "No conversation to branch" after entering a worktree or in some background sessions
- Fixed pressing Escape in the AskUserQuestion notes field aborting the turn instead of returning to answer selection
- Fixed model selection not applying when changed via the IDE model picker or `applyFlagSettings` after startup
- Resumed sessions now keep the model they were using instead of picking up another session's `/model` choice
- Fixed Bedrock and Vertex users unable to select "Opus (1M context)" from the `/model` picker (regression in v2.1.129)
- Fixed remote-session login failing with "Can't access this organization" for users with `forceLoginMethod` and `forceLoginOrgUUID` set
- Fixed MCP servers with paginated `tools/list` responses only returning the first page, silently dropping tools
- Fixed MCP images with unsupported MIME types (e.g. SVG) breaking the conversation — now saved to disk and referenced in the tool result
- Fixed file descriptor exhaustion when a build runs inside a skill directory — non-`.md` files no longer trigger skill reloads
- Fixed session title being generated from plugin monitor output instead of the user's first prompt
- Fixed Skill tool failing with permission error in headless mode (regression in v2.1.141)
- Fixed plugins enabled in your own settings showing "not cached" errors after first load on a fresh machine; plugins enabled only by a project's `.claude/settings.json` now show an actionable `claude plugin install` hint
- Fixed `claude mcp list` silently reporting no servers when `.mcp.json` can't be parsed (e.g. using VS Code's `"servers"` key instead of `"mcpServers"`) — now shows configuration errors
- Fixed background side-queries on custom `ANTHROPIC_BASE_URL` setups and Bedrock Mantle not using Haiku — now falls back correctly when a first-party API key is configured or no Haiku model is set
- Fixed scrolling in attached background sessions on Windows — PgUp/PgDn, mouse wheel, and Ctrl+O transcript navigation now work
- Fixed a crash when closing the terminal while attached to a background session
- Fixed on Windows, pressing ← in `claude agents` leaving the list unresponsive to keyboard input
- Fixed ghost characters at the left edge when switching panes in Agent View on Windows Terminal with CJK content
- `/bg` and `←`-detach now preserve directories added via `/add-dir`
- Fixed Edit/Write refusing with "background session hasn't isolated its changes yet" right after detaching a session that was already editing in place
- Fixed `claude respawn <id>` on a stopped background session showing "stopped" instead of running
- Fixed `/resume` picker not showing sessions forked from a background session
- Fixed opening a session from `claude agents` or running `claude logs <id>` hanging when the background service is unresponsive — now times out after 10s with a recovery hint
- Fixed background Bash tasks spawned by subagents staying "Running" in SDK task panels after the process exits
- Fixed completed or stopped background sessions briefly failing to wake being permanently marked as a startup crash
- Fixed markdown links in `claude agents` attached sessions rendering as plain text instead of clickable hyperlinks
- Fixed custom `spinnerVerbs` applying to the post-turn duration message — past-tense built-ins like "Worked for 5s" are restored there
- `claude agents` / `--bg` rejection messages now name the specific gate (non-TTY, env var, or setting) instead of a generic message
- `claude --bg --name <label>` now echoes the name in the post-spawn confirmation
- `claude agents`: renaming a background session with Ctrl+R now updates the attached session's banner immediately
- Background session worktree isolation guard now applies for non-git VCS users with `WorktreeCreate` hooks configured
- Plugin marketplace add/update now respects `CLAUDE_CODE_PLUGIN_PREFER_HTTPS`
- `/plugin` now returns to the Installed list after enabling, disabling, or uninstalling a plugin
- `/doctor` now shows an exec-form example when a command hook is missing the `command` field
- Skill-listing truncation is no longer shown as a startup notification — run `/doctor` for the full breakdown
- Improved recovery from rare pre-response stream stalls — now retries streaming once instead of falling back to a slower non-streaming request
- Improved SDK/headless MCP startup: pre-wait now overlaps startup instead of blocking before the first turn (up to 2s faster with slow MCP servers)
- The post-survey follow-up hint now appears after every non-dismiss survey response with context-aware copy, making it easier to share more detail via /feedback.


## 現在の .claude/settings.json

```json
{
  "permissions": {
    "allow": [
      "Read:*",
      "Bash:git:*",
      "Write:*",
      "Edit:*"
    ],
    "deny": [
      "Read:.env*",
      "Bash:sudo:*",
      "Bash:rm -rf /:*"
    ]
  },
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash /home/user/claude/.claude/hooks/session-start.sh",
            "timeout": 60
          }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash /home/user/claude/.claude/hooks/auto-push.sh",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## 取得元
- https://registry.npmjs.org/@anthropic-ai/claude-code/latest
- https://raw.githubusercontent.com/anthropics/claude-code/main/README.md
- https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md
- https://code.claude.com/docs/llms.txt
- https://code.claude.com/docs/en/settings
- https://code.claude.com/docs/en/hooks
- https://code.claude.com/docs/en/overview
