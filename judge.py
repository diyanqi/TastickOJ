import os
import filecmp
import time
import run_cpp
import coins_ctrl
import problem_set

def read_file_as_str(file_path):
    # 判断路径文件存在
    if not os.path.isfile(file_path):
        raise TypeError(file_path + " does not exist")

    all_the_text = open(file_path).read()
    # print type(all_the_text)
    return all_the_text

def get_file_info(pro_num):
    DIR='io_data/'+str(pro_num)
    return int(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])/2)

def file_judge(code_out_path,ac_out_path):
    return filecmp.fcmp(code_out_path,ac_out_path)

def py_run(path):
    pass

def cpp_run(path,pro_num,username):
    os.system('g++ caj/code.cpp -o caj/code.sh 2> caj/complinglog.txt')
    # os.system('g++ -Wall -Werror caj/code.cpp -o caj/code.sh &> caj/complinglog.txt')
    if not os.path.isfile('caj/code.sh'):
        rst={'log':read_file_as_str('caj/complinglog.txt')}
        return rst
    pro_info=get_file_info(pro_num)
    score=0
    rst={'log':'OK','score':0,'testpoints':{1:{'time':0,'status':'AC'}}}
    rst['testsnum']=pro_info
    for i in range(pro_info):
        try:
            time_start=time.time()
            rt=run_cpp.run(pro_num,i+1)
            time_end=time.time()
        except:
            rst['testpoints'][(i+1)]['time']=-1
            rst['testpoints'][(i+1)]['status']='LTE'
            continue
        rst['testpoints'][(i+1)]={'time':0,'status':'AC'}
        if rt==-1:
            rst['testpoints'][(i+1)]['time']=-1
            rst['testpoints'][(i+1)]['status']='RE'
            continue
        if file_judge('caj/code.out','io_data/'+str(pro_num)+'/'+str(i+1)+'.out'):
            score+=1
            rst['testpoints'][(i+1)]['time']=round(time_end-time_start,3)
            rst['testpoints'][(i+1)]['status']='AC'
        else:
            rst['testpoints'][(i+1)]['time']=round(time_end-time_start,3)
            rst['testpoints'][(i+1)]['status']='WA'
            exptd=read_file_as_str('io_data/'+str(pro_num)+'/'+str(i+1)+'.out')
            yrt=read_file_as_str('caj/code.out')
            rst['testpoints'][(i+1)]['expected']=exptd
            rst['testpoints'][(i+1)]['your_out']=yrt
    rst['score']=int(score/pro_info*100)
    has_ac = problem_set.user_post(username,pro_num,int(score/pro_info*100))
    if (has_ac) and (score==pro_info):
        coins_ctrl.add_user_coins(username,100)
    open('caj/out.txt','w').truncate()
    os.remove('caj/code.sh')
    return rst