# Native scope and sources

The profile is **bash-automation**. The qualified versions are
**GNU Bash 5.2.21 and ShellCheck 0.11.0** on Linux x86-64.

ShellCheck receives source on stdin with its rc and editorconfig lookup
disabled. The profile conservatively rejects inline ShellCheck directive
candidates, including matching text in heredocs. Sourced-file diagnostics
record an evidence gap. Explicitly list each file you want checked.

Use quoted arrays and pass each argument as its own value. Check the status
of operations that change directories or produce assignment values. Test
an argument beginning with a dash, a space-containing value, a literal glob,
and an empty input. The example behavior suite exercises those cases.

The Linux x86-64 ShellCheck archive matches the SHA-256 published by GitHub for the upstream release asset. Bash comes from the Ubuntu 24.04 base system and is checked for the exact supported version. See the [toolchain manifest](../toolchain.json).

The profile implements the finite rules in the catalogue. Platform branches,
application behaviors beyond the declared examples, and the effectiveness of
project-specific operating practices need their own evidence.

## Primary sources

- [GNU Bash reference manual](https://www.gnu.org/software/bash/manual/bash.html)
- [ShellCheck 0.11.0 command and policy documentation](https://github.com/koalaman/shellcheck/blob/v0.11.0/shellcheck.1.md)
- [ShellCheck 0.11.0 release](https://github.com/koalaman/shellcheck/releases/tag/v0.11.0)
