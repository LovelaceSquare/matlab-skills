---
name: matlab-figures
description: How to make MATLAB figures at the size and format a journal asks, and check the exported file. Use for figures for papers or reports.
---

# Figures for publication in MATLAB

What is judged is the exported file at its printed size, not the figure
window. You do not see the window anyway: build the figure hidden, export
it, and look at the file (matlab-run skill). Sizes below were measured on
R2024a.

## 1. Ask for the target before drawing

Width in cm (one column, one and a half, two), accepted formats, minimum
resolution, font family and smallest font size come from the journal's
current guide for authors, or from the person. Without them, say which
defaults you used: 8.5 cm wide, 8 pt Arial, vector PDF plus 600 dpi TIFF.

## 2. Build at final size

Set the physical size first, draw, then set fonts last so they apply to
everything.

```matlab
f = figure('Visible', 'off', 'Units', 'centimeters', 'Position', [2 2 8.5 6.5], 'Color', 'w');
tl = tiledlayout(f, 1, 2, 'TileSpacing', 'compact', 'Padding', 'compact');
ax = nexttile(tl);
plot(ax, x, y, 'LineWidth', 0.75);
xlabel(ax, 'Wavenumber (cm^{-1})');  ylabel(ax, 'Absorbance (a.u.)');
fontname(f, 'Arial');  fontsize(f, 8, 'points');
```

- A figure drawn large and shrunk later ends with unreadable text: fonts
  scale with the picture. Draw at the printed size.
- `fontname` and `fontsize` exist from R2022a. On older releases set
  `FontName` and `FontSize` on axes, labels and legends.
- Every axis carries the quantity and its unit. The default TeX
  interpreter handles `cm^{-1}` and `\lambda`; with
  `'Interpreter','latex'` the syntax and the font change, so look at the
  result.
- Colour is not the only carrier of meaning: add markers or line styles,
  and check the figure in greyscale. A palette safe for colour-blind
  readers (Okabe-Ito):
  `[0 0 0; 230 159 0; 86 180 233; 0 158 115; 240 228 66; 0 114 178; 213 94 0; 204 121 167]/255`.
  Its yellow (the fifth) hardly shows on white: skip it for points and
  thin lines, or give the markers a dark edge.
- Panels of one figure share font sizes and line widths; panel letters
  go in the same corner of each.

## 3. Export: two functions, two behaviours

```matlab
exportgraphics(f, 'fig2.pdf', 'ContentType', 'vector');
exportgraphics(f, 'fig2.tif', 'Resolution', 600);
```

`exportgraphics` crops to the content. An 8.5 x 6.5 cm figure came out
as 7.44 x 6.12 cm: the file is narrower than the size you set, by an
amount that depends on labels and margins. When the journal fixes the
width, either measure the file and adjust the figure, or use `print`,
which keeps the page you define:

```matlab
set(f, 'PaperUnits', 'centimeters', 'PaperSize', [8.5 6.5], 'PaperPosition', [0 0 8.5 6.5]);
print(f, '-dtiff', '-r600', 'fig2.tif');     % 8.50 x 6.50 cm
print(f, '-dpdf', '-vector', 'fig2.pdf');    % exact page, fonts not embedded (below)
```

- **For PDF, `print` does not embed the fonts.** Its PDF had the exact
  page (8.50 x 6.00 cm) but `pdffonts` showed Helvetica, not embedded,
  in place of Arial; journals reject that. `exportgraphics` embeds the
  font (ArialMT) and crops the page (7.97 x 5.57 cm for 8.5 x 6). So for
  a vector PDF use `exportgraphics`, measure the page and enlarge the
  figure by the difference; keep `print` for TIFF and PNG of exact size.
- Vector (PDF, EPS) for lines and text; raster (TIFF, PNG) at the
  resolution asked for images, or when a plot with very many points makes
  the vector file huge.
- Options differ between releases (a `'Padding'` option of
  `exportgraphics` is rejected in R2024a). Read `help exportgraphics` in
  the install before using an option from memory.
- Both functions overwrite an existing file silently; choose a new name
  (matlab-run skill, "What belongs to the person").

## 4. Measure the file

```matlab
i = imfinfo('fig2.tif');
switch lower(i.ResolutionUnit)
    case 'inch',  wcm = i.Width / i.XResolution * 2.54;
    case 'meter', wcm = i.Width / i.XResolution * 100;    % PNG stores pixels per metre
end
```

- TIFF reports resolution per inch, PNG per metre (300 dpi shows as
  11811). With no resolution in the file, the physical size is unknown;
  do not compute one.
- For PDF, check page size and that fonts are embedded with a PDF tool
  (`pdfinfo`, `pdffonts`) when one is installed; otherwise say it was not
  checked.

## 5. Look at it

Open the exported image (convert a PDF or TIFF page to PNG if needed) and
check at the printed size: nothing clipped at the edges, tick labels not
overlapping, legend not covering data, units present, smallest text
legible, panels aligned. Then fix and export again.

## 6. What to hand back

The files with their measured width, height and resolution, the script
that draws them (kept with the data so the figure can be redone), the
image you looked at, and anything the journal asks that you could not
verify.
