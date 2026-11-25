# Common MATLAB errors: cause and check

| Message (start) | Usual cause | Check or fix |
|---|---|---|
| `Undefined function or variable 'x'` / `Unrecognized function or variable 'x'` | typo; file not on the path or not in the current folder; a toolbox function without the toolbox; a script variable used inside a function | `which x`, `exist('x')`, `ver`; pass the variable as an argument |
| `Undefined function 'f' for input arguments of type 'double'` | `f` exists only for another class (a table method called on a matrix) or in a toolbox that is missing | `which -all f`; convert the input (`table2array`, `double`) |
| `Arrays have incompatible sizes for this operation` / `Matrix dimensions must agree` | element-wise operation on arrays whose sizes don't match or broadcast | `size(a)`, `size(b)`; a row where a column was meant (`x(:)`, `x.'`) |
| `Incorrect dimensions for matrix multiplication` | `*` where `.*` was meant, or a transposed operand | inner dimensions of `A*B` agree: `size(A,2) == size(B,1)` |
| `Index exceeds the number of array elements` / `Index in position 2 exceeds array bounds` | loop limit wrong; an empty result from `find` or a filter | `numel`, `size`; guard empty results |
| `Unable to perform assignment because the size of the left side is …` | assigning a vector into a scalar slot, or a row into a column | preallocate with the right size; check the shape of the right side |
| `Array indices must be positive integers or logical values` | index 0, a negative or fractional index (`x(i/2)`), a variable named like a function (`sum = …`) | check why the index is invalid; `clear sum` and rename |
| `Index exceeds the number of array elements. Index must not exceed 1.` on a function call | a variable named like the function (`mean = 3`, then `mean(x)`) | `which name` says "is a variable"; rename it |
| `Dot indexing is not supported for variables of this type` | `.field` on a non-struct; `load` returned a struct and the field name differs | `class(v)`, `fieldnames(S)` |
| `Conversion to double from cell is not possible` | a cell array (text columns from `readcell`/`readtable`) used as numbers | `cell2mat`, `str2double`, or import with numeric types |
| `Error using readtable … Unable to find or open` | relative path from the wrong folder; missing file or insufficient access | `pwd`, `isfile(f)`, absolute path from `mfilename('fullpath')` |
| `Out of memory` / `Requested array exceeds maximum array size` | a full `n x n` matrix by mistake (e.g. `X*X'` on many rows), `kron` of large factors, an array grown inside a loop | work out the size before the step (rows x columns x 8 bytes) against free memory; `'econ'` SVD; `single`; process in blocks |
| `License checkout failed. License Manager Error -4` / `-15` | -4: all seats in use; -15: the licence server unreachable (VPN off, or commands run in a sandbox without network) | retry later; check the network and the VPN; `license('inuse')` |
| MATLAB closes with `There is insufficient memory for the Java Runtime Environment` / `Fatal Java Exception`, exit code 3 | the whole machine is out of memory, often because of other programs, not this code | look at free memory and what else is running before blaming the script; tell the person; run again when memory is free |
| `Warning: Matrix is close to singular or badly scaled. RCOND = …` | collinear columns, more unknowns than the data supports, a zero column | use SVD or `pinv`, fewer terms, drop constant columns |
| `Warning: Polynomial is badly conditioned` (from `polyfit`) | x values far from zero or a high degree | the centred and scaled form `[p, S, mu] = polyfit(x, y, n)` with `polyval(p, x, S, mu)`; a lower degree |
| `Warning: Rank deficient, rank = …` | `\` on a matrix without full column rank | same as above; the result is not unique |
| `Error: File: x.m Line: N Column: M … Function definitions in a script must appear at the end of the file` | local functions above script code in releases requiring them at the end | move them to the end if required by the release |
| `Invalid use of operator` / `Parse error` | a missing `end`, unbalanced brackets or quotes, `"` vs `'` mixed in an old release | the line and column in the message; `checkcode('x.m')` lists problems |

`checkcode('file.m')` (the Code Analyzer) finds many of these without
running the code.
