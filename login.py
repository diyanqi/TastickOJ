import json
import os

def read_file_as_str(file_path):
    # 判断路径文件存在
    if not os.path.isfile(file_path):
        raise TypeError(file_path + " does not exist")

    all_the_text = open(file_path).read()
    # print type(all_the_text)
    return all_the_text

def yanzheng(username,password):
    try:
        data=json.loads(read_file_as_str('users.json'))
        if(data[username]['password']==password):
            return True
        else:
            return False
    except:
        return False