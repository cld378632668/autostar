Engish [here](README.md)
# GitAutoFork
gitstar自动点fork工具
# 快速入门
## Linux
### Step1
安装python2.x

安装pip, 从 这里下载[get-pip.py](https://bootstrap.pypa.io/get-pip.py)

接着运行:

> python get-pip.py

安装依赖

> pip install -r requirements.txt

### Step2
打开```settings.py```,替换以下内容  
```
#############settings#############
NAME		= "1" #GitStar用户名
PASSWORD	= "1" #GitStar密码
GITNAME		= "1" #github用户名
GITPASSWORD	= "1" #github密码
#############settings#############
```
把它们改成你自己的信息。  

### Step 3
运行 ```python2 gitstar.py --help See``` 查看帮助
```
usage: gitstar.py [-h]
                  [--target [{star,follow,fork} [{star,follow,fork} ...]]]
                  [-r SCORER] [-s SLEEP_TIME]

Star up automatically

optional arguments:
  -h, --help            show this help message and exit
  --target [{star,follow,fork} [{star,follow,fork} ...]]
                        Set operation target, <'star|follow|fork> default all
  -r SCORER, --scoreR SCORER
                        Set scoreR maximum, default 10
  -s SLEEP_TIME, --sleep-time SLEEP_TIME
                        Set sleep time, default 5
```
运行```python2  gitstar.py```  
Everything is ok,hooray!

### Step 4 (可选的)
设置定时任务

crontab -e

例子:

50 13 * * 1,3,5 /usr/bin/python2 /home/knitmesh/tools/gitstar/autostar.py >> /home/knitmesh/tools/gitstar/gitstar.log  2>&1

## Windows
我好久没用过Windows了~    
你可以百度一下```windows python2.x安装教程```看看，祝你好运！:)