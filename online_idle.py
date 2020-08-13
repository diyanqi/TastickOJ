import os

def read_file_as_str2(file_path):
    # 判断路径文件存在
    if not os.path.isfile(file_path):
        raise TypeError(file_path + " does not exist")

    all_the_text = open(file_path).read()
    # print type(all_the_text)
    return all_the_text

def onlineCodeRun(code,codesh,inputfile,outputfile,clog):
    os.system('g++ '+code+' -o '+codesh+' 2> '+clog)
    if not os.path.isfile(codesh):
        rst={'log':'编译错误：'+read_file_as_str2(clog)}
        return rst
    os.system('./'+codesh+' < '+inputfile+' > '+outputfile)
    rst={'log':read_file_as_str2(outputfile)}
    open(outputfile,'w').truncate()
    os.remove(codesh)
    return rst