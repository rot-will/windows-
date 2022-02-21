import sys,os,re
if sys.version_info.major!=3:
    exit("python3 must be used")
if len(sys.argv)<2:
    exit("python setup.py tools_path [System_var]")

root_path=os.path.realpath(sys.argv[1])
if len(sys.argv)==2:
    var_name='tools'
else:
    var_name=sys.argv[2]
    
if not os.path.isdir(root_path):
    try:
        os.mkdir(root_path)
        if not os.path.isdir(root_path):
            os.mkdir(root_path+'\\hide')
    except:
        exit("A file with the same name may exist")

path=os.popen('reg query HKEY_CURRENT_USER\Environment').read()
path_var=re.findall(' +[Pp]ath +REG_EXPAND_SZ +(.*)',path)[0]
path_var=path_var.replace("%"+var_name+"%",'')
path_var+=";%"+"%s"%var_name+"%"
path_var=path_var.replace(';;',';').replace('%','"%"')
os.popen('echo off && setx path "%s"'%path_var)
print("[+] change path success")
os.popen('echo off && setx %s "%s"'%(var_name,root_path))
print("[+] create %s success"%(var_name))

python_path=sys.executable
f=open('help.py')
script_data=f.read()
f.close()
script_data='root_path=r"%s"\n'%root_path+script_data
script_data='var_name=r"%s"\n'%var_name+script_data
f=open(root_path+'\\hide\\help.py','w')
f.write(script_data)
f.close()
print("[+] create file success")
def editbat(name,cmd,path):
    bat_file=open(root_path+'/'+path+'/'+name+'.bat','wb')
    direct="""@echo off
{} %* 
"""
    cmd=cmd.replace("'",'"')
    direct=direct.format(cmd)
    bat_file.write(direct.encode())
    bat_file.close()

cmd="%s %s\\hide\\help.py"%(python_path,root_path)
editbat("helper",cmd,'hide')
os.system(cmd+' -c')

