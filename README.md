# Help your AI assistant work in MATLAB

Seven short guides that an AI assistant reads before it works in MATLAB for you. They help it work the way a careful person would.

With them, the assistant:

- runs your code and checks whether it really worked;
- reads your data files without changing the numbers;
- makes figures at the size a journal asks for;
- uses code written by other people safely;
- writes tidy, well-explained functions;
- builds small apps with buttons and windows.

The guides are about using MATLAB well. They do not teach any scientific method. They were checked in MATLAB R2024a on Windows, and each guide says what could not be checked.

Part of [Lovelace's Square](https://lovelacesquare.org), the open home for chemometrics code, data and teaching material.

---

## The seven guides

| Guide | What it helps with |
|---|---|
| `matlab-run` | Running code without opening MATLAB's window, checking how it ended, and understanding common errors. |
| `matlab-shared-session` | Working inside the MATLAB you already have open, and leaving your variables and settings as they were. |
| `matlab-data-files` | Reading and saving CSV, Excel and `.mat` files without losing or changing data. |
| `matlab-figures` | Making figures at the right size for a paper and checking the saved file. |
| `matlab-third-party-code` | Using toolboxes and other people's code: what is installed, which function will run, and its licence. |
| `matlab-writing-code` | Writing functions with a clear help text, an example, input checks and clear error messages. |
| `matlab-app-design` | Building a small app with a clean look, and checking each screen. |

## How to use them

Each folder inside `skills/` is one guide. Its main file is `SKILL.md`, and some folders also have a `references/` folder with extra notes.

- If your AI assistant has a skills folder, copy the folders you want there.
- If it does not, give it the `SKILL.md` file of the guide you need.

They work with any AI assistant that can read files and run commands on your computer.

## Licence

MIT. See `LICENSE`. To cite these guides, see `CITATION.cff`.
