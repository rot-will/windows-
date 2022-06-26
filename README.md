setup.py<br>
    python3 setup.py 命令储存目录 [环境变量名称]<br>
        目录可以是创建好的 也可以不创建 <br>
        环境变量名称 默认为 tools<br>
        最后会创建命令helper<br>
        需要重启cmd<br>
<br>
<br>
<br>
<br>
usage: help [-h] [-c] [-help] [-hide] [-out OUT_COMMAND] [-noc NUM_COL] [-s SEARCH_STR] [-dire] [-d DIRECT] [-start]<br>
            [-tardir TARGET_DIR] [-n NAME] [-r REPRESENT] [-replace] [-t TYPE] [-add ADD_DIRE] [-del DEL_DIRE]<br>
<br>
optional arguments:<br>
  -h, --help            show this help message and exit<br>
  -c, --create          Construct system variables default:False<br>
  -help                 view type default:False     查看帮助文档,并显示所有目录<br> 
  -hide                 Show hide commands default:True    列出命令,包括隐藏的文件<br>
  -out OUT_COMMAND      View the contents of the command    显示命令的内容,与描述<br>
   -noc NUM_COL         Number of columns  指定每行命令名称个数<br>
  -s SEARCH_STR, --search SEARCH_STR    指定搜索的字符串 可以传入一部分<br>
                        Search specified string    搜索命令名称<br>
  -dire                 Search specified type   指定搜索目录名称,输出搜索到的目录中的所有命令  与-s 一起使用<br>
  
  -start                Do you want to use start to launch exe    指定窗口程序不使用 start命令<br>
  -tardir TARGET_DIR    Specify target program directory    当程序只能在指定目录使用时,使用这个参数,指定目录<br>
  -n NAME, --name NAME  Specify script name    指定命令的名称<br>
  -t TYPE, --type TYPE  Type of command xx/xxx/xxxx    指定添加的命令所在目录<br>
  -d DIRECT, --direct DIRECT    指定添加的命令<br>
                        Specify command<br>                      
  -r REPRESENT, --represent REPRESENT    指定命令的描述<br>
                        command note<br>
  -replace              Replace the original command default:False    用于修改命令(命令内容,命令位置,命令描述,命令是否使用start)<br>
  
  -add ADD_DIRE         Added type    添加目录<br>
  -del DEL_DIRE         Delete command or type    删除目录或命令<br>
