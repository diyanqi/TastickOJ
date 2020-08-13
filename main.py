from judge import *
# cpp_run(path,pro_num)
from flask import *
import json
from flask_cors import *
from queue import Queue,LifoQueue,PriorityQueue
import time
import login
from datetime import datetime, timedelta
import coins_ctrl
import difflib
from online_idle import *
import shutil
import os
import glob
import paiming

q = Queue(maxsize=0) #测评
idle_q = Queue(maxsize=0) #在线IDLE
stid = 0
not_invited = '''
     <html>   <head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <title>Tastick OJ - 后台管理</title>
  <link rel="stylesheet" href="//cdn.jsdelivr.net/npm/mdui@1.0.0/dist/css/mdui.min.css"/>
</head><body>
        <script src="//cdn.jsdelivr.net/npm/mdui@1.0.0/dist/js/mdui.min.js"></script>
        <script>
        mdui.snackbar({
  message: '啊哦，你无权查看此界面，还是回去做题吧',
  buttonText: '好吧',
  onClick: function(){
    location.href='/problem/list?page=1';
  },
  onButtonClick: function(){
    location.href='/problem/list?page=1';
  },
  onClose: function(){
    location.href='/problem/list?page=1';
  }
});</script></body></html>
        '''

def is_admin(user):
    return json.loads(read_file_as_str("users.json"))[user]['is_admin']
    # print(json.loads(read_file_as_str("users.json")))
    # return True

def addst(task,user,info):
    global stid
    stid+=1
    j = json.loads(read_file_as_str("serverst.json"))
    j[str(stid)]={"id":stid,"task":task,"user":user,"info":info}
    with open('serverst.json',"w") as file:
        file.write(json.dumps(j))

def f2s(file_path):
    # 判断路径文件存在
    if not os.path.isfile(file_path):
        raise TypeError(file_path + " does not exist")

    all_the_text = open(file_path).read()
    # print type(all_the_text)
    return all_the_text

def save_to_file(file_name, contents):
    fh = open(file_name, 'w')
    fh.write(contents)
    fh.close()

def get_file_info():
    DIR='html/problem/topics/'
    return int(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])/2)

def problem_file(file_dir,page):
    problems={"problem_id":"href"}
    start_id=(page-1)*15+1000
    end_id=page*15+1000-1
    for i in range(start_id,end_id):
        try:
            f=read_file_as_str('html/problem/topics/'+str(i)+'.json')
            print(file_dir+'/'+str(i)+'.json')
            data=json.loads(f)
            problems[str(i)]=data['title']
        except:
            problems[str(i)]='NotFound'
    return json.dumps(problems)

def dif(str1, str2):
   return difflib.SequenceMatcher(None, str1, str2).quick_ratio()

def to_lower(text):
    low_text = ""
    for c in text:
        if 65 <= ord(c) <= 90:
            c = chr(ord(c) + 32)
        low_text += c
    return low_text

def delete(pid):
    shutil.rmtree('io_data/'+str(pid))
    os.remove('html/problem/topics/'+str(pid)+'.json')

def getiofile(file):
    rt={}
    cnt=0
    for root, dirs, files in os.walk(file):
        for f in files:
            rt[str(f)]=read_file_as_str(os.path.join(root, f))
            cnt+=1
    rt['cnt']=cnt/2
    return json.dumps(rt)

def get_key (dict, value):
    return [k for k, v in dict.items() if v == value]

app = Flask(import_name=__name__)

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "html")#html是个文件夹

@app.route("/tongguozhuce",methods=['POST'])
def tongguozhuce():
    cookie=request.headers['Cookie']
    denghao=cookie.find('=')
    user=cookie[:denghao]
    if is_admin(user):
        data=json.loads(request.get_data(as_text=True))
        username=data['username']
        password=data['password']
        fj=json.loads(read_file_as_str("users.json"))
        fj[username]={"is_admin": False, "id": fj['userids']+1, "password": password, "coins": 0, "level": 0, "qianming": ".", "problems": {"1001": 100}}
        fj['userids']+=1
        print(fj)
        f=open("users.json","w")
        f.write(json.dumps(fj))
        f.close()
        return 'OK'
    else:
        return not_invited

