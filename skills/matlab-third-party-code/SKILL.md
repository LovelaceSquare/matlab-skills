---
name: matlab-third-party-code
description: How to use a toolbox or someone else's MATLAB code, from its help and source to name clashes and licence. Use before calling unknown code.
---

# Using MATLAB code you did not write

A call written from memory is often from another release, another
toolbox or another author's function of the same name. MATLAB can tell
you what is installed here and what a function expects: ask it before
writing the call. Checked on R2024a.

## 1. What is on this machine

```matlab
ver                                      % products and versions installed
license('test', 'Statistics_Toolbox')    % 1 when the licence allows it
which -all name                          % every file answering to that name, in order
exist('name')                            % 2 file, 5 built-in, 6 P-file, 0 nothing
```

- Installed is not licensed, and licensed is not installed: check both.
  `license('test', ...)` takes the feature name (`Statistics_Toolbox`,
  `Signal_Toolbox`, `Optimization_Toolbox`); the product title raises
  an error.
- `ver` prints over a hundred lines on a full install; ask for one
  product (`ver('stats')`) or filter the list.
- A folder with a `Contents.m` whose second line is
  `% Version 2.3 01-Jan-2020` answers to `ver('foldername')` and
  `help foldername`: that is how to read the version of code that is not
  from MathWorks. Take the output (`v = ver('foldername'); v.Version`);
  printed, it comes after the whole MATLAB banner.

## 2. Which function will run

`which -all name` lists the candidates; the first line is the one called,
the rest carry `% Shadowed`. Adding a downloaded folder to the path can
put its `pca.m` in front of the toolbox `pca` for every later call, with
a different argument order and no error until the outputs are wrong.

- Run `which -all` on each function of the package before and after
  `addpath`, and say what became shadowed.
- Add a folder to the end (`addpath(folder, '-end')`) when its names
  clash with functions other code relies on, and remove it afterwards
  (`rmpath`). No `savepath`.
- A variable named like a function shadows it too: after `mean = 3`,
  `mean(x)` indexes the variable. Most calls then fail with `Index
  exceeds the number of array elements`, some with `Array indices must
  be positive integers`, and `mean(1)` returns 3 with no error at all.
  `which mean` answers "mean is a variable".
- Code in a package folder (`+pkg`) is called as `pkg.name`; code in a
  class folder (`@cls`) runs only for inputs of that class.

## 3. What it expects

```matlab
help name                    % the header of the file that will run
type name                    % its source
nargin('name'), nargout('name')
```

- `help` shows the header of the first match and lists the others under
  "Other uses of". Read the one you will call.
- Read the source for what the help leaves out: defaults, whether data is
  centred or scaled inside, the orientation it assumes (samples in rows
  or columns), what it does with `NaN`, the convergence test and its
  iteration limit, which random numbers it draws.
- Built-in functions have no source (`'svd' is a built-in function`) and
  P-files (`exist` returns 6) cannot be read: rely on their documentation
  and on tests.
- Run the author's own example first, unchanged. If it does not give the
  result they show, stop there: the release, a missing dependency or a
  shadowed name is the cause, and your data would only hide it.
- Then run it on a small case with a known answer before the real data.

## 4. What it depends on

```matlab
[files, products] = matlab.codetools.requiredFilesAndProducts('main.m');
{products.Name}
```

This lists the toolboxes and the other files a function needs, without
running it. A function that calls another by a name built at run time
(`feval`, `eval`, `str2func`) escapes the analysis. MEX files (`.mexw64`,
`.mexa64`, `.mexmaci64`) run only on the platform they were compiled for.

## 5. Whose it is

Before copying, adapting or redistributing code that is not the person's:

- Find its licence: a `LICENSE` or `license.txt` in the folder, a notice
  in the file headers, the page it was downloaded from.
- No licence found means no permission to redistribute. Using it locally
  is one thing; shipping it inside the person's toolbox is another.
- Tell the person what the licence allows and requires (keep the notice,
  cite, share alike, no commercial use) before any of it goes into code
  they will publish. The choice is theirs.
- Keep the author's header and notice in any file you adapt, and add a
  line saying what was changed.
- Record the source, version and date of download next to the code, and
  the reference the author asks to be cited.

## 6. What to hand back

For each outside function used: where it came from and its version, the
file that actually ran (`which`), what it shadowed, the toolboxes it
needs, its licence, and the result of the author's example on this
machine.
