import rarfile,zipfile,os,shutil
from pathlib import Path

basePath='C:\\test'
outPath='C:\\test'
passlist=[]
passlist.append("gxzc")
# with open('pass.txt','r') as f:
#     for line in f.readlines():
#         passlist.append(line.rstrip())

for root,dirs,fs in os.walk(basePath):
    for f in fs:
        filename=os.path.join(root,f)
        type=os.path.splitext(filename)[-1][1:]
        if type=='rar':
            fileget=rarfile.RarFile(filename)
            with fileget as rf:
                if rf.needs_password():#判断是否需要密码
                    for pwds in passlist:
                        try:
                            fileget.extractall(outPath,pwd=pwds.encode())#不要直接用pwds，要编码一下
                            print(filename+":"+pwds)
                            os.remove(filename)
                        except:
                            pass
                else:
                    try:
                        fileget.extractall(outPath)
                        os.remove(filename)
                    except:
                        pass
        elif type=='zip':
            with zipfile.ZipFile(filename, 'r') as zf:
                for info in zf.infolist():
                    try:
                        newname=info.filename.encode('cp437').decode('gbk');
                    except:
                        try:
                            newname=info.filename.encode('cp437').decode('utf-8');
                        except:
                            newname=info.filename
                    outname=newname.split('/')
                    l=len(outname)
                    if outname[l-1]!='':#如果是文件
                        if info.flag_bits & 0x01:#如果文件有密码
                            for pwd in passlist:
                                try:
                                    body=zf.read(info,pwd=pwd.encode())
                                    print("pass:"+pwd)
                                    with open(outPath+'/'+outname[l-1],'wb') as outfile:
                                        outfile.write(body)
                                except:
                                    pass
                        else:
                            with open(outPath+'/'+outname[l-1],'wb') as outfile:#要把中文的zip解压出中文，就不要用extract了，在新位置创建中文名文件，然后把读取出来的数据写进去就可以。
                                outfile.write(zf.read(info))
        else:#如果是文件，直接复制到新位置
            shutil.copy(filename,outPath+'\\'+f)