@app.route("/replyforum",methods=['POST'])
def replyforum():
    try:
        cookie=request.headers['Cookie']
        denghao=cookie.find('=')
        user=cookie[:denghao]
        data=json.loads(request.get_data(as_text=True))
        fid=int(data['id'])
        info=data['ta']
        f=json.loads(read_file_as_str("forum/show.json"))
        f[str(fid)]['replies']['num']=int(f[str(fid)]['replies']['num']+1)
        f[str(fid)]['replies'][str(f[str(fid)]['replies']['num'])]={'user':user,"info":info}
        j=open("forum/show.json","w")
        j.write(json.dumps(f))
        j.close()
        return 'OK'
    except:
        return '请先登录'

@app.route("/zhuce",methods=['POST'])
def zhuce():
    data=json.loads(request.get_data(as_text=True))
    username=data['username']
    password=data['password']
    zcf=json.loads(read_file_as_str("zhuceshenhe.json"))
    zcf['num']=zcf['num']+1
    zcf[str(zcf['num'])]={'username':username,"password":password}
    f=open("zhuceshenhe.json","w+")
    f.write(json.dumps(zcf))
    f.close()
    return 'OK'

@app.route("/getforuminfo",methods=['POST'])
def getforuminfo():
    try:
        cookie=request.headers['Cookie']
        denghao=cookie.find('=')
        user=cookie[:denghao]
        data=json.loads(request.get_data(as_text=True))
        fid=int(data['id'])
        return json.dumps(json.loads(read_file_as_str('forum/show.json'))[str(fid)])
    except:
        return '请先登录'

@app.route("/forum")
def forum():
    return send_from_directory(root,"forum.htm")

@app.route("/forums")
def forums():
    return read_file_as_str("forum/show.json")

@app.route("/newforum",methods=['POST'])
def newforum():
    try:
        cookie=request.headers['Cookie']
        denghao=cookie.find('=')
        user=cookie[:denghao]
        data=json.loads(request.get_data(as_text=True))
        info=data['info']
        kind=data['kind']
        print(kind)
        title=data['title']
        if((len(info)<=15 and len(title)<=5)or(kind=='non')):
            return '帖子太水'
        if kind == 'guanshui':
            kind='灌水'
        elif kind == 'tiwen':
            kind='提问'
        elif kind == 'zhanwu':
            kind='站务'
        elif kind == 'jiaocheng':
            kind='教程'
        show=json.loads(read_file_as_str('forum/show.json'))
        fid=int(show['numbers'])+1
        show['numbers']=fid
        show[str(fid)]={'title':title,'user':user,'kind':kind,'info':info,'replies':{'num':0}}
        f=open("forum/show.json","w")
        f.write(json.dumps(show))
        f.close
        return 'OK'
    except:
        return '请先登录'

@app.route("/learn")
def learn():
    return send_from_directory(root,'learn.htm')

@app.route("/delforum",methods=['POST'])
def delforum():
    cookie=request.headers['Cookie']
    denghao=cookie.find('=')
    user=cookie[:denghao]
    if is_admin(user):
        data=json.loads(request.get_data(as_text=True))
        fid=data['id']
        show=json.loads(read_file_as_str('forum/show.json'))
        show.pop(str(fid))
        f=open("forum/show.json","w")
        f.write(json.dumps(show))
        f.close
        return 'OK'
    else:
        return not_invited

@app.route("/uploaddata",methods=['POST'])
def uploaddata():
    cookie=request.headers['Cookie']
    denghao=cookie.find('=')
    user=cookie[:denghao]
    if is_admin(user):
        data=json.loads(request.get_data(as_text=True))
        num=data['num']
        pid=data['id']
        for i in range(1,num+1):
            f=open("io_data/"+str(pid)+'/'+data[str(i)]['name'],"w+")
            f.write(data[str(i)]['data'])
            f.close
        return 'OK'
    else:
        return not_invited

@app.route("/uploadiodata")
def uploadiodata():
    cookie=request.headers['Cookie']
    denghao=cookie.find('=')
    user=cookie[:denghao]
    if is_admin(user):
        return send_from_directory(root,"uploadiodata.htm")
    else:
        return not_invited

