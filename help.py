#!python3
"""
@User: rot_will
@date: 2022.6.26
"""
import os,re
import argparse
import sys,msvcrt
import colorama

colorama.init(autoreset=True)
file_color="\033[94m"
dire_color="\033[92m"
back_color="\033[0m"

wait=['< -- wait -- >\r','              \r']
ddict={}
tools_env=root_path+';'
filelist={}
comm_orig=['@echo off','cd /d %sour_dir%','set sour_dir=%CD%','']
def updir(cmd,path,dict_path,is_creat=False):
    global ddict
    global filelist
    global tools_env
    cache=os.listdir(path)
    exec("%s={}"%cmd)
    dircache=[]
    for i in cache:
        if os.path.isfile(path+'/'+i):
            if i[-4:]!='.bat':
                continue
            exec("%s['%s']=1"%(cmd,i))
            i=i[:i.rfind('.')]
            filelist[i]=path
        else:
            dircache.append(i)
    for i in dircache:
        if is_creat:
            if ' ' in path+'\\'+i:
                tools_env+='"%s"'%(path+'\\'+i)+';'
            else:
                tools_env+=path+'\\'+i+';'
        getdirlist(dict_path+'$'+i,is_creat)
            
def getdirlist(path='',is_creat=False):
    global root_path
    global ddict
    global filelist
    global tools_env
    if path:
        cmd='ddict'
        for i in path.split('$'):
            if i:
                cmd+='["%s"]'%i
            else:
                cmd+='["/"]'
        real_path=root_path+path.replace('$','\\')
        updir(cmd,real_path,path,is_creat=is_creat)
    else:
        ddict['/']={}
        cache=os.listdir(root_path)
        dircache=[]
        for i in cache:
            if os.path.isfile(root_path+'\\'+i):
                if i[-4:]!='.bat':
                    continue
                ddict['/'][i]=1
                i=i[:i.find('.')]
                filelist[i]=root_path
            else:
                dircache.append(i)
        for i in dircache:
            if is_creat:
                if ' ' in root_path+'\\'+i:
                    tools_env+='"%s"'%(root_path+'\\'+i)+';'
                else:
                    tools_env+=root_path+'\\'+i+';'
            getdirlist('$'+i,is_creat)
                
def setenv():
    os.popen('@echo off && setx %s %s'%(var_name,tools_env.strip(';')))
    print('[+] save success')

def showdict(dir_dict,pad="",search_str="",is_show_file=True,is_dire=False,dire_in=-1,hide=True,num_col=0):
    n=0
    cache=''
    file_cache=""
    file_num=0
    file_for=file_color+'{}'+back_color+' / '
    dire_for='\n{}'+"*- "+dire_color+'{}'+back_color
    for i in dir_dict:
        if dir_dict[i]==1:
            if is_show_file and ((dire_in + is_dire)==-1 or (dire_in+is_dire)==2):
                i=i[:i.rfind('.')]
                if search_str and not is_dire:
                    if search_str in i:
                        file_num+=1
                        file_cache+="%s / "%(file_color+i+back_color)
                        n=n+1
                else:
                    file_num+=1
                    file_cache+="%s / "%(file_color+i+back_color)
                    n=n+1
                    
                if file_num>=num_col:
                    file_num=0
                    file_cache=file_cache[:-3]+'\n'+pad+" \\-  "
        else:
            if ('hide' in i and hide) or ('real_hide' in i):
                continue
            n_1=0
            cache_1=''
            if is_dire:
                n_1,cache_1=showdict(dir_dict[i],pad+'  ',search_str,is_show_file,is_dire,(search_str in i or (dire_in==1)),hide,num_col)
            else:
                n_1,cache_1=showdict(dir_dict[i],pad+'  ',search_str,is_show_file,is_dire,-1,hide,num_col)
            if n_1!=0 or search_str=='':
                cache+=dire_for.format(pad,i)+cache_1
                #cache+="\n%s*- %s"%(pad,dire_color+i+back_color)+cache_1
                n=n+1
    if file_cache=="":
        file_cache=''
    else:
        file_cache="\n"+pad+'+-- '+file_cache[:-3]
    cache=cache+file_cache
    return n,cache

