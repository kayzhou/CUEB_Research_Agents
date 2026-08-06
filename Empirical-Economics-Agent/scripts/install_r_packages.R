#!/usr/bin/env Rscript

# Install the causal-inference packages documented by this repository.
# Run after: source scripts/setup_env.sh

repos <- c(CRAN = "https://cloud.r-project.org")
packages <- c("fixest", "did", "rdrobust", "eventstudyr")
missing <- packages[!vapply(packages, requireNamespace, logical(1), quietly = TRUE)]

if (length(missing) == 0) {
  cat("R causal packages already installed.\n")
  quit(status = 0)
}

cat("Installing:", paste(missing, collapse = ", "), "\n")
# Install Depends/Imports/LinkingTo only. `dependencies = TRUE` also installs
# every Suggests package and can trigger a very large, unnecessary toolchain.
install.packages(missing, repos = repos, dependencies = NA)

still_missing <- packages[!vapply(packages, requireNamespace, logical(1), quietly = TRUE)]
if (length(still_missing)) {
  stop("Installation incomplete: ", paste(still_missing, collapse = ", "))
}

cat("R causal packages installed successfully.\n")