@app.route("/xinjian",methods=['POST'])
def xinjian():
    cookie=request.headers['Cookie']
    denghao=cookie.find('=')
    user=cookie[:denghao]
    if is_admin(user):
        data=json.loads(request.get_data(as_text=True))
        pid=int(data['id'])
        f=open('html/problem/topics/'+str(pid)+".json","w+")
        f.write(read_file_as_str("html/problem/topics/sample.json"))
        f.close()
        os.mkdir('io_data/'+str(pid))
        os.mknod('io_data/'+str(pid)+"/1.in")
        os.mknod('io_data/'+str(pid)+"/1.out")
        return 'OK'
    else:
        return not_invited

@app.route("/savepro",methods=['POST'])
def savepro():
    cookie=request.headers['Cookie']
    denghao=cookie.find('=')
    user=cookie[:denghao]
    if is_admin(user):
        data=json.loads(request.get_data(as_text=True))
        pid=int(data['proid'])
        f=open('html/problem/topics/'+str(pid)+".json","w+")
        f.write(json.dumps(data))
        f.close()
        return 'OK'
    else:
        return not_invited

@app.route("/saveiodata",methods=['POST'])
def saveiodata():
    cookie=request.headers['Cookie']
    denghao=cookie.find('=')
    user=cookie[:denghao]
    if is_admin(user):
        data=json.loads(request.get_data(as_text=True))
        file_number=int(data['iodata']['num'])
        iodatas=(data['iodata'])
        pid=int(data['proid'])
        for i in range(1,file_number+1):
            f=open('io_data/'+str(pid)+'/'+str(i)+".in","w+")
            f.write(str(iodatas[str(i)+'.in']))
            f.close()
            f=open('io_data/'+str(pid)+'/'+str(i)+".out","w+")
            f.write(str(iodatas[str(i)+'.out']))
            f.close()
        return 'OK'
    else:
        return not_invited

@app.route("/zhuceshenqing")
def zhuceshenqing():
    cookie=request.headers['Cookie']
    denghao=cookie.find('=')
    user=cookie[:denghao]
    if is_admin(user):
        return read_file_as_str("zhuceshenhe.json")
        return 'OK'
    else:
        return not_invited

@app.route("/addiodata",methods=['POST'])
def addiodata():
    cookie=request.headers['Cookie']
    denghao=cookie.find('=')
    user=cookie[:denghao]
    if is_admin(user):
        data=json.loads(request.get_data(as_text=True))
        inputs=str(data['input'])
        pid=int(data['proid'])
        outputs=str(data['output'])
        file_number=len(glob.glob(pathname='io_data/'+str(pid)+'/*.in')) #获取当前文件夹下个数
        print(file_number)
        f=open('io_data/'+str(pid)+'/'+str(file_number+1)+".in","w+")
        f.write(str(inputs))
        f.close()
        f=open('io_data/'+str(pid)+'/'+str(file_number+1)+".out","w+")
        f.write(str(outputs))
        f.close()
        return 'OK'
    else:
        return not_invited

@app.route("/deliodata",methods=['POST'])
def deliodata():
    cookie=request.headers['Cookie']
    denghao=cookie.find('=')
    user=cookie[:denghao]
    if is_admin(user):
        data=json.loads(request.get_data(as_text=True))
        pid=int(data['proid'])
        ioid=int(data['ioid'])
        try:
            file_number=len(glob.glob(pathname='io_data/'+str(pid)+'/*.in')) #获取当前文件夹下个数
            os.remove('io_data/'+str(pid)+'/'+str(ioid)+'.in')
            os.remove('io_data/'+str(pid)+'/'+str(ioid)+'.out')
            print(ioid,file_number)
            for i in range(ioid,file_number):
                os.rename('io_data/'+str(pid)+'/'+str(i+1)+'.out','io_data/'+str(pid)+'/'+str(i)+'.out')
                os.rename('io_data/'+str(pid)+'/'+str(i+1)+'.in','io_data/'+str(pid)+'/'+str(i)+'.in')
            return 'OK'
        except:
            return 'NotFound'
    else:
        return not_invited

