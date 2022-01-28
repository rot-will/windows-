import os
import argparse
root_path=r'B:\tools'
ddict={}
tools_env=root_path+';'
filelist=[]
def updir(cmd,path,dict_path,is_creat=False,hide=True):
    global ddict
    global filelist
    global tools_env
    cache=os.listdir(path)
    exec("%s={}"%cmd)
    for i in cache:
        if os.path.isfile(path+'/'+i):
            exec("%s['%s']=1"%(cmd,i))
            filelist.append(i)
        else:
            if is_creat:
                if ' ' in path+'\\'+i:
                    tools_env+='"%s"'%(path+'\\'+i)+';'
                else:
                    tools_env+=path+'\\'+i+';'
            if hide and 'hide' in i:
                continue
            getdirlist(dict_path+'$'+i,is_creat,hide)
            
def getdirlist(path='',is_creat=False,hide=True):
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
                cmd+='["root"]'
        real_path=root_path+path.replace('$','\\')
        updir(cmd,real_path,path,is_creat=is_creat,hide=hide)
    else:
        ddict['root']={}
        cache=os.listdir(root_path)
        for i in cache:
            if os.path.isfile(root_path+'\\'+i):
                ddict['root'][i]=1
                filelist.append(i)
            else:
                if is_creat:
                    if ' ' in root_path+'\\'+i:
                        tools_env+='"%s"'%(root_path+'\\'+i)+';'
                    else:
                        tools_env+=root_path+'\\'+i+';'
                if hide and 'hide' in i:
                    continue
                getdirlist('$'+i,is_creat,hide)
                
def setenv():
    os.system('setx tools %s'%tools_env.strip(';'))

def showdict(dir_dict,pad="",search_str="",is_show_file=True,is_dire=False,dire_in=-1):
    n=0
    for i in dir_dict:
        if dir_dict[i]==1:
            if is_show_file and ((dire_in + is_dire)==-1 or (dire_in+is_dire)==2):
                i=i[:i.find('.')]
                if search_str and not is_dire:
                    if search_str in i:
                        print("%s|- %s"%(pad,i))
                        n=n+1
                else:
                    print("%s|- %s"%(pad,i))
                    n=n+1
        else:
            print("%s*- %s"%(pad,i))
            if is_dire:
                showdict(dir_dict[i],pad+'  ',search_str,is_show_file,is_dire,(search_str in i))
            else:
                showdict(dir_dict[i],pad+'  ',search_str,is_show_file,is_dire)
            n=n+1
    if n==0 and is_show_file:
        print("%s-- ..."%(pad))
    return n

def addbat(cmd,name,path='',real_dir='',is_start=True):
    if name+'.bat' in filelist:
        exit("There are duplicate options")
    bat_file=open(root_path+'/'+path+'/'+name+'.bat','wb')
    direct="""@echo off
set sour_dir=%CD%
set dl=%CD:~0,2%
{} %*
%dl%
cd %sour_dir%
@echo on
"""
    cd_dir=""
    if real_dir:
        cd_dir+=real_dir[:2]+'\n'
        cd_dir+="cd "+real_dir+'\n'
    if os.path.isfile(cmd):
        if '.exe' in cmd:
            if ' ' in cmd:
                direct=direct.format(cd_dir+'start '*is_start+'"%s"'%cmd)
            else:
                direct=direct.format(cd_dir+'start '*is_start+'%s'%cmd)
        else:
            direct=direct.format(cd_dir+'"%s"'%cmd.replace("'",'"'))
    else:
        direct=direct.format(cd_dir+(cmd.replace("'",'"')))
    bat_file.write(direct.encode())
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
    
def help(parse):
    parse.add_argument('-c','--create',dest='is_creat',action='store_true', default=False,help="Construct system variables default:False")
    parse.add_argument('-help',dest='show_type',action='store_true', default=False,help="view type default:False")
    parse.add_argument('-hide',dest='is_hide',action='store_false', default=True,help="Show hide commands default:True")
    parse.add_argument('-s','--search',dest='search_str',default='',help="Search specified string")
    parse.add_argument('-dire',dest='dire_str',action='store_true',default=False,help='Search specified directory')
    parse.add_argument('-d','--direct',dest='direct',default='',help='Specify command')
    parse.add_argument('-start',dest='is_start',action='store_false', default=True,help="Do you want to use start to launch exe")
    parse.add_argument('-n','--name',dest='name',default='',help='Specify script name')
    parse.add_argument('-t','--type',dest='type',default='',help='Type of command xx/xxx/xxxx')
    parse.add_argument('-tardir',dest='target_dir',default='',help="Specify target program directory")
    parse.add_argument('-add',dest='add_dire',help='Added directory')
    parse.add_argument('-del',dest='del_dire',help='Delete command or directory')
    

def main():
    parse=argparse.ArgumentParser('help')
    help(parse)
    args=parse.parse_args()
    getdirlist(is_creat=args.is_creat,hide=args.is_hide)
    if args.is_creat:
        setenv()
    if args.show_type:
        parse.print_help()
        print("\n--------------- view Type ---------------\n")
        showdict(ddict,'',is_show_file=not args.show_type)
        exit(0)
    elif args.direct:
        if not (args.name or args.type):
            exit("When direct exists, name is required")
        addbat(args.direct,args.name,args.type,args.target_dir,args.is_start)
    elif args.del_dire:
        delete(args.del_dire)
    elif args.add_dire:
        create(args.add_dire)
    else:
        showdict(ddict,'',args.search_str,is_dire=args.dire_str)

if __name__=='__main__':
    main()
