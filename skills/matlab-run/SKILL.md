---
name: matlab-run
description: How to run MATLAB code without its window, keep results between runs and check how it ended. Use when MATLAB code must be run or fixed.
---

# Running MATLAB as an agent

You have no desktop, no workspace panel and no figure windows. You have
the text MATLAB prints and the files it leaves. Everything below follows
from that. The numbers quoted were measured on R2024a on Windows.

## 1. Find it and check it answers

MATLAB is often not on PATH. Find the launcher, then confirm it starts and
the licence answers before planning any work.

```powershell
where.exe matlab
Get-ChildItem "C:\Program Files\MATLAB"          # one folder per release
& "C:\Program Files\MATLAB\R2024a\bin\matlab.exe" -batch "disp(version)"
```

On macOS the launcher is inside the app bundle
(`/Applications/MATLAB_R2024a.app/bin/matlab`); on Linux it is usually on
PATH. With several releases, use the one the project names. If nothing is
found, ask where it is.

## 2. Every run starts from nothing

`-batch` opens a new MATLAB, runs the statement and exits.

- **Starting is slow**: 10 to 80 seconds per call, the first call of the
  day the slowest. Twenty small calls cost ten minutes of waiting. Write
  one script that does the whole step and run it once.
- **Nothing survives**: variables from the previous run are gone. What the
  next step needs goes to a file (`save('step1.mat', ...)`) and the next
  script loads it.
- **The person's open MATLAB is another process**: you do not see their
  variables or figures, and they do not see yours. To work on what they
  have loaded, see the matlab-shared-session skill.

```powershell
& "C:\...\matlab.exe" -sd "C:\path\to\project" -batch "run('scripts/step1.m')" -logfile step1.log
$LASTEXITCODE
```

`-sd` sets the folder. In PowerShell a quoted path runs only after `&`,
and a `$` inside double quotes is expanded: keep the statement short and
put the code in a `.m` file. Inside the statement use single quotes for
MATLAB text and forward slashes in paths.

## 3. See what you did

- Print sizes and summaries, not whole arrays: `whos`, `size`, `class`,
  `min`/`max`, the first rows. A large array printed to the log hides the
  line you needed.
- Figures appear on the person's screen even under `-batch`
  (`DefaultFigureVisible` is `on`). Create them hidden and save them:

```matlab
f = figure('Visible', 'off');
plot(x, y);
exportgraphics(f, 'check.png', 'Resolution', 150);
```

- A script you may not edit draws on screen with its own `figure` calls.
  Hide them from outside, in the same statement:
  `-batch "set(groot,'DefaultFigureVisible','off'); theirScript"`.
- **Open the image and look at it** before saying anything about the
  result. A number that looks right does not tell you the plot is right.
- After a run, check that the expected files exist, are new and have a
  sensible size.

## 4. Memory: work it out first, then say

Before loading a large file or building a large array, estimate it:
rows x columns x 8 bytes for `double`. Compare with what is free:

```matlab
[u, s] = memory;                          % Windows only
freeGB = s.PhysicalMemory.Available / 2^30;
needGB = n * m * 8 / 2^30;
w = whos('-file', 'big.mat');  [w.bytes]  % size in memory of a .mat, before loading it
```

- If the estimate passes half of the free memory, stop and tell the
  person the numbers before running. They choose: go ahead, work in
  blocks, `single`, `sparse`, `matfile`, or another machine.
- Count the copies. `X*X'` on n samples is n x n; centring, a
  decomposition and its outputs each hold another array of the size of X.
- Over the array size limit MATLAB raises
  `MATLAB:array:SizeLimitExceeded` at once. Under it, a request that does
  not fit in RAM goes to swap and the machine stops answering. The error
  is the good case.
- On macOS and Linux `memory` does not exist; read free memory from the
  system (`vm_stat`, `free -m`).

## 5. Loops: check that nothing grows

Before running a loop that may go round many times, read its body for
anything that gets bigger on each pass:

- an array extended inside the loop (`r(end+1) = ...`, `C = [C; c]`)
  without preallocation;
- a history that keeps the whole result of every iteration when only the
  last, or one number per iteration, is needed;
- figures or files opened and not closed (`close(f)`, `fclose(fid)`);
- a cell or struct array collecting large items.

Preallocate, keep the scalar per iteration, close what is opened. For a
long loop print progress every N passes and save intermediate results so
the run can resume; know the time limit of the command you run under.

## 6. What needs a person

- `input` fails at once under `-batch` ("Support for user input is
  required", exit code 1). `keyboard` is skipped without a word and the
  run goes on to exit code 0: a script that stopped there to let the
  person inspect will not stop.
- `pause` without a time does not wait: it prints a warning and goes on.
  A script that relied on it to let the person look will run past.
- File pickers, dialogs and `uiwait` open on the person's screen and wait
  for a click that may not come. Replace them with arguments or files, or
  leave that step to the person.
- Parallel pools take time to start and may need a licence; check before
  relying on them.

## 7. Read how it ended

- An uncaught error prints its message and `Error in name (line N)`,
  and the exit code is 1. `Error using ...` comes first only when a
  function raised the error; an operator error (sizes, indices) has no
  such line, so search the log for `Error in`. In the `-logfile`, errors
  are wrapped in `{ }` and warnings in `[ ]`. Start at the first frame
  in the project's own code.
  Common messages and their usual cause: [errors](references/errors.md).
- A warning prints `Warning: ...` and the exit code stays 0. Read the log
  for warnings; do not silence them with `warning off`.
- A script that catches its own errors also exits 0. Exit code 0 means
  MATLAB ended, not that the result is right.

To get the full report from a script:

```matlab
try
    main();
catch ME
    fprintf(2, '%s\n', getReport(ME, 'extended', 'hyperlinks', 'off'));
    exit(1);
end
```

## 8. What belongs to the person

- **Where results go**: the first time in a project, ask where outputs
  should be written and keep to it. Intermediate files go to a separate
  scratch folder (`tempname`), not among their data.
- **No overwriting unless asked in those words.** `save`, `writematrix`,
  `writetable` to CSV, `exportgraphics` and `print` all replace an
  existing file without a word. Check first and pick another name:

```matlab
if isfile(out), error('run:exists', '%s already exists', out); end
```

- Their data and scripts are read, not rewritten.
- No `savepath`, no changes to `startup.m` or preferences: add folders to
  the path for the run only.
- A file open in Excel or in their editor may be locked or hold unsaved
  work.

## 9. What to hand back

The command and the release used, the numbers that matter, the warnings,
the files written and where, and the pictures you looked at. Say what you
could not check.