@app.route("/getproio",methods=['POST'])
def getproio():
    cookie=request.headers['Cookie']
    denghao=cookie.find('=')
    user=cookie[:denghao]
    if is_admin(user):
        data=json.loads(request.get_data(as_text=True))
        pid=int(data['id'])
        return getiofile("io_data/"+str(pid)+"/")
    else:
        return not_invited

@app.route("/bs/editproblem")
def edit():
    cookie=request.headers['Cookie']
    denghao=cookie.find('=')
    user=cookie[:denghao]
    if is_admin(user):
        return send_from_directory(root,"edit.htm")
    else:
        return not_invited

@app.route("/del",methods=['POST'])
def delt():
    cookie=request.headers['Cookie']
    denghao=cookie.find('=')
    user=cookie[:denghao]
    if is_admin(user):
        data=json.loads(request.get_data(as_text=True))
        pid=int(data['id'])
        delete(pid)
        return 'OK'
    else:
        return not_invited

@app.route("/back-stage/editproblem")
def editproblem():
    cookie=request.headers['Cookie']
    denghao=cookie.find('=')
    user=cookie[:denghao]
    if is_admin(user):
        return send_from_directory(root,"editproblem.htm")
    else:
        return not_invited

@app.route("/bsproblems",methods=['POST'])
def bsproblems():
    data=json.loads(request.get_data(as_text=True))
    page=int(data['page'])
    problems={"problemid":"title"}
    start_id=(page-1)*30+1000
    end_id=page*30+1000-1
    for i in range(start_id,end_id):
        try:
            f=read_file_as_str('html/problem/topics/'+str(i)+'.json')
            data=json.loads(f)
            problems[str(i)]=data['title']
        except:
            problems[str(i)]='NotFound'
    problems['startid']=start_id
    problems['endid']=end_id
    return json.dumps(problems)

@app.route("/back-stage")
def bs():
    cookie=request.headers['Cookie']
    denghao=cookie.find('=')
    user=cookie[:denghao]
    if is_admin(user):
        return send_from_directory(root,"bs.htm")
    else:
        return not_invited

@app.route("/getpaiming",methods=['POST'])
def pm():
    return paiming.sort()

@app.route("/rank")
def rank():
    return send_from_directory(root,"rank.htm")

@app.route("/fatie")
def fatie():
    return send_from_directory(root,"fatie.htm")

@app.route("/serverst")
def serverst():
    return read_file_as_str("serverst.json")

@app.route("/server-status")
def server_status():
    return send_from_directory(root,"server_status.htm")

@app.route("/tools")
def tools_page():
    return send_from_directory(root,"tools.htm")

@app.route("/search",methods=['POST'])
def search_problem():
    data=json.loads(request.get_data(as_text=True))
    msg=data['text']
    i=999
    find=0
    get_num=0
    rst={}
    while find<=get_file_info():
        i+=1
        try:
            f=json.loads(read_file_as_str('html/problem/topics/'+str(i)+'.json'))
        except:
            pass
        find+=1
        title=f['title']
        if (to_lower(msg) in to_lower(title))or(dif(msg,title)>=0.5):
            get_num+=1
            rst[str(get_num)]={'id':i,'title':f['title']}
    return json.dumps(rst)

@app.route("/send_msg",methods=['POST'])
def send_msg():
    data=json.loads(request.get_data(as_text=True))
    msg=data['msg']
    cookie=request.headers['Cookie']
    denghao=cookie.find('=')
    user=cookie[:denghao]
    t=json.loads(read_file_as_str('talks_info.json'))
    mymsg=user+'：'+msg
    ret={'1':mymsg}
    cnt=1
    for i in t.keys():
        cnt+=1
        if cnt>15:
            break
        ret[str(cnt)]=t[i]
    # print(ret)
    f='talks_info.json'
    with open(f,"w") as file:   #”w"代表着每次运行都覆盖内容
        file.write(json.dumps(ret))
    return 'OK'

@app.route("/talks",methods=['POST','GET'])
def talks():
    return read_file_as_str('talks_info.json')

@app.route("/talk")
def talk():
    return send_from_directory(root,"talk.htm")

