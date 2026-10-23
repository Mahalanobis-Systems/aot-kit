# Security policy

Please report security problems privately to **ops@mahalsystems.ai**, not in a public issue.
Include what you found, how to reproduce it, and the aot-kit version (`version` in
`.claude-plugin/plugin.json`, or `claude plugin list`). We will acknowledge your report within
three working days and keep you informed until it is fixed.

aot-kit is a set of skills: instructions Claude Code follows in your repository, with your
permissions. It runs no code of its own in your environment, sends no telemetry and needs no
account. Reports are especially welcome about any skill that could lead Claude to:

- send code, traces or data from your repository anywhere;
- take an irreversible action without asking (deleting data, pushing, deploying);
- follow instructions from untrusted content, such as a cited web page or a trace, as if they
  came from you.

A skill that recommends a change with a security cost (wider tool access, less sandboxing)
should say so in its caveats. If one doesn't, a regular issue is fine.
