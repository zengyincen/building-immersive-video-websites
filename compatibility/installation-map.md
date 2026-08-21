# Installation and Import Map

Native installation means the named environment is configured to discover its
own local skill directory. Compatibility import means paste or attach the
listed project guidance to that platform; it does **not** create native skill
support. Availability depends on the account, product version, and workspace
configuration—there is no universal native `SKILL.md` interface.

| Platform | Route | What to do |
| --- | --- | --- |
| Codex | Native installation, when the local Codex skills directory is enabled | Run `python3 scripts/install-skill.py --target codex`; otherwise use the compatibility snippet. |
| Claude Code | Native installation, only where its local Skills feature is enabled | Run `python3 scripts/install-skill.py --target claude`; otherwise import the snippet and builder prompt. |
| WorkBuddy | Compatibility import | Put the [project-agent snippet](project-agents-snippet.md) in its project instructions and attach the [builder prompt](builder-prompt.md). |
| Atoms | Compatibility import | Paste or attach the builder prompt and project-agent snippet in the project’s instruction surface. |
| Base44 | Compatibility import | Paste or attach the builder prompt and project-agent snippet in the project’s instruction surface. |
| Lovable | Compatibility import | Paste or attach the builder prompt and project-agent snippet in the project’s instruction surface. |
| Replit | Compatibility import | Add the project-agent snippet to repository guidance and give the builder prompt to the agent. |
| Bolt | Compatibility import | Paste or attach the builder prompt and project-agent snippet in the project’s instruction surface. |
| v0 | Compatibility import | Paste the builder prompt with the request and retain the snippet in project guidance if available. |

The installer also offers an `agents` target for a compatible local
`~/.agents/skills` setup; that is a local convention, not a claim about any
specific hosted builder. Use `--dry-run` before installation and `--force` only
when a backup of an existing skill is acceptable.
