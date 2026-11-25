"""Builds evals/fixtures/ for the MATLAB plugin's skill evals.

Run from anywhere: python evals/make_fixtures.py  (needs numpy and scipy).
All data are synthetic (Gaussian bands, invented sample names) and carry on
purpose the traps the cases' rubrics check: a transposed std that breaks a
script at line 42, rows with NaN, a script that opens a figure, and a
semicolon/decimal-comma CSV in Windows-1252. Deterministic: same files on every run
(the .mat header timestamp is overwritten with a fixed text).
"""
import csv
from pathlib import Path

import numpy as np
import scipy.io

OUT = Path(__file__).resolve().parent / "fixtures"
OUT.mkdir(exist_ok=True)


def rng(seed):
    return np.random.default_rng(seed)


def gauss(x, c, w, h=1.0):
    return h * np.exp(-0.5 * ((x - c) / w) ** 2)


def fmt(v, nd=5):
    return "" if np.isnan(v) else f"{v:.{nd}f}"


def write_csv(name, header, rows, sep=",", decimal=".", encoding="utf-8"):
    with open(OUT / name, "w", newline="", encoding=encoding) as f:
        w = csv.writer(f, delimiter=sep)
        w.writerow(header)
        for r in rows:
            w.writerow([x.replace(".", decimal) if decimal != "." else x for x in r])


def write_text(name, text):
    (OUT / name).write_text(text.lstrip("\n"), encoding="utf-8", newline="\n")


def savemat(name, data):
    p = OUT / name
    scipy.io.savemat(p, data, do_compression=True, oned_as="column")
    raw = bytearray(p.read_bytes())
    head = b"MATLAB 5.0 MAT-file, synthetic fixture for Ada skill evals"
    raw[:116] = head.ljust(116, b" ")
    p.write_bytes(bytes(raw))


# ---------------------------------------------------------------- spectra
def nir_axis(m=300):
    return np.linspace(10000, 4000, m)          # cm-1, decreasing (FT-NIR export)


def nir_set(n, seed, m=300, moisture=None):
    """NIR spectra of a food powder: water, protein, carbohydrate + scatter."""
    r = rng(seed)
    x = nir_axis(m)
    water = gauss(x, 5180, 90, 1.0) + gauss(x, 6900, 160, 0.45)
    prot = gauss(x, 4600, 120, 0.6) + gauss(x, 4850, 80, 0.3) + gauss(x, 5950, 140, 0.2)
    carb = gauss(x, 4400, 150, 0.7) + gauss(x, 8300, 300, 0.15) + gauss(x, 6800, 250, 0.2)
    if moisture is None:
        moisture = r.uniform(8, 16, n)
    pr = r.uniform(10, 14, n)
    C = np.column_stack([moisture / 10, pr / 10, 1.6 - moisture / 30 - pr / 40])
    S = np.vstack([water, prot, carb])
    pure = C @ S
    a = r.normal(0.25, 0.06, (n, 1))
    b = r.normal(1.0, 0.08, (n, 1))
    slope = r.normal(0, 0.03, (n, 1)) * (x - 7000) / 3000
    X = a + b * pure + slope + r.normal(0, 0.002, (n, m))
    return x, X, moisture, pr


def ir_axis_asc(m=600):
    return np.linspace(650, 4000, m)            # FTIR-ATR, stored ascending


