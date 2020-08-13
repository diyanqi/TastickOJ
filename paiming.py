import json
import os

def read_file_as_str(file_path):
    # 判断路径文件存在
    if not os.path.isfile(file_path):
        raise TypeError(file_path + " does not exist")

    all_the_text = open(file_path).read()
    # print type(all_the_text)
    return all_the_text

def sort():  
    users=json.loads(read_file_as_str("users.json"))
    ul=[]
    ret={}
    for key in users:
        user_level=users[key]['level']
        ul.append({"user":key,"level":user_level})
    ul.sort(key = lambda x:x["level"])
    cnt=0
    for i in range(len(ul)-1,-1,-1):
        cnt+=1
        ret[str(cnt)]={"user":ul[i]['user'],"level":ul[i]['level']}
    return json.dumps(ret)