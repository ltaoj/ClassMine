import os
import sys

from urllib.request import urlretrieve
from selenium import webdriver

from contants import CONFIG
from zips import UnzipFactory

# find driver path
def find_driver(name, path='..'):
    print('searching file %s from %s' % (name, path))
    for filename in os.listdir(path):
        print(filename)
        cur_dir = os.path.join(path, filename)
        if os.path.isfile(cur_dir) and name == filename:
            return cur_dir
        if os.path.isdir(cur_dir):
            return find_driver(name, cur_dir)
    print('not found %s' % name)
    return ""

# will down the driver from the default source
# and return the path of phantomjs if success
def download_driver():
    path = ''
    sources = CONFIG.PHANTOMJS_SOURCES
    for source in sources:
        name = source.split('/')[-1]
        dir_path = os.getcwd()
        dir_zip = os.path.join(dir_path, name)
        print('downloading %s from %s...' % (name, source))
        print('please wait a moment...')
        try:
            urlretrieve(source, name)
            print('download successfully')
            print('saved file %s to %s' % (name, dir_path))
            print('unziping...')
            status = UnzipFactory.create_unzip(dir_zip).unzip()
            if status == 0:
                raise Exception("download driver failed")
            print('unzip successfully')
            print('starting find %s\'path' % CONFIG.PHANTOMJS_NAME)
            dir_path = find_driver(CONFIG.PHANTOMJS_NAME, os.path.join(dir_path, name.replace('.tar.bz2', '')))
            if dir_path == "":
                raise Exception("not found driver path, place find it by hand then modify the value of PHANTOMJS_PATH at file contants/CONFIG.py")
            print('found driver %s at %s' % (CONFIG.PHANTOMJS_NAME, dir_path))
            os.remove(dir_zip)
            print('removed %s' % dir_zip)
            path = dir_path
            break
        except BaseException as e:
            print(e)
    return path

# path: the phantomjs path
# if path is specified, then load driver from the path
# but if the path is not specified, then download the library
# from net, then unzip it and get the tmp path
# will return the driver if load successfully
def load_driver():
    path = CONFIG.PHANTOMJS_PATH
    if path == '':
        path = download_driver()
    
    if path == '':
        print('no driver path available, exit with code 1')
        sys.exit(1)
    
    print('load driver successfully')
    return webdriver.PhantomJS(path)

# abstract login class
# return webdriver
class Login(object):

    def login(self, username, password):
        pass

# login with verify code
class CodeLogin(Login):
    
    def login(self, username, password):
        load_driver()

# login without verify code
class NormalLogin(Login):
    
    def login(self, username, password):
        pass

class Context(object):
    
    def __init__(self, login):
        self.__login = login

    def login(self, username, password):
        return self.__login.login(username, password)
