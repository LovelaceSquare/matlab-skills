# MATLAB skills for AI agents

Seven skills that teach an AI agent to work in MATLAB the way a careful person would: run code and check how it ended, read and write data files without changing the numbers, make figures at the size a journal asks, use other people's code safely, write well-documented functions and build small apps.

They are about MATLAB itself, not about any method: no statistics, chemometrics or signal-processing recipes. The facts in them were checked in MATLAB R2024a on Windows; each skill says what it could not check.

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

Left out: Simulink, App Designer's visual editor, MATLAB Compiler and method guides of any field.

## Use

Each folder inside `skills/` is one skill in the open Agent Skills format: a `SKILL.md` file (a short header with its name and when to use it, then the instructions) and, for some, a `references/` folder the skill points to.

Copy the folders you want to wherever your agent reads skills from, or give their `SKILL.md` to an agent that has no skills folder. They work with any agent that can read files and run commands.

## Licence

MIT. See `LICENSE`. To cite, see `CITATION.cff`.
