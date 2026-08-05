# Assumptions Checklist

Use this checklist when drafting or auditing assumptions.

## Spatial weights

- [ ] \(W_N\) has zero diagonal.
- [ ] Row sums are uniformly bounded.
- [ ] Column sums are uniformly bounded if needed.
- [ ] Spectral radius condition or invertibility condition is stated.
- [ ] Normalization is defined.
- [ ] Whether \(W_N\) is fixed or stochastic is stated.

## Regressors

- [ ] Dimensions are clear.
- [ ] Exogeneity or predeterminedness is stated.
- [ ] Moment conditions are stated.
- [ ] Rank condition is stated.
- [ ] Spatially lagged regressors are handled.

## Errors

- [ ] Conditional mean zero.
- [ ] Variance structure.
- [ ] Moment bound.
- [ ] Cross-sectional dependence assumption.
- [ ] Temporal dependence assumption.
- [ ] Heteroskedasticity allowance.

## Break

- [ ] True break fraction is interior.
- [ ] Break magnitude is nonzero or shrinking regime is specified.
- [ ] Break is common or heterogeneous.
- [ ] Number of breaks is fixed.
- [ ] Trimmed search set is defined.

## Identification

- [ ] Expected objective uniquely maximized at true parameter.
- [ ] Regimes are distinguishable.
- [ ] No observational equivalence.

## Asymptotics

- [ ] State whether \(N\to\infty\), \(T\to\infty\), or both.
- [ ] State relative rate restrictions if needed.
- [ ] Define effective information rate.
- [ ] Define stochastic order notation.