def get_cmd_info(path):
    f=open(path,'rb')
    data=f.read().decode('gbk')
    cmd=re.findall('set c=(.*)',data)[0].strip()
    des=re.findall('set des=(.*)',data)[0].strip()
    real_dir=''
    try:
        real_dir=re.findall('set real_dir="(.*?)"',data)[0].strip()
    except IndexError:
        pass
        
    is_start=False
    if 'start ""'  in data:
        is_start=True
    return cmd,des,is_start,real_dir


def editbat(name,cmd,path,real_dir,represent,is_start):
    file_path=root_path+'\\'+path+'\\'+name+'.bat'
    bat_file=open(file_path,'wb')
    try:
        pad='"%c%" %*\r\n'
        cmd_line='set c='
        direct=comm_orig[0]+'\r\n'
        cd_dir=""
        return_dir=""
        des_line='set des=%s'%represent
        if real_dir:
            return_dir=comm_orig[1]+'\r\n'
            #cd_dir+=comm_orig[3]+'\r\n'+comm_orig[4]+'\r\n'
            cd_dir+=comm_orig[2]+'\r\n'
            cd_dir+='set real_dir="%s"'%real_dir+'\r\n'
            cd_dir+="cd /d %real_dir%"+'\r\n'
        
        cmd=cmd.replace("'",'"')
        if os.path.isfile(cmd):
            if is_start:
                pad='start "" "%c%" %*\r\n'
            cmd=os.path.realpath(cmd)
            cmd_line+=cmd
        else:
            pad='%c% %*\r\n'
            if '%*' in cmd:
                pad='%c% \r\n'
            cmd_line+=cmd
        direct=direct+cd_dir+cmd_line+'\r\n'+pad+return_dir+des_line
        bat_file.write(direct.encode('gbk'))
    except:
        os.remove(file_path)
        
def addbat(name,cmd='',path='',real_dir='',represent='',is_start=True,is_re=False):
    if is_re:
        if path and cmd:
            exit("Only command contents or command directories can be replaced")
        try:
            cmd_c,des,is_start_c,real_dir_c=get_cmd_info(filelist[name]+'\\'+name+'.bat')
        except KeyError:
            print("Not found %s \\ %s"%(name,path))
        if is_start==True and is_start_c!=is_start:
            is_start=False
        elif is_start==False and is_start_c==is_start:
            is_start=True
        if not represent:
            represent=des
        if not cmd:
            cmd=cmd_c
        if not real_dir:
            real_dir=real_dir_c
        if path:
            if os.path.isdir(root_path+'\\'+path):
                path+="\\"+name
            elif os.path.isdir(root_path+'\\'+path+'.bat'):
                exit("There are duplicate options")
                return 0
            os.rename(filelist[name]+'\\'+name+'.bat',root_path+'\\'+path+'.bat')
            return 0
        else:
            editbat(name,cmd,filelist[name][len(root_path)+1:],real_dir,represent,is_start)
            return 0;
    elif name in filelist:
        exit("There are duplicate options")
    editbat(name,cmd,path,real_dir,represent,is_start)
    
def deldir(path):
    cache=os.listdir(path)
    for i in cache:
        if os.path.isdir(path+'/'+i):
            deldir(path+'/'+i)
            os.rmdir(path+'/'+i)
        else:
            os.remove(path+'/'+i)

def delete(path):
    if os.path.isdir(root_path+'/'+path):
        deldir(root_path+'/'+path)
        os.rmdir(root_path+'/'+path)
    elif os.path.isfile(root_path+'/'+path+'.bat'):
        os.remove(root_path+'/'+path+'.bat')
    else:
        exit('The command or directory does not exist')

def create(path):
    real_path=root_path
    if os.path.isdir(real_path+'/'+path):
        exit("The specified destination is occupied by the directory")
    elif os.path.isfile(real_path+'/'+path+'.bat'):
        exit('The specified target is occupied by the command')
    for i in path.split('/'):
        real_path+='/'+i
        if not os.path.isdir(real_path):
            os.mkdir(real_path)
    getdirlist(is_creat=True)
    setenv()
    
