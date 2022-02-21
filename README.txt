setup.py<br>
    python3 setup.py 命令储存目录 [环境变量名称]<br>
        目录可以是创建好的 也可以不创建 <br>
        环境变量名称 默认为 tools<br>
        最后会创建命令helper<br>
        需要重启cmd<br>
<br>
<br>
help<br>
    -h, --help            show this help message and exit<br>
    -c, --create          构建系统变量<br>
    -help                 查看类型与帮助文档 <br>
    -hide                 查看所有类型或变量 除了 real_hide中的命令<br>
    -s SEARCH_STR, --search SEARCH_STR<br>
                        搜索命令或类型<br>
    -dire                 允许搜索类型<br>
    -d DIRECT, --direct DIRECT<br>
                        命令内容<br>
    -start                是否使用start启动exe程序 (当程序为命令行工具时 建议使用该参数)<br>
    -tardir TARGET_DIR    当命令需要在指定的目录中执行时 建议使用该参数 <br>
    -n NAME, --name NAME  命令名称<br>
    -replace              是否允许修改 默认 不允许<br>
        当同时存在 -d -n 时修改命令<br>
        当同时存在 -n -t 时修改命令名称 或 命令路径 <br>
    -t TYPE, --type TYPE  类型路径 xx/xxx/xxxx<br>
    -add ADD_DIRE         添加类型<br>
    -del DEL_DIRE         删除类型或命令<br>
    <br>
    <br>
    helper -d 命令执行字符串  -n 命令名称 -t 命令路径  <br>
        创建一个命令<br>
    <br>
    <br>
    -c 构建系统变量 tools 将所有目录加入tools中<br>
    -s 搜索指定命令名称  当存在 -dire 参数时用于搜索目录名称 <br>
    -help 显示帮助文档并显示目录框架<br>
    -d 添加的命令 当目标为exe时 使用-start 指定是否使用start 命令开启<br>
    -n 命令名称<br>
    -t 命令所属类型<br>
    -replace 当存在时 命令 与 命令类型只需要一个 用来修改命令 或者 修改命令路径 或 路径/名称<br>
    -tardir 命令执行目录 当命令需要在指定目录执行时<br>
    -add 添加的类型<br>
    -del 删除的类型 或 命令<br>
    -hide 当存在时 显示hide 目录 当不存在时不显示  real_hide 必定不显示<br>
