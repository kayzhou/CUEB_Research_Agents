# install_r_packages.R — 安装空间计量交叉验证所需 R 包（用法：Rscript scripts/install_r_packages.R）
# 用途见 ENVIRONMENT.md §二.2：用 R 独立实现交叉验证 MATLAB/Python 的估计结果。

pkgs <- c(
  "spdep",        # 空间权重矩阵构造与检验
  "spatialreg",   # SAR / SDM / SEM 极大似然估计
  "splm",         # 空间面板模型
  "strucchange"   # 结构断点检验
)

missing <- pkgs[!vapply(pkgs, requireNamespace, logical(1), quietly = TRUE)]
if (length(missing) == 0) {
  cat("R 空间计量包已齐全：", paste(pkgs, collapse = ", "), "\n")
} else {
  cat("安装缺失包：", paste(missing, collapse = ", "), "\n")
  install.packages(missing, repos = "https://cloud.r-project.org")
  still <- missing[!vapply(missing, requireNamespace, logical(1), quietly = TRUE)]
  if (length(still) > 0) {
    cat("\n以下包安装失败：", paste(still, collapse = ", "), "\n")
    cat("常见原因：spdep/spatialreg/splm 经由 sf 依赖系统库 libudunits2、cmake、GDAL/GEOS/PROJ。\n")
    cat("无 root 权限时无法补齐系统库；此时按 ENVIRONMENT.md 的降级路由，\n")
    cat("空间估计交叉验证改用 Python 独立实现，断点检验用 strucchange。\n")
    quit(status = 1)
  }
  cat("安装完成。\n")
}
