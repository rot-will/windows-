-c, --create          Construct system variables default:False
-help                 view type default:False
-hide                 Show hide commands default:True
-s SEARCH_STR, --search SEARCH_STR
                      Search specified string
-dire                 Search specified type
-d DIRECT, --direct DIRECT
                      Specify command
-start                Do you want to use start to launch exe
-tardir TARGET_DIR    Specify target program directory
-n NAME, --name NAME  Specify script name
-replace              Replace the original command default:False
-t TYPE, --type TYPE  Type of command xx/xxx/xxxx
-add ADD_DIRE         Added type
-del DEL_DIRE         Delete command or type

-c 构建系统变量 tools 将所有目录加入tools中
-s 搜索指定命令名称  当存在 -dire 参数时用于搜索目录名称 
-help 显示帮助文档并显示目录框架
-d 添加的命令 当目标为exe时 使用-start 指定是否使用start 命令开启
-n 命令名称
-t 命令所属类型
-replace 当存在时 命令 与 命令类型只需要一个 用来修改命令 或者 修改命令路径
-tardir 命令执行目录 当命令需要在指定目录执行时
-add 添加的类型
-del 删除的类型 或 命令
-hide 当存在时 显示hide 目录 当不存在时不显示  real_hide 必定不显示

help1 搜索字符时 当没有找到元素 则输出 ...
help  搜索字符时 当没有找到元素 则不输出类型