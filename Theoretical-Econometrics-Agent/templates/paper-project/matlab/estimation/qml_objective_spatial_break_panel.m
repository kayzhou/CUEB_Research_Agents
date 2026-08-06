function obj = qml_objective_spatial_break_panel(lambda, y_block, X_block, W)
%QML_OBJECTIVE_SPATIAL_BREAK_PANEL Concentrated objective for one regime.
% This is a simplified scaffold. Adapt fixed effects and covariance assumptions.

[N, Tj] = size(y_block);
k = size(X_block, 2);
I = eye(N);
S = I - lambda * W;

% Stability check
if rcond(S) < 1e-8
    obj = -Inf;
    return;
end

logdetS = log(abs(det(S)));
Ytilde = zeros(N * Tj, 1);
Z = zeros(N * Tj, 2 * k + N);

for tt = 1:Tj
    rows = (tt - 1) * N + (1:N);
    Xt = X_block(:, :, tt);
    Ytilde(rows) = S * y_block(:, tt);
    Z(rows, :) = [Xt, W * Xt, eye(N)];
end

delta_hat = Z \ Ytilde;
e = Ytilde - Z * delta_hat;
sigma2_hat = max((e' * e) / (N * Tj), 1e-10);

obj = Tj * logdetS - (N * Tj / 2) * log(sigma2_hat);
end

