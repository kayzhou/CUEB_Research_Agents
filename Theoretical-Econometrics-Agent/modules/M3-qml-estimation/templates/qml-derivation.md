# QML Derivation Template

## Model

\[
S_N(\lambda_j)y_t = Z_t\delta_j + u_t.
\]

## Residual

\[
e_{jt}(\theta_j)=S_N(\lambda_j)y_t-Z_t\delta_j.
\]

## Log-likelihood

\[
\ell_{NT}=\sum_{j=1}^2\left[T_j\log|S_N(\lambda_j)|-\frac{NT_j}{2}\log(2\pi\sigma_j^2)-\frac{1}{2\sigma_j^2}\sum_{t\in\mathcal{T}_j}e_{jt}'e_{jt}\right].
\]

## Concentration

For fixed \(\lambda_j\) and \(\tau\), derive \(\widehat\delta_j\) and \(\widehat\sigma_j^2\).

## Score

Derive score with respect to:

- \(\lambda_j\);
- \(\delta_j\);
- \(\sigma_j^2\).

## Hessian / information

State expected Hessian and sandwich components.

