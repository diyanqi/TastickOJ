# TastickOJ
基于python的轻量OJ——'全新界面'为做题带来不一样的体验！

### ~~小声BB:小学生爆肝100+小时开发水作很不容易的！~~ [StarIt!]

### Linux-Ubuntu 安装方案  
##### - 视频教程：https://www.bilibili.com/video/bv1vp4y1q7ce 同时也诠释了下文为什么难以使用80端口。（可以使用nginx端口转发） 
##### - 一键安装并运行： https://github.com/diyanqi/TastickOJ-Installer
-这里以Ubuntu20.04LTS（WSL）为例。
1. 您首先应当更换国内源，保证接下来的下载数据能100%可靠。
  - 更换apt-get源。请自行百度，因为不同的系统会有不同的操作。
2. 查看是否已预装了g++、python3和git。
- 在终端输入以下命令：
```bash
g++
```
- 看看终端的返回结果，如果是：
```bash
g++: fatal error: no input files
compilation terminated.
```
- 则表明已安装了g++编译器。否则请自行百度安装。
- 再输入以下命令：
```bash
python3
```
- 看看会不会有以下 __类似__ 的信息：
```bash
Python 3.8.2 (default, Apr 27 2020, 15:53:34)
[GCC 9.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```
- ~~TIP:您可以按下CTRL+D退出这个交互式界面，返回bash。~~
- 若有类似信息，则说明已安装，否则请自行百度安装。
- 您的python版本可能不是3.8.2，不过请保证python版本至少为3.7+（包括3.7），3.6可能会有未知错误。
- 检查是否安装了GIT。
- 运行以下命令：
```bash
git
```
- 看看会不会涌现出一大堆信息，如下（只复制了一小部分上来）：
```bash
usage: git [--version] [--help] [-C <path>] [-c <name>=<value>]
           [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
           [-p | --paginate | -P | --no-pager] [--no-replace-objects] [--bare]
           [--git-dir=<path>] [--work-tree=<path>] [--namespace=<name>]
           <command> [<args>]

These are common Git commands used in various situations:
```
- ~~省略N行……~~
3. git克隆TastickOJ代码库
- 运行命令：
```bash
git clone https://github.com/diyanqi/TastickOJ/
```
- 您可能需要等待1分钟时间（最慢的时候），因为GitHub的服务器远在国外，速度会有点慢。
- 但相比较其他笨重的项目，这个速度已经是很快的了。
- 过了一段时间（大约也就30秒钟），您会看到以下信息（在下载过程中是变化的，不过运行完成后是固定的）：
```bash
Cloning into 'TastickOJ'...
remote: Enumerating objects: 101, done.
remote: Counting objects: 100% (101/101), done.
remote: Compressing objects: 100% (56/56), done.
remote: Total 101 (delta 16), reused 92 (delta 13), pack-reused 0
Receiving objects: 100% (101/101), 345.11 KiB | 22.00 KiB/s, done.
Resolving deltas: 100% (16/16), done.
```
- 现在，TastickOJ已经下载到了您当前的目录里了。
- 请不要cd到其它目录，只需输入以下命令：
```bash
cd TastickOJ
```
- 您的命令前缀便改成了：
```bash
用户名@电脑名:~/TastickOJ$
```
- 如果您下载时的目录不是~/，此目录可能会改变，但您需要保证最后一个/的后面是“TastickOJ”。
- 用户名 以及 电脑名 的部分因设备而异。
4. 准备环境&运行
- 您已安装好了python，查看pip功能是否能正常使用。
- 运行以下命令：
```bash
pip3
```
- 您可能会看到：
```bash
Command 'pip3' not found, but can be installed with:
sudo apt install python3-pip
```
- 那么就运行：
```
sudo apt install python3-pip
```
- 在此过程中可能会要求您输入密码
- 当出现“您希望继续执行吗？ [Y/n]”的提示时，按下回车即可。
- 等待安装pip3
- 若安装失败，如以下信息：
```bash
E: 有几个软件包无法下载，要不运行 apt-get update 或者加上 --fix-missing 的选项再试试？
```
- 请您尝试运行：
```bash
sudo apt-get install python3-pip --fix-missing
```
- 或者
```bash
sudo apt-get upgrade
```
- 等待完成，运行以下命令检测是否安装成功：
```
pip3
```
- 若成功，又会返回一大堆数据：
```
Usage:
  pip3 <command> [options]

Commands:
  install                     Install packages.
  download                    Download packages.
```
- 省略了N行。
- 确认安装成功，逐行运行以下命令：
```bash
pip3 install timeout_decorator -i https://pypi.tuna.tsinghua.edu.cn/simple
pip3 install flask -i https://pypi.tuna.tsinghua.edu.cn/simple
pip3 install flask_cors -i https://pypi.tuna.tsinghua.edu.cn/simple
```
- __TIP：是pip3而不是pip，因为这是Linux而不是Windows__
- 等待安装完成后，输入以下命令：
```
python3 main.py
```
- 此时又分为两种情况，我们向您分别说明。
- 1. 报错，最后一行出现
```
ModuleNotFoundError: No module named 'XXXXX'
```
- 其中XXXXX是名称。
- 解决方法:
- 运行命令：
```
pip3 install XXXXX -i https://pypi.tuna.tsinghua.edu.cn/simple
```
- 其中XXXXX是你刚刚报错的名称，替换进去，但不要包含单引号'
```
E.G.：出现ModuleNotFoundError: No module named 'timeout_decorator'
您需要运行命令：
pip3 install timeout_decorator -i https://pypi.tuna.tsinghua.edu.cn/simple
```
- 您可能会有多个库没有安装，手动执行以上命令直到能运行为止。
- 2. 运行成功，出现：
```
* Serving Flask app "main" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 334-787-378
```
- 恭喜！安装成功！在与此主机的同一局域网内用浏览器打开 主机IP地址+:8080 即可访问！
- 如：你的主机ip为192.168.9.11，只需访问 http://192.168.9.11:8080/ 。
- 为查看主机IP，你可以运行以下命令：
```
ifconfig
```
- 您可以在一大堆信息中找到形如
```
inet 192.168.9.11
```
- 的内容。依次尝试其中的IP地址+:8080的端口。总有一个是可以用的。

# IMPORTANT   defualtAdminUsername:admin         Password:admin

5. 后期开发与配置
- TastickOJ采用Mozilla2.0协议。
- 当服务器被访问资源时，您会在控制台看到相应的信息。
- **修改端口号和调试模式**：
- 服务器默认是调试模式的，但这会有一点缺陷，比如，服务器已经告诉我们：
```
WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
```
- 找到main.py，最后一行：
```python
app.run(host = "0.0.0.0",port=8080,debug = True)
```
- 请不要修改host，不然会导致服务器无法运行。
- 修改port=的值，比如80，这是http的默认端口，那意味着您在访问服务器时不需要加端口号，但这可能会使一些系统无法正常运行此OJ。
- 修改debug=的布尔值为False，使得服务器取消调试模式。

# 最后，感谢使用此OJ系统的教练以及OIer们，愿你们都能**AKIOI**！
