Chinese [here](README_CN.md)
# GitAutoFork
Auto fork for gitstar.cn
## Installation
Install Python 2.x,run```python --version```and```pip```for a test.  

To install pip, securely download [get-pip.py](https://bootstrap.pypa.io/get-pip.py)

Then run the following:

> python get-pip.py

If you have downloaded it,skip the step.  
MAKE SURE that you have installed ```requests```.
> pip install -r requirements.txt

## Usage
### Step 1
Clone the repo  
```git clone https://github.com/acelwiker/GitAutoFork.git && cd GitAutoFork```

### Step 2
Open```settings.py```, replace variables with your own infomation.
```
#############settings#############
NAME		= "1" #GitStar username
PASSWORD	= "1" #GitStar password
GITNAME		= "1" #GitHub username
GITPASSWORD	= "1" #Github password
#############settings#############
```
### Step 3
Run python2 gitstar.py --help
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
Run```python2  gitstar.py```  
Everything is ok,hooray!

### Step 4 (OPTIONAL)
Set timed task

crontab -e

Example:

50 13 * * 1,3,5 /usr/bin/python2 /home/knitmesh/tools/gitstar/autostar.py >> /home/knitmesh/tools/gitstar/gitstar.log  2>&1