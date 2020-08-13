def read_file_as_str(file_path):
    # 判断路径文件存在
    if not os.path.isfile(file_path):
        raise TypeError(file_path + " does not exist")

    all_the_text = open(file_path).read()
    # print type(all_the_text)
    return all_the_text

def fcmp(patha,pathb):
    f1=open(patha)
    f2=open(pathb)
    line_cnt=0
    while 1:
        line_cnt+=1
        co = f1.readline()
        ao = f2.readline()
        if not co:
            break
        if co=='\n' and line_cnt==len(f1.readlines()):
            break
        co=co.rstrip()
        ao=ao.rstrip()
        if(co!=ao):
            return False
    return True