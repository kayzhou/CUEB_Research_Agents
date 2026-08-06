function data = simulate_spatial_break_panel(N, T, W, params)
%SIMULATE_SPATIAL_BREAK_PANEL Simulate a spatial Durbin panel with one break.

k = numel(params.beta_pre);
tau0 = floor(params.break_fraction * T);
I = eye(N);

alpha = randn(N, 1) * 0.2;
X = randn(N, k, T);
y = zeros(N, T);

for t = 1:T
    if t <= tau0
        lambda = params.lambda_pre;
        beta = params.beta_pre;
        gamma = params.gamma_pre;
        sigma = params.sigma_pre;
    else
        lambda = params.lambda_post;
        beta = params.beta_post;
        gamma = params.gamma_post;
        sigma = params.sigma_post;
    end

    Xt = X(:, :, t);
    u = sigma * randn(N, 1);
    S = I - lambda * W;
    rhs = Xt * beta + W * Xt * gamma + alpha + u;
    y(:, t) = S \ rhs;
end

data.y = y;
data.X = X;
data.tau0 = tau0;
data.params = params;
end

