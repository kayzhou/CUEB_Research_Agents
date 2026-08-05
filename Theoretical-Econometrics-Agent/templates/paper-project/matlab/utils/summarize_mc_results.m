function summary = summarize_mc_results(T_raw, true_params)
%SUMMARIZE_MC_RESULTS Compute simple Monte Carlo summary.
% Extend this function to all parameters after estimator returns full theta.

rows = [];
idx = 0;
designs = unique(T_raw(:, {'N', 'T'}));

for d = 1:height(designs)
    N = designs.N(d);
    TT = designs.T(d);
    mask = T_raw.N == N & T_raw.T == TT & T_raw.converged == 1;
    sub = T_raw(mask, :);

    idx = idx + 1;
    rows(idx).N = N; %#ok<AGROW>
    rows(idx).T = TT;
    rows(idx).parameter = "lambda_pre";
    rows(idx).true_value = true_params.lambda_pre;
    rows(idx).mean_hat = mean(sub.lambda_pre_hat, 'omitnan');
    rows(idx).bias = rows(idx).mean_hat - true_params.lambda_pre;
    rows(idx).rmse = sqrt(mean((sub.lambda_pre_hat - true_params.lambda_pre).^2, 'omitnan'));
    rows(idx).cp95 = NaN; % requires standard errors
    rows(idx).fail_rate = 1 - height(sub) / sum(T_raw.N == N & T_raw.T == TT);

    idx = idx + 1;
    rows(idx).N = N;
    rows(idx).T = TT;
    rows(idx).parameter = "lambda_post";
    rows(idx).true_value = true_params.lambda_post;
    rows(idx).mean_hat = mean(sub.lambda_post_hat, 'omitnan');
    rows(idx).bias = rows(idx).mean_hat - true_params.lambda_post;
    rows(idx).rmse = sqrt(mean((sub.lambda_post_hat - true_params.lambda_post).^2, 'omitnan'));
    rows(idx).cp95 = NaN;
    rows(idx).fail_rate = 1 - height(sub) / sum(T_raw.N == N & T_raw.T == TT);
end

summary = struct2table(rows);
end

