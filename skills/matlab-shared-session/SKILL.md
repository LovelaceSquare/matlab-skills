---
name: matlab-shared-session
description: How to work inside the MATLAB the person already has open, on their own variables. Use when the work is on what they have loaded.
---

# Working inside the person's open MATLAB

A `-batch` run (matlab-run skill) is a separate process: it cannot see
the variables or figures in the window the person has open. To work on
what they already have loaded, they share their session and you connect
to it. Measured on R2024a: connecting takes about half a second and each
call answers in hundredths of a second, with variables kept between calls.

## 1. Connect

Ask the person to type this in their MATLAB:

```matlab
matlab.engine.shareEngine
```

Then connect from Python. The engine package has to match the release
(`pip install "matlabengine==24.1.*"` for R2024a; each release supports
only some Python versions, so check before installing). Install it in a
virtual environment, not in the person's system Python.

```python
import io, matlab.engine
names = matlab.engine.find_matlab()          # () when nothing is shared
eng = matlab.engine.connect_matlab(names[0])
```

- An empty `find_matlab()` means no session is shared: the command above
  has not been typed, or that MATLAB runs as another user.
- With several names, ask which window is the one to use.
- Sharing ends when that MATLAB closes. `eng.quit()` on a shared session
  only disconnects you.

## 2. Look before touching

```python
eng.who()                                    # their variable names
out = io.StringIO()
eng.eval("whos", nargout=0, stdout=out)      # sizes and classes
print(out.getvalue())
x = eng.workspace['X']                       # copies X to Python
```

- Text MATLAB prints goes to Python's standard output, mixed with your
  own prints. Pass `stdout=` (and `stderr=`) to hold it in a variable.
- `eng.workspace['X']` copies the whole array across. For a large array
  ask for `size`, a summary or a slice computed in MATLAB instead.
- A MATLAB error arrives as a Python exception
  (`matlab.engine.MatlabExecutionError`) carrying the message.

## 3. It is their workspace

Whatever runs through `eng.eval` runs as if they had typed it.

- No `clear`, `clearvars`, `close all`, `clc`, `cd`, `rng`, `format`,
  `addpath`/`rmpath` or `warning off` unless they asked for it. Each one
  changes something they will meet later without knowing why.
- No assignment to a name that already exists. Check with
  `eng.eval("exist('name','var')", nargout=1)` and pick another. Changing
  one of their variables needs their request in those words.
- A statement with no assignment (`eng.eval("1+1;")`) writes `ans` in
  their workspace. Assign to a name of your own, or call the function
  through the engine (`eng.size(x)`) so the value comes back to Python.
- Put your code in functions, which have their own workspace, and return
  only what was asked for. Variables you do leave behind get a prefix you
  tell them about, and you list them at the end.
- Figures you create open on their screen. Create them with
  `'Visible','off'`, save them to a file, and delete them; leave their
  figures alone.

## 4. What changes compared with a batch run

- Anything that waits for a person now waits in their window: `input`,
  `keyboard`, a bare `pause`, dialogs. Your call does not return until
  they answer.
- A long computation holds their MATLAB busy; they cannot type meanwhile.
  Tell them before starting one, or run it in a separate `-batch` process
  on a saved copy of the data.
- An error in your code does not close their session, but a crash of
  MATLAB does lose their unsaved workspace. Before anything heavy (memory
  section of the matlab-run skill), suggest they `save` their workspace
  to a new file.
- The current folder and the path are theirs: use full paths rather than
  `cd`.

## 5. What to hand back

What you read, what you ran, the variables and files you created (with
their names), and confirmation that nothing of theirs was changed, or
exactly what was and at whose request.

Without a shared session, use the matlab-run skill and files.
