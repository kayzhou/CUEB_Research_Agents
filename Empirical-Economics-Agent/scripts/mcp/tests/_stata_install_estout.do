* 安装 estout（esttab 表格输出依赖）。
* 运行前先 cd 到项目根目录，日志写入 results/logs/。
clear all
set more off
capture log close
log using "results/logs/install_estout.log", replace text

ssc install estout, replace

log close
exit, STATA