def oil_ir(n, seed, m=600):
    r = rng(seed)
    x = ir_axis_asc(m)
    s1 = gauss(x, 1745, 15, 1.0) + gauss(x, 2925, 25, 0.8) + gauss(x, 2855, 20, 0.6) + gauss(x, 1160, 30, 0.5)
    s2 = gauss(x, 3010, 12, 0.3) + gauss(x, 1655, 12, 0.15) + gauss(x, 720, 10, 0.3)
    s3 = gauss(x, 965, 10, 0.25) + gauss(x, 1460, 20, 0.3) + gauss(x, 1377, 12, 0.15)
    grp = np.repeat(["Arbequina", "Picual", "Hojiblanca", "Cornicabra"], n // 4)
    shift = {"Arbequina": (0.9, 1.2), "Picual": (1.0, 0.7), "Hojiblanca": (1.1, 1.0), "Cornicabra": (0.95, 0.85)}
    c2 = np.array([shift[g][0] for g in grp]) + r.normal(0, 0.05, n)
    c3 = np.array([shift[g][1] for g in grp]) + r.normal(0, 0.08, n)
    X = np.outer(r.normal(1, 0.02, n), s1) + np.outer(c2, s2) + np.outer(c3, s3)
    X += r.normal(0, 0.003, (n, m)) + r.normal(0.02, 0.005, (n, 1))
    return x, X, grp


# ---------------------------------------------------------------- MATLAB fixtures
def run_script():
    """analisis_nir.m + nir_lote3.csv: runs to the end but warns (2 NaN spectra)
    and opens a figure with the default visibility, so a careless headless run
    pops a window on the owner's screen."""
    x, X, _, _ = nir_set(32, 31)
    X[[8, 21], 120:123] = np.nan
    rows = [[str(i + 1)] + [fmt(v) for v in X[i]] for i in range(len(X))]
    write_csv("nir_lote3.csv", ["muestra"] + [f"{v:.2f}" for v in x], rows)
    write_text("analisis_nir.m", r"""
% analisis_nir.m  -  SNV + PCA de los espectros NIR del lote 3
% Lee nir_lote3.csv (primera fila: numeros de onda en cm-1) y guarda la
% figura de scores en scores_lote3.png junto al script.

root = fileparts(mfilename('fullpath'));
T = readmatrix(fullfile(root, 'nir_lote3.csv'), 'NumHeaderLines', 0);
wn  = T(1, 2:end);
X   = T(2:end, 2:end);
ids = T(2:end, 1);

bad = any(isnan(X), 2);
if any(bad)
    warning('analisis:nan', '%d espectros con NaN eliminados (muestras %s)', ...
        nnz(bad), mat2str(ids(bad)'));
    X = X(~bad, :);
    ids = ids(~bad);
end

% SNV fila a fila y centrado por columnas
Xs = (X - mean(X, 2)) ./ std(X, 0, 2);
Xc = Xs - mean(Xs, 1);

[U, S, V] = svd(Xc, 'econ');
ev = diag(S).^2;
expl = 100 * ev / sum(ev);
fprintf('Espectros usados: %d de %d, %d variables\n', size(X, 1), size(T, 1) - 1, numel(wn));
fprintf('Varianza explicada PC1-PC4: %s %%\n', mat2str(round(expl(1:4)', 1)));

A = 2;
scores = U(:, 1:A) * S(1:A, 1:A);
t2 = sum(scores.^2 ./ (ev(1:A)' / (size(X, 1) - 1)), 2);
[~, k] = max(t2);
fprintf('Muestra con mayor T2 (A=%d): %d (T2 = %.2f)\n', A, ids(k), t2(k));

figure;
plot(scores(:, 1), scores(:, 2), 'o');
xlabel(sprintf('PC1 (%.1f %%)', expl(1)));
ylabel(sprintf('PC2 (%.1f %%)', expl(2)));
saveas(gcf, fullfile(root, 'scores_lote3.png'));
disp('Figura guardada en scores_lote3.png');
""")


def error_script():
    """preprocess_raman.m: line 42 divides an n-by-m matrix by a transposed
    1-by-n std, 'Arrays have incompatible sizes for this operation'. Once fixed,
    the 6th-degree polyfit on the raw cm-1 axis warns 'badly conditioned'."""
    x = np.linspace(400, 1800, 700)
    r = rng(42)
    n = 24
    pure = gauss(x, 1001, 5, 1.0) + gauss(x, 1450, 12, 0.5) + gauss(x, 1655, 10, 0.6) + gauss(x, 850, 8, 0.3)
    bg = np.outer(r.uniform(2, 4, n), np.exp(-(x - 400) / 900)) + np.outer(r.uniform(0.2, 0.5, n), ((x - 1100) / 700) ** 2)
    X = bg + np.outer(r.uniform(0.6, 1.2, n), pure) + r.normal(0, 0.01, (n, len(x)))
    rows = [[f"R{i + 1:02d}"] + [fmt(v, 4) for v in X[i]] for i in range(n)]
    write_csv("raman_serie.csv", ["sample"] + [f"{v:.2f}" for v in x], rows)
    lines = [
        "% preprocess_raman.m",
        "% Baseline correction (polynomial) + SNV + mean centring of the Raman",
        "% series in raman_serie.csv. Writes raman_preprocessed.csv next to the script.",
        "%",
        "% Author: lab group, 2026",
        "",
        "root = fileparts(mfilename('fullpath'));",
        "% First row: Raman shift (cm-1); first column: sample names.",
        "C = readcell(fullfile(root, 'raman_serie.csv'));",
        "names = C(2:end, 1);",
        "wn = cell2mat(C(1, 2:end));          % 1 x m axis",
        "X = cell2mat(C(2:end, 2:end));       % n x m spectra",
        "",
        "[n, m] = size(X);",
        "fprintf('Loaded %d spectra x %d points (%.0f-%.0f cm-1)\\n', n, m, wn(1), wn(end));",
        "",
        "% ---- 1. Polynomial baseline (degree 6, iterative clipping) ----",
        "deg = 6;",
        "nIter = 5;",
        "B = zeros(n, m);",
        "for i = 1:n",
        "    y = X(i, :);",
        "    for it = 1:nIter",
        "        p = polyfit(wn, y, deg);",
        "        b = polyval(p, wn);",
        "        y = min(y, b);",
        "    end",
        "    B(i, :) = b;",
        "end",
        "Xb = X - B;",
        "",
        "% ---- 2. Quick look at the corrected range ----",
        "fprintf('Corrected intensity range: %.3f to %.3f\\n', min(Xb(:)), max(Xb(:)));",
        "",
        "% ---- 3. SNV (row-wise) ----",
        "% Each spectrum is centred on its own mean and divided by its own",
        "% standard deviation, so the multiplicative intensity effects of",
        "% focus and laser power are removed before the mean centring.",
        "mu = mean(Xb, 2);",
        "sd = std(Xb, 0, 2);",
        "",
        "Xsnv = (Xb - mu) ./ sd';",
        "",
        "% ---- 4. Mean centring (column-wise) ----",
        "Xc = Xsnv - mean(Xsnv, 1);",
        "",
        "out = array2table([wn; Xc]);",
        "writetable(out, fullfile(root, 'raman_preprocessed.csv'), 'WriteVariableNames', false);",
        "fprintf('Done: %d spectra written to raman_preprocessed.csv\\n', n);",
    ]
    assert lines[41] == "Xsnv = (Xb - mu) ./ sd';", "the bug must sit on line 42"
    write_text("preprocess_raman.m", "\n".join(lines) + "\n")


def excel_csv(name="espectros_excel.csv"):
    """Semicolon, decimal comma, cp1252 (accents in names), wavenumbers with
    decimals in the header, first column text, 3 empty cells."""
    x = nir_axis(160)[::-1]
    _, X, _, _ = nir_set(24, 5, m=160)
    X = X[:, ::-1]                               # this instrument exports ascending
    names = [f"{o}_{i:02d}" for o in ("Jaén", "Córdoba", "Lleida") for i in range(1, 9)]
    X[3, 40] = np.nan
    X[3, 41] = np.nan
    X[17, 150] = np.nan
    rows = [[names[i]] + [fmt(v) for v in X[i]] for i in range(24)]
    head = ["Muestra"] + [f"{v:.2f}".replace(".", ",") for v in x]
    write_csv(name, head, rows, sep=";", decimal=",", encoding="cp1252")


def pca_results():
    """pca_resultados.mat: scores, loadings and explained variance of an FTIR
    PCA (olive oil cultivars), axis stored ascending although IR plots run
    from high to low wavenumber."""
    x, X, grp = oil_ir(40, 13)
    mu = X.mean(0)
    U, s, Vt = np.linalg.svd(X - mu, full_matrices=False)
    for a in range(5):                                    # sign convention: largest loading positive
        if Vt[a, np.argmax(np.abs(Vt[a]))] < 0:
            Vt[a] *= -1
            U[:, a] *= -1
    ev = s ** 2
    savemat("pca_resultados.mat", {
        "T": np.round(U[:, :5] * s[:5], 6), "P": np.round(Vt[:5].T, 6),
        "explained": np.round(100 * ev[:5] / ev.sum(), 4), "wavenumber": x,
        "media": np.round(mu, 6), "grupo": np.array(list(grp), dtype=object),
        "info": "FTIR-ATR de 40 aceites, cm-1 (eje guardado ascendente), solo centrado",
    })


if __name__ == "__main__":
    run_script()
    error_script()
    excel_csv()
    pca_results()
    total = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
    print(f"{len(list(OUT.iterdir()))} fixtures, {total / 1e6:.2f} MB in {OUT}")
