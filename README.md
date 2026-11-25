# MATLAB skills for AI agents

Seven skills that teach an AI agent (Claude Code, Codex, Ada and others that read `SKILL.md` files) to work in MATLAB the way a careful person would: run code and check how it ended, read and write data files without changing the numbers, make figures at the size a journal asks, use other people's code safely, write well-documented functions and build small apps.

They are about MATLAB itself, not about any method: no statistics, chemometrics or signal-processing recipes. The facts in them were checked with MATLAB R2024a on Windows; each skill says what it could not check.

Part of [Lovelace's Square](https://lovelacesquare.org), the open hub for chemometrics code, data and teaching material.

---

## Skills

| Skill | Why it is here |
|---|---|
| `matlab-run` | Finding the launcher, `-batch` runs that start from nothing, seeing results without a window, working out memory before a large step, loops that grow, what waits for a person, exit codes and logs, not overwriting; common errors with causes in `references/`. |
| `matlab-shared-session` | Connecting to the MATLAB the person has open (`shareEngine`, the Python engine), looking before touching, and leaving their workspace, path and settings as they were. |
| `matlab-data-files` | Looking at a file before reading it, import options for numeric headers, `;` with decimal commas and mixed columns, `.mat` versions, checks on what arrived, and writing without silent overwrites or stale rows. |
| `matlab-figures` | Figures built at their final size, `exportgraphics` against `print` when the size has to be exact, measuring the exported file and looking at it. |
| `matlab-third-party-code` | What is installed and licensed, which of several functions with one name will run, reading help and source before calling, dependencies, and the licence of code that is not the person's. |
| `matlab-writing-code` | Asking how strict to be and which licence, the help header (syntax, inputs and outputs, runnable example, author and citation), `arguments` checks, errors with identifiers, and checks before handing over. |
| `matlab-app-design` | Apps as a `uifigure` with an HTML screen: layers, messages between page and MATLAB, every click also callable from a script, pictures taken hidden and looked at; default design values in `references/`. |

## Install

**Claude Code**

```
/plugin marketplace add LovelaceSquare/matlab-skills
/plugin install matlab@matlab-skills
```

**Codex and other agents**: copy the folders inside `skills/` to the agent's skills folder (for example `~/.claude/skills/` or `~/.codex/skills/`). Each folder is one skill: a `SKILL.md` and, for some, a `references/` folder.

**Ada Essential Commons**: included as the *MATLAB* plugin.

## Tests

`evals/cases.json` holds the test prompts (Spanish and English, plus cases where no skill should fire). The test files they use are in `evals/fixtures/` and can be rebuilt with `evals/make_fixtures.py`. Notes on what is in and out of scope: `PLUGIN-NOTES.md`.

## Licence

MIT. See `LICENSE`. To cite, see `CITATION.cff`.
