---
name: matlab-data-files
description: How to read CSV, Excel and .mat files in MATLAB without changing the numbers, and write results safely. Use for loading or saving data.
---

# Data in and out of MATLAB

MATLAB's import functions guess, and a wrong guess does not raise an
error: it returns a table of the right shape with the wrong content. The
behaviour below was checked on R2024a.

## 1. Look at the file before parsing it

Read the first lines as text and the size on disk before choosing a
function:

```matlab
txt = fileread(f);  disp(txt(1:min(400, end)));
d = dir(f);  d.bytes
```

What to read off: the separator (`,` `;` tab), the decimal mark, whether
the first row is a header and whether that header is text or numbers,
how many lines come before the data, and whether accented letters show
correctly (encoding).

## 2. Reading text files

| The file has | What happens by default | Call that reads it right |
|---|---|---|
| A header of numbers (an axis: `id,4000,4010.5,...`) | the header is taken as data: names become `Var1, Var2...` and the table has one row too many. `'VariableNamingRule','preserve'` alone does not change this | `readtable(f, 'ReadVariableNames', true, 'VariableNamingRule', 'preserve')`, then `str2double(T.Properties.VariableNames(2:end))` |
| Numbers only, first row is the axis | `readmatrix` returns the axis as row 1 of the data | `M = readmatrix(f); ax = M(1,:); X = M(2:end,:);` |
| `;` separator and decimal comma | the `;` is detected, the comma is not: every numeric column arrives as text (`class` is `cell`), no error | `o = detectImportOptions(f, 'Delimiter', ';', 'DecimalSeparator', ',', 'ReadVariableNames', true, 'VariableNamingRule', 'preserve'); T = readtable(f, o);` |
| Decimal comma in the header too | names stay as text with the comma (`'4037,74'`) | `str2double(strrep(names, ',', '.'))` |
| Text header with spaces, units or symbols | without `preserve`, names are rewritten into valid identifiers (`x4000_00`) | `'VariableNamingRule', 'preserve'`, and index columns by position or `T.("name")` |
| Mixed text and numbers in a column | the column becomes text, or the text cells become `NaN` | `readcell(f)` and convert each column yourself |
| Lines of metadata above the table | detection may start in the wrong line | `'NumHeaderLines', k`, or `o.DataLines` and `o.VariableNamesLine` |

`DecimalSeparator` is an argument of `detectImportOptions`, not a
property you can read back from the options object. To see what was
detected, inspect `o.Delimiter`, `o.Encoding`, `o.VariableTypes`,
`o.VariableNamesLine` and `o.DataLines`.

## 3. Reading Excel

```matlab
sheetnames(f)
T = readtable(f, 'Sheet', 'Spectra', 'Range', 'A1:Z200', 'VariableNamingRule', 'preserve');
```

Name the sheet and, when the sheet holds more than the table, the range.
Merged header cells, dates and cells with formula errors are where
imports go wrong; look at those columns after reading. A workbook open in
Excel may be locked.

## 4. Reading .mat

```matlab
whos('-file', f)             % names, sizes and classes without loading
S = load(f);  X = S.X;       % into a struct
m = matfile(f);  block = m.X(1:100, :);   % part of a large variable
```

- `load(f)` with no output drops every variable of the file into the
  workspace and silently replaces any with the same name. Load into a
  struct.
- The first bytes of the file say the format: `MATLAB 5.0 MAT-file` (v7
  and earlier) or `MATLAB 7.3 MAT-file` (HDF5). Partial reads with
  `matfile` are efficient only on v7.3.
- A variable saved from an object needs its class on the path; without
  it `load` warns and returns something unusable.

## 5. Check what arrived

Before any computation, and in what you report:

- `size`, and the `class` of each column (`varfun(@class, T)`): a `cell`
  where numbers were expected means the decimal mark or a stray text cell;
- `nnz(isnan(X))` and where the gaps are: missing in the file, or made by
  the import;
- the first and last value of the axis and its direction;
- the first and last row against the lines of the file read in section 1;
- one plot of the data, saved and looked at (matlab-run skill).

## 6. Writing

Outputs go where the person said results go, under names that do not
exist yet (matlab-run skill, "What belongs to the person").

```matlab
writetable(T, out);                          % csv
writematrix([ax; X], out);                   % first row = axis
save(out, 'P', 'mu', 'ax', '-v7');           % readable with scipy.io.loadmat
save(out, 'X', '-v7.3');                     % over 2 GB, or partial reads; HDF5
```

- `writetable`, `writematrix` and `save` replace an existing file without
  warning. Test `isfile(out)` first.
- `writetable` to an existing `.xlsx` sheet writes over the top-left cells
  and leaves the rest: a shorter table leaves old rows underneath, and
  reading it back returns both. To replace a sheet you created, use
  `'WriteMode', 'overwritesheet'`. In the person's workbook, write to a
  new file.
- `writematrix` writes 15 significant digits: a round trip through CSV
  matches to about 1e-14 relative, not bit for bit. `NaN` is written as
  the text `NaN`.
- `save` without a version flag uses the person's preference; say `-v7`
  or `-v7.3` when another program will read the file.
- CSV for someone else: agree separator, decimal mark and encoding, and
  check accented text after writing.

## 7. Read back what you wrote

Read the file again and compare: `isequaln` for `.mat`; for CSV the same
size, the same positions of `NaN`, and values within a tolerance that
fits the digits written. Report the file, its size and the comparison.
