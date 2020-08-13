import json
import os
def read_file_as_str(file_path):
    # 判断路径文件存在
    if not os.path.isfile(file_path):
        raise TypeError(file_path + " does not exist")

    all_the_text = open(file_path).read()
    # print type(all_the_text)
    return all_the_text

def user_post(user,problem_id,chengji):
    data=json.loads(read_file_as_str('users.json'))
    try:
        if data[user][str(problem_id)]==100:
            return True
    except:
        pro_data=json.loads(read_file_as_str('html/problem/topics/'+str(problem_id)+'.json'))
        data[user]['problems'][str(problem_id)]=chengji
        with open('html/problem/topics/'+str(problem_id)+'.json',"w") as file:
            file.write(json.dumps(pro_data))
        with open('users.json',"w") as file:
            file.write(json.dumps(data))
        return False