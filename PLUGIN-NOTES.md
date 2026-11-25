# matlab — working in MATLAB as an agent

No other plugin required. This plugin is about MATLAB itself: it has no
guides on methods (statistics, chemometrics, signal processing). The
`python` plugin follows the same rule; the two can be on together
(skill names are `matlab-*` and `python-*`).

Rule for inclusion: a line stays only if an agent would act differently
for having read it. What is here is what an agent working without the
MATLAB window does not reliably get right unaided: every run starting
from nothing, figures and prompts it cannot see, memory that runs out
without warning, imports that silently change numbers or headers,
exports that are not the size asked for, a downloaded function that
takes the place of another, files and variables replaced without
asking, and apps nobody looked at. The facts were checked in MATLAB
R2024a on Windows; each guide says what it could not check.

| Skill | Why it is here |
|---|---|
| `matlab-run` | Finding the launcher, `-batch` runs that start from nothing, seeing results without a window, working out memory before a large step, loops that grow, what waits for a person, exit codes and logs, not overwriting; common errors with causes in `references/`. |
| `matlab-shared-session` | Connecting to the MATLAB the person has open (`shareEngine`, the Python engine), looking before touching, and leaving their workspace, path and settings as they were. |
| `matlab-data-files` | Looking at a file before reading it, import options for numeric headers, `;` with decimal commas and mixed columns, `.mat` versions, checks on what arrived, and writing without silent overwrites or stale rows. |
| `matlab-figures` | Figures built at their final size, `exportgraphics` against `print` when the size has to be exact, measuring the exported file and looking at it. |
| `matlab-third-party-code` | What is installed and licensed, which of several functions with one name will run, reading help and source before calling, dependencies, and the licence of code that is not the person's. |
| `matlab-writing-code` | Asking how strict to be and which licence, the help header (syntax, inputs and outputs, runnable example, author and citation), `arguments` checks, errors with identifiers, and checks before handing over. |
| `matlab-app-design` | Apps as a `uifigure` with an HTML screen: layers, messages between page and MATLAB, every click also callable from a script, pictures taken hidden and looked at; default design values in `references/`. |

Left out: Simulink, App Designer's visual editor, MATLAB Compiler and
method guides of any field.

Evals: `evals/cases.json` (Spanish and English positives per skill,
negatives); fixtures are built by `evals/make_fixtures.py`.
