import json
import os
def read_file_as_str(file_path):
    # 判断路径文件存在
    if not os.path.isfile(file_path):
        raise TypeError(file_path + " does not exist")

    all_the_text = open(file_path).read()
    # print type(all_the_text)
    return all_the_text

def get_user_coins(user):
    try:
        data=json.loads(read_file_as_str('users.json'))
        return data[user]['coins']
    except:
        return -1

def add_user_coins(user,num):
    try:
        data=json.loads(read_file_as_str('users.json'))
        data[user]['coins']=data[user]['coins']+num
        with open('users.json',"w") as file:
            file.write(json.dumps(data))
        return data[user]['coins']
    except:
        return -1