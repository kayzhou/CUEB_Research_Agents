function cp = coverage_tstat(theta_hat, se_hat, theta0, alpha)
%COVERAGE_TSTAT Coverage probability for two-sided t-stat interval.

if nargin < 4
    alpha = 0.05;
end

z = 1.959963984540054; % norminv(0.975), avoid toolbox dependency
valid = isfinite(theta_hat) & isfinite(se_hat) & se_hat > 0;
covered = theta0 >= theta_hat(valid) - z * se_hat(valid) & ...
          theta0 <= theta_hat(valid) + z * se_hat(valid);
cp = mean(covered);
end