def out_command(coms,rows=20):
    coms=coms.splitlines()
    row=0
    uchar=''
    curr_row=0
    while curr_row<len(coms):
        sys.stdout.flush()
        sys.stdin.flush()
        try:
            if row<rows:
                sys.stdout.write(wait[1])
                print(coms[curr_row])
                row=row+1
                curr_row+=1
            else:
                sys.stdout.write(wait[0])
                uchar=msvcrt.getch()
                if uchar == b' ':
                    row=row-5
                elif uchar in [b'e',b'q',b'\x03',b'\x1a']:
                    raise KeyError()
                else:
                    row-=1
        except Exception as e:
            sys.stdout.write(wait[1])
            print(coms[curr_row])
            return 0

def out_des_com(comm_list,cmd_width,des_width):
    print("command:")
    for i in comm_list:
        cmd=i[0].ljust(cmd_width,b' ').decode('gbk')
        des=i[2].ljust(des_width,b' ').decode('gbk')
        print("   %s : %s : %s"%(cmd,des,i[1]))


def OutCommands(com_s):
    out_comm_list=[]
    cmd_width=0
    des_width=0
    for i in filelist.keys():
        if com_s in i or com_s=='*':
            cache=(get_OutCommand(i))
            if len(cache[0])>cmd_width:
                cmd_width=len(cache[0])
            if len(cache[2])>des_width:
                des_width=len(cache[2])
            out_comm_list.append(cache)
    out_des_com(out_comm_list,cmd_width,des_width)
    
def get_OutCommand(com_n):
    comm_path=filelist[com_n]+'\\'+com_n+'.bat'
    f=open(comm_path,'rb')
    d=f.read().decode('gbk')
    cmd=re.findall('set c=(.*)',d)[0]
    des=re.findall('set des=(.*)',d)[0].encode("gbk")
    return [com_n.encode("gbk"),cmd,des]
        
def help(parse):
    """ show """
    parse.add_argument('-c','--create',dest='is_creat',action='store_true', default=False,help="Construct system variables default:False")
    parse.add_argument('-help',dest='show_type',action='store_true', default=False,help="view type default:False")
    parse.add_argument('-hide',dest='is_hide',action='store_false', default=True,help="Show hide commands default:True")
    parse.add_argument('-out',dest='out_command',help="View the contents of the command")
    parse.add_argument('-noc',dest='num_col',default=6,help="Number of columns")
    
    """ search """
    parse.add_argument('-s','--search',dest='search_str',default='',help="Search specified string")
    parse.add_argument('-dire',dest='dire_str',action='store_true',default=False,help='Search specified type')
    
    """ command_data """
    parse.add_argument('-d','--direct',dest='direct',default='',help='Specify command')
    parse.add_argument('-start',dest='is_start',action='store_false', default=True,help="Do you want to use start to launch exe")
    parse.add_argument('-tardir',dest='target_dir',default='',help="Specify target program directory")
    
    """ command """
    parse.add_argument('-n','--name',dest='name',default='',help='Specify script name')
    parse.add_argument('-r','--represent',dest='represent',default='',help="command note")
    parse.add_argument('-replace',dest='is_re',action='store_true',default=False,help="Replace the original command default:False")
    
    """ type """
    parse.add_argument('-t','--type',dest='type',default='',help='Type of command xx/xxx/xxxx')
    
    """ create type """
    parse.add_argument('-add',dest='add_dire',help='Added type')
    
    """ delete type/command """
    parse.add_argument('-del',dest='del_dire',help='Delete command or type')
    

def main():
    parse=argparse.ArgumentParser('help')
    help(parse)
    args=parse.parse_args()
    getdirlist(is_creat=args.is_creat)
    if args.is_creat:
        setenv()
    if args.show_type:
        parse.print_help()
        print("\n--------------- view Type ---------------\n")
        print(showdict(ddict,'',is_show_file=not args.show_type)[1])
        exit(0)
    elif args.name:
        if (not (args.direct or args.type or args.is_re)) :
            exit("When name exists, direct is required")
        addbat(args.name,args.direct,args.type,args.target_dir,args.represent,args.is_start,args.is_re)
    elif args.del_dire:
        delete(args.del_dire)
    elif args.add_dire:
        create(args.add_dire)
    elif args.out_command:
        OutCommands(args.out_command)
    else:
        coms=showdict(ddict,'',args.search_str,is_dire=args.dire_str,hide=args.is_hide,num_col=args.num_col)[1]
        out_command(coms)

if __name__=='__main__':
    main()
