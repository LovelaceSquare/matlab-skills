---
name: matlab-writing-code
description: How to write MATLAB functions that last, with help header, input checks, clear errors and a licence. Use when writing code to keep.
---

# Writing MATLAB code that will be kept

## 1. Two questions before the first line

- **How strict?** Ask whether this is code to keep (a function others
  will call, a toolbox, something to publish) or a quick test. The rules
  below are for code that stays. In a project that already has its own
  written conventions (a coding standard, a style guide, a contributing
  file), read them first: they win over this guide.
- **Which licence?** At the start of every new project ask the person
  which licence the code will carry, even if it is not going to be shared
  yet. Do not pick one for them and do not write a licence line without
  their answer. Until they decide, the header says so (section 2).

## 2. The help header

`help name` and `lookfor` read the comment block right under the
`function` line. Every function that stays has all four parts:

```matlab
function [C, S, info] = fitModel(X, k, opts)
%FITMODEL  Fit a k-component bilinear model to X by alternating least squares.
%
%   [C, S] = FITMODEL(X, k)
%   [C, S, info] = FITMODEL(X, k, Name, Value)
%
%   Inputs
%     X        n-by-m double   data, one sample per row; no NaN
%     k        scalar integer  number of components, 1 <= k <= min(n, m)
%     maxIter  scalar          iteration limit (default 500)
%     tol      scalar          relative change in fit to stop (default 1e-8)
%
%   Outputs
%     C     n-by-k double   contributions
%     S     m-by-k double   profiles, unit length
%     info  struct          .iter, .converged, .lof (percent)
%
%   Example
%     X = rand(20, 3) * rand(3, 50);
%     [C, S, info] = fitModel(X, 3);
%     info.lof
%
%   Reference: Author, Journal year, volume, pages. doi:...
%   Author: Name, affiliation, year.   Licence: (as chosen by the author)
```

1. **H1 line and syntax**: the name in capitals and one sentence saying
   what it does, then every way of calling it.
2. **Inputs and outputs**: size, type, units and orientation of each;
   defaults for what is optional.
3. **An example that runs** when pasted as it is, with nothing loaded.
   Run it yourself before handing the file over.
4. **Author, licence and citation**: who wrote it and when, the licence
   the person chose, and the paper to cite for the method.

The comment line holding only `%` keeps the block together; a truly
empty line ends what `help` prints.

## 3. Checks at the door

```matlab
arguments
    X (:,:) double {mustBeFinite}
    k (1,1) double {mustBeInteger, mustBePositive}
    opts.maxIter (1,1) double {mustBePositive} = 500
    opts.tol (1,1) double {mustBePositive} = 1e-8
end
```

The `arguments` block (R2019b on) checks size, class and value, sets
defaults and gives name-value options, and its error names the argument.
Add by hand the checks that relate inputs to each other
(`k <= min(size(X))`).

## 4. Errors and warnings with a name

```matlab
error('fitModel:rankDeficient', 'X has rank %d, fewer than k = %d.', r, k);
warning('fitModel:notConverged', 'Stopped at %d iterations, change %.2g.', it, d);
```

An identifier (`package:what`) lets the caller catch one case and lets a
person switch one warning off without silencing the rest. The message
says what was found and the value, not only that something failed. A
function does not print with `disp` to report a problem and does not
open a dialog: it raises, and the caller decides.

## 5. The body

- **Comments say why**, the code says what: the reason for a choice, the
  source of a formula, a step that looks wrong but is not.
- **No bare numbers**: a tolerance, a limit or a window width is a named
  constant or an option with a default stated in the header.
- **Preallocate** what a loop fills (`zeros(n, 1)`); an array grown one
  element per pass is slow and is how loops run out of memory.
- **Short functions with one job.** Reading a file, computing and
  plotting are three functions; the computing one takes arrays, not file
  names, and draws nothing.
- **No hidden state**: no `global`, no `eval`, no `assignin`/`evalin`,
  no `cd`, no `clear` or `close all` inside functions. What a function
  needs comes in as arguments; what it produces goes out as outputs.
- **Paths from the file, not from the machine**:
  `root = fileparts(mfilename('fullpath'))` and `fullfile(root, ...)`;
  no `C:\Users\...` in code.
- **No names of existing functions** for variables (`sum`, `mean`, `i`,
  `length`, `pca`).
- **Randomness is an input**: take a seed or a stream as an option and
  record it in the output, so a result can be repeated.
- The file is named after its first function. Local functions go at the
  end of the file. The folder gets another name than the function, or
  `help` mixes the two.

## 6. Before handing it over

```matlab
msgs = checkcode('fitModel.m');  {msgs.message}     % Code Analyzer, without running
help fitModel                                        % does the header read well
```

- `checkcode` clean, or each remaining message explained.
- The header example run as written, in a fresh session (matlab-run
  skill), so nothing depends on variables that happened to exist.
- A small test with a known answer saved next to the code
  (`tests/test_fitModel.m`): a case built from known factors, one edge
  case, one input that has to be refused. `runtests('tests')` does not
  put the code's folder on the path: `addpath` it for the run, or every
  test fails with `Undefined function`.
- In `assert(cond, msg)` a message containing `:` is taken for an
  identifier and raises its own confusing error. Write
  `assert(cond, 'pkg:what', 'text %s', value)`.
- Releases: say the oldest release the code needs when it uses recent
  functions (`arguments` R2019b, `exportgraphics` R2020a, `fontname`
  R2022a).

## 7. What to hand back

The files written, the result of `checkcode` and of the tests, the
example output, the licence question if it is still open, and anything
in the rules above that was left out and why.
