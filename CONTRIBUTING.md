# Contributing

A component is one README building block: a widget, a markdown trick, an HTML layout, a writing rule, or a generator script.

## Add a component

1. **Reference.** Copy `references/_COMPONENT_TEMPLATE.md` to `references/<name>.md`. Include the paste-ready snippet, every parameter with its default, when to use it, gotchas (what GitHub strips, activation steps, rate limits, privacy) and the date you last confirmed the URL works. Keep it under ~150 lines.
2. **Generator.** If the component is a parameterised URL, add a subcommand to `scripts/snippets.py` (or a new script). Python 3 standard library only; Pillow is the one optional dependency.
3. **Register.** Add a row to the Components table in `SKILL.md` and `README.md`. Keep `SKILL.md` under 500 lines and move detail into `references/`.
4. **Lint rule.** If the component has a common failure, add a check to `scripts/lint_readme.py` with a severity: ERR (renders wrong), WARN (probably wrong), TIP (polish).
5. **Test.** Run the script, paste the output into a scratch README, check the Preview in light and dark theme, run the linter on it, and add a triggering prompt to `evals/evals.json`.

## Standards

- Anything that ends up in a user's README has no em dashes and no marketing words. The linter enforces this on the examples; keep them clean.
- Examples use fictional handles (`octocat-dev`) and `example.dev` domains.
- Never add a component that needs a secret token pasted into a README.
