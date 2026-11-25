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
