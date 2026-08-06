function est = estimate_qml_grid_break(data, W, trim)
%ESTIMATE_QML_GRID_BREAK Grid search over break dates and spatial parameters.
% This scaffold uses coarse lambda grid. Replace with robust optimization for final use.

if nargin < 3
    trim = 0.15;
end

y = data.y;
X = data.X;
[~, T] = size(y);

lambda_grid = linspace(-0.8, 0.8, 41);
tau_grid = floor(trim * T):ceil((1 - trim) * T);

best_obj = -Inf;
best = struct('tau', NaN, 'lambda_pre', NaN, 'lambda_post', NaN);

for tau = tau_grid
    y1 = y(:, 1:tau);
    X1 = X(:, :, 1:tau);
    y2 = y(:, tau+1:T);
    X2 = X(:, :, tau+1:T);

    for lam1 = lambda_grid
        obj1 = qml_objective_spatial_break_panel(lam1, y1, X1, W);
        if ~isfinite(obj1); continue; end
        for lam2 = lambda_grid
            obj2 = qml_objective_spatial_break_panel(lam2, y2, X2, W);
            obj = obj1 + obj2;
            if obj > best_obj
                best_obj = obj;
                best.tau = tau;
                best.lambda_pre = lam1;
                best.lambda_post = lam2;
            end
        end
    end
end

est.lambda_pre = best.lambda_pre;
est.lambda_post = best.lambda_post;
est.tau_hat = best.tau;
est.obj = best_obj;
est.converged = isfinite(best_obj);

% Placeholder standard errors. Must be replaced by Hessian/sandwich estimates.
est.se_lambda_pre = NaN;
est.se_lambda_post = NaN;
end

