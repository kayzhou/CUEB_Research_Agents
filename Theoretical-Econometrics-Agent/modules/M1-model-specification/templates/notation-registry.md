# Notation Registry

Use this file as the master symbol table.

| Symbol | Meaning | Dimension | First used | Status |
|---|---|---:|---|---|
| \(N\) | number of cross-sectional units | scalar | model | confirmed |
| \(T\) | number of time periods | scalar | model | confirmed |
| \(y_t\) | dependent variable vector | \(N\times1\) | model | confirmed |
| \(X_t\) | regressors | \(N\times k\) | model | editable |
| \(W_N\) | spatial weights matrix | \(N\times N\) | model | editable |
| \(S_N(\lambda)\) | \(I_N-\lambda W_N\) | \(N\times N\) | likelihood | confirmed |
| \(\tau_0\) | true break date | scalar | break | confirmed |
| \(\widehat\tau\) | estimated break date | scalar | estimation | confirmed |
| \(\theta_j\) | regime-j parameter vector | varies | likelihood | editable |
| \(u_t\) | disturbance vector | \(N\times1\) | model | editable |

When the agent introduces a new symbol, it must add a row here or in the project-level copy.

