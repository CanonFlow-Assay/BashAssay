"""Bash syntax checking and a finite ShellCheck mapping."""

import re


SHELLCHECK_RULES = {
    2035: "BA004",
    2046: "BA005",
    2068: "BA006",
    2086: "BA007",
    2155: "BA008",
    2164: "BA009",
}


def inspect(target):
    syntax = target.call("bash", ["--noprofile", "--norc", "-n"], (0, 2))
    if syntax and syntax.exit_code == 2:
        target.finding("BA001")
        return

    # This profile conservatively forbids inline analyzer policy, including
    # ShellCheck-looking text in heredocs. Lint is skipped before any such
    # directive can affect source traversal or suppress a check.
    source = target.contents.decode("utf-8")
    directive = re.search(r"(?i)#\s*shellcheck\b", source)
    if directive:
        target.finding("BA002", source.count("\n", 0, directive.start()) + 1)
        return

    result = target.call("shellcheck", ["--norc", "--shell=bash", "--format=json1", "-"])
    if result is None:
        return

    from .engine import strict_json

    try:
        diagnostics = strict_json(result.stdout)["comments"]
        if not isinstance(diagnostics, list) or bool(diagnostics) != (result.exit_code == 1):
            raise ValueError("inconsistent ShellCheck status")
        for diagnostic in diagnostics:
            code, line, column = (diagnostic[key] for key in ("code", "line", "column"))
            level = diagnostic["level"]
            if not all(type(value) is int and value > 0 for value in (code, line, column)):
                raise ValueError("invalid ShellCheck diagnostic")
            if level not in ("error", "warning", "info", "style"):
                raise ValueError("invalid ShellCheck severity")
            if code in (1090, 1091):
                target.gaps.append(f"ShellCheck SC{code}: sourced content is outside this check")
                continue
            rule = SHELLCHECK_RULES.get(code, "BA003" if level == "error" else None)
            if rule:
                target.finding(rule, line, column, f"SC{code}")
    except (KeyError, TypeError, ValueError, RecursionError):
        target.failures.append("shellcheck: malformed native diagnostic output")