@app.route("/has_login")
def has_login():
    try:
        cookie=request.headers['Cookie']
        denghao=cookie.find('=')
        user=cookie[:denghao]
        return "True"
    except:
        return "False"

@app.route("/lists",methods=['POST'])
def lists():
    data=json.loads(request.get_data(as_text=True))
    page=int(data['page'])
    return problem_file('html/problem/topics',page)

@app.route("/problem/list")
def problem_list():
    return send_from_directory(root,'list.htm')

@app.route("/help")
def help():
    return send_from_directory(root,'help.htm')

@app.route("/me_img")
def me_jpg():
    return send_from_directory(root,'img/me.jpg')

@app.route('/tologin',methods=['POST'])
def login_handler():
    data=json.loads(request.get_data(as_text=True))
    if login.yanzheng(data['username'],data['password']):
        resp = Response("success")
        resp.set_cookie(data['username'],str(time.time()),max_age=360000)
        return resp
    else:
        return '登陆失败'


@app.route("/get_cookie")
def get_cookie():
    cookie_1 = request.cookies.get("diyanqi")
    return cookie_1

@app.route('/login')
def login_page():
    return send_from_directory(root,"login.htm")

@app.route('/')
def home():
    return send_from_directory(root, "index.htm")

@app.route('/idle-test',methods=['POST'])
def idle_test():
    cookie=request.headers['Cookie']
    denghao=cookie.find('=')
    user=cookie[:denghao]
    test_id=time.time()
    idle_q.put(test_id)
    while(idle_q.queue[0]!=test_id):
        pass
    data = request.json
    inputtext=data["input"]
    code=data["code"]
    code_type=data["code_type"]
    save_to_file('online_idle/code.cpp',code)
    save_to_file('online_idle/code.in',inputtext)
    return_data=onlineCodeRun(code='online_idle/code.cpp',codesh='online_idle/code.sh',inputfile='online_idle/code.in',outputfile='online_idle/code.out',clog='online_idle/log.txt')
    idle_q.get()
    return jsonify(return_data)

@app.route('/online-idle')
def online_idle():
    return send_from_directory(root, "online-idle.htm")

@app.route('/problem')
def problem():
    return send_from_directory(root, "problem/index.htm")

@app.route('/topics/',methods=["POST"])
def problem_json():
    data=json.loads(request.get_data(as_text=True))
    pro_id=int(data['pro_id'])
    return send_from_directory(root,'problem/topics/'+str(pro_id)+'.json')

@app.route('/img/pro_img.jpg')
def img():
    return send_from_directory(root, "img/pro_img.jpg")

@app.route('/get_my_coins')
def get_my_coins():
    cookie=request.headers['Cookie']
    denghao=cookie.find('=')
    user=cookie[:denghao]
    return str(coins_ctrl.get_user_coins(user))

@app.route('/me')
def my_page():
    return send_from_directory(root,"me.htm")

@app.route('/get_my_level')
def my_level():
    cookie=request.headers['Cookie']
    denghao=cookie.find('=')
    user=cookie[:denghao]
    return str(coins_ctrl.get_user_coins(user))

@app.route('/whatsmyname')
def myname():
    try:
        cookie=request.headers['Cookie']
        denghao=cookie.find('=')
        user=cookie[:denghao]
        return user
    except:
        return 'NeedLogin'

@app.route('/procodetest', methods = ["POST"])
@cross_origin()
def judge_code():
    cookie=request.headers['Cookie']
    denghao=cookie.find('=')
    user=cookie[:denghao]
    test_id=time.time()
    q.put(test_id)
    while(q.queue[0]!=test_id):
        pass
    data = request.json
    pro_num=data['pro_id']
    code=data["code"]
    code_type=data["code_type"]
    save_to_file('caj/code.cpp',code)
    return_data=cpp_run("caj/code.cpp",pro_num,user)
    q.get()
    addst(task="测评代码 <a href='/problem?id="+str(pro_num)+"' class='mdui-btn'>P"+str(pro_num)+"</a>",user=user,info='分数:'+str(return_data['score']))
    return jsonify(return_data)

if __name__ == "__main__":
	app.run(host = "0.0.0.0",port=8080,debug = True)