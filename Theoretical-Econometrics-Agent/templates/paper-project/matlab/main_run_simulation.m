% main_run_simulation.m
% Reproducible Monte Carlo scaffold for a spatial panel model with an unknown break.
% Adapt the estimator details after finalizing the likelihood.

clear; clc;

addpath(genpath(fileparts(mfilename('fullpath'))));

cfg.seed = 20260622;
cfg.R = 50;              % debug; use 500/1000 for final
cfg.N_grid = [50, 100];
cfg.T_grid = [40, 80];
cfg.trim = 0.15;
cfg.weight_design = 'ring';

true_params.lambda_pre = 0.30;
true_params.lambda_post = 0.50;
true_params.beta_pre = [1.0; 0.5];
true_params.beta_post = [1.0; 0.8];
true_params.gamma_pre = [0.2; 0.1];
true_params.gamma_post = [0.2; 0.3];
true_params.sigma_pre = 1.0;
true_params.sigma_post = 1.0;
true_params.break_fraction = 0.50;

out_rows = [];
row_id = 0;

for N = cfg.N_grid
    for T = cfg.T_grid
        fprintf('Running design N=%d, T=%d\n', N, T);
        W = make_spatial_weights(N, cfg.weight_design);
        for r = 1:cfg.R
            rng(cfg.seed + r, 'twister');
            data = simulate_spatial_break_panel(N, T, W, true_params);
            est = estimate_qml_grid_break(data, W, cfg.trim);
            row_id = row_id + 1;
            out_rows(row_id).N = N; %#ok<SAGROW>
            out_rows(row_id).T = T;
            out_rows(row_id).rep = r;
            out_rows(row_id).lambda_pre_hat = est.lambda_pre;
            out_rows(row_id).lambda_post_hat = est.lambda_post;
            out_rows(row_id).tau_hat = est.tau_hat;
            out_rows(row_id).converged = est.converged;
        end
    end
end

results_dir = fullfile(fileparts(fileparts(mfilename('fullpath'))), 'results');
if ~exist(fullfile(results_dir, 'raw'), 'dir'); mkdir(fullfile(results_dir, 'raw')); end
if ~exist(fullfile(results_dir, 'tables'), 'dir'); mkdir(fullfile(results_dir, 'tables')); end

T_raw = struct2table(out_rows);
writetable(T_raw, fullfile(results_dir, 'raw', 'mc_estimates.csv'));

summary = summarize_mc_results(T_raw, true_params);
writetable(summary, fullfile(results_dir, 'tables', 'mc_summary.csv'));

disp(summary);

