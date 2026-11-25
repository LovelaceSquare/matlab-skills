% preprocess_raman.m
% Baseline correction (polynomial) + SNV + mean centring of the Raman
% series in raman_serie.csv. Writes raman_preprocessed.csv next to the script.
%
% Author: lab group, 2026

root = fileparts(mfilename('fullpath'));
% First row: Raman shift (cm-1); first column: sample names.
C = readcell(fullfile(root, 'raman_serie.csv'));
names = C(2:end, 1);
wn = cell2mat(C(1, 2:end));          % 1 x m axis
X = cell2mat(C(2:end, 2:end));       % n x m spectra

[n, m] = size(X);
fprintf('Loaded %d spectra x %d points (%.0f-%.0f cm-1)\n', n, m, wn(1), wn(end));

% ---- 1. Polynomial baseline (degree 6, iterative clipping) ----
deg = 6;
nIter = 5;
B = zeros(n, m);
for i = 1:n
    y = X(i, :);
    for it = 1:nIter
        p = polyfit(wn, y, deg);
        b = polyval(p, wn);
        y = min(y, b);
    end
    B(i, :) = b;
end
Xb = X - B;

% ---- 2. Quick look at the corrected range ----
fprintf('Corrected intensity range: %.3f to %.3f\n', min(Xb(:)), max(Xb(:)));

% ---- 3. SNV (row-wise) ----
% Each spectrum is centred on its own mean and divided by its own
% standard deviation, so the multiplicative intensity effects of
% focus and laser power are removed before the mean centring.
mu = mean(Xb, 2);
sd = std(Xb, 0, 2);

Xsnv = (Xb - mu) ./ sd';

% ---- 4. Mean centring (column-wise) ----
Xc = Xsnv - mean(Xsnv, 1);

out = array2table([wn; Xc]);
writetable(out, fullfile(root, 'raman_preprocessed.csv'), 'WriteVariableNames', false);
fprintf('Done: %d spectra written to raman_preprocessed.csv\n', n);
