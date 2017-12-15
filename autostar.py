#!/usr/bin/python2
import abc
import argparse
import time
import os
import sys
import requests
from bs4 import BeautifulSoup
from requests.auth import HTTPBasicAuth
import settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class StarBase(object):
    __metaclass__ = abc.ABCMeta
    count = 0

    def __init__(self, cookie, auth, scorer, sleep_time=5):
        self.cookie = cookie
        self.auth = auth
        self.scorer = scorer
        self.sleep_time = sleep_time

    @property
    def counter(self):
        self.count += 1
        time.sleep(self.sleep_time)
        return self.count

    @abc.abstractmethod
    def run(self):
        return None


class Star(StarBase):
    def projects_list(self):
        url = "http://gitstar.top:88/api/users/%s/status/recommend" % settings.NAME
        response = requests.get(url, headers={'Accept': 'application/json',
                                              'Cookie': self.cookie})
        if response.status_code != 200:
            return []
        result = response.json()
        return [r['Repo'] for r in result if r.get('scoreR') < self.scorer]

    def star(self, project_name):
        res = requests.put("https://api.github.com/user/starred/" + project_name,
                           headers={'Content-Length': '0'}, auth=self.auth)

        print("[%d]Stared  %s! --> %s" % (self.counter, 'OK' if res.ok else 'Failure', project_name))

    def update_gitstar(self):
        url = "http://gitstar.top:88/star_update"
        res = requests.get(url, headers={'Accept': 'application/json', 'Cookie': self.cookie})
        print "update: %s" % str(res.status_code == 200)

    def run(self):
        projects = self.projects_list()
        print "Get total github project count:%d" % len(projects)
        for project_name in projects:
            self.star(project_name)
        if len(projects) > 0:
            self.update_gitstar()


class Floolw(StarBase):
    def projects_list(self):
        url = "http://gitstar.top:88/follow"
        response = requests.get(url, headers={'Accept': 'application/json', 'Cookie': self.cookie})
        if response.status_code != 200:
            return []
        bs = BeautifulSoup(response.text, "html.parser")
        jsn = bs.find_all("div", class_="media")
        projects = []
        for obj in jsn:
            try:
                projects.append(obj.find('a')['href'].replace("https://github.com/", ""))
            except Exception as e:
                pass
        return projects

    def follow(self, project_name):
        res = requests.put("https://api.github.com/user/following/%s" % project_name,
                           headers={'Content-Length': '0'}, auth=self.auth)
        print("[%d]Followed  %s! --> %s" % (self.counter, 'OK' if res.ok else 'Failure', project_name))

    def update_gitstar(self):
        url = "http://gitstar.top:88/follow_update"
        res = requests.get(url, headers={'Accept': 'application/json', 'Cookie': self.cookie})
        print "update: %s" % str(res.status_code == 200)

    def run(self):
        projects = self.projects_list()
        print "get total github repo:%d" % len(projects)
        for project_name in projects:
            self.follow(project_name)
        if len(projects) > 0:
            self.update_gitstar()


class Fork(StarBase):
    def projects_list(self):
        url = "http://gitstar.top:88/api/users/%s/status/fork-recommend" % settings.NAME
        response = requests.get(url, headers={'Accept': 'application/json', 'Cookie': self.cookie})
        if response.status_code != 200:
            return []
        result = response.json()
        return [r['Repo'] for r in result if r.get('scoreR') < self.scorer]

    def fork(self, project_name):
        res = requests.post("https://api.github.com/repos/%s/forks" % project_name,
                            headers={'Content-Length': '0'},
                            auth=self.auth)
        print("[%d]Forked  %s! --> %s" % (self.counter, 'OK' if res.ok else 'Failure', project_name))

    def update_gitstar(self):
        url = "http://gitstar.top:88/api/users/%s/forking-repos/update" % settings.NAME
        res = requests.get(url, headers={'Accept': 'application/json', 'Cookie': self.cookie})
        print "update: %s" % str(res.status_code == 200)

    def run(self):
        projects = self.projects_list()
        print "get total github repo:%d" % len(projects)
        for project_name in projects:
            self.fork(project_name)
        if len(projects) > 0:
            self.update_gitstar()


class Gitstar(object):
    def __init__(self):
        parser = argparse.ArgumentParser(description='Star up automatically')
        parser.add_argument("--target",
                            default=['star', 'follow', 'fork'],
                            nargs='*',
                            help="Set operation target, <'star|follow|fork> default all",
                            choices=['star', 'follow', 'fork'])
        parser.add_argument("-r", "--scoreR", type=int, default=10,
                            help="Set scoreR maximum,  default 10")
        parser.add_argument("-s", "--sleep-time", type=int, default=5,
                            help="Set sleep time,  default 5")
        self.parser = parser
        self.cookie = self.login_gitstar()
        self.auth = HTTPBasicAuth(settings.GITNAME, settings.GITPASSWORD)

    def login_gitstar(self):
        r = requests.post("http://gitstar.top:88/api/user/login",
                          params={'username': settings.NAME, 'password': settings.PASSWORD})
        return r.headers['Set-Cookie']

    def autorun(self, argv):
        args = self.parser.parse_args(argv)
        for target in args.target:
            print '%s START --> %s' % (target.upper(), time.asctime(time.localtime(time.time())))
            class_map = {'star': Star,
                         'follow': Floolw,
                         'fork': Fork}
            class_ = class_map[target]
            object_ = class_(self.cookie, self.auth, args.scoreR, args.sleep_time)
            object_.run()


def main(argv=sys.argv[1:]):
    app = Gitstar()
    app.autorun(argv)


if __name__ == '__main__':
    sys.exit(main())
