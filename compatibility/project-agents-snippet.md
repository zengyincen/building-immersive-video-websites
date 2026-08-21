# Project-Agent Compatibility Snippet

Use this in `AGENTS.md`, a repository instruction field, or the opening prompt
of a coding agent that does not natively discover the skill:

```md
For immersive-video work, first read `SKILL.md`. Then read only the references
that its routing points to for the current request; do not load unrelated
guidance. Preserve the project’s existing architecture and verify changes in a
browser. If a routed capability is unavailable, report the limitation and its
impact instead of simulating success.
```

This is a compatibility import, not evidence that the host has native
`SKILL.md` support. Pair it with the [builder prompt](builder-prompt.md) when a
visual builder needs implementation instructions.
