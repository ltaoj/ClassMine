import os
import sys

from urllib.request import urlretrieve
from selenium import webdriver
from PIL import Image
import re
import time

from contants import CONFIG
from contants import URL
from zips import UnzipFactory

# find driver path
def find_driver(name, path='..'):
    print('searching file %s from %s' % (name, path))
    for filename in os.listdir(path):
        cur_dir = os.path.join(path, filename)
        if os.path.isfile(cur_dir) and name == filename:
            return cur_dir
        if os.path.isdir(cur_dir):
            result = find_driver(name, cur_dir)
            if result != '':
                return result
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
    
    # the way of code login
    # if login success will enter the system
    # return the driver from operations after
    def login(self, username, password):
        driver = load_driver()
        driver.get(URL.LOGIN_PAGE_WITHCODE)
        code_path = self.get_code_image(driver)
        code_result = ''
        if CONFIG.USE_OCR:
            print('use OCR function recognizing, please wait...')
            code_result = recognize_with_ocr(code_path)
            print('OCR recognized result is:%s' % code_result)
        else:
            print('don\'t use OCR function, please check the code image at %s' % code_path)
            code_result = input('type in the code you recognized:')
            print('ok, your input is %s' % code_result)
        driver.find_element_by_id(CONFIG.CODE_INPUT_ID).send_keys(code_result)
        driver.find_element_by_id(CONFIG.SUBMIT_BTN_ID).click()

        # wait from redirect page
        time.sleep(3)
        print(driver.page_source)
        print('login successfully')
        return driver

    # screenshot the web page and crop the code image area
    # and save the code image
    # will return the code image path
    def get_code_image(driver):
        print('screenshot the web page...')
        driver.save_screenshot(CONFIG.SCREENSHOT_NAME)
        print('screenshot completed')
        elem = driver.find_element_by_id(CONFIG.CODE_IMAGE_ID)
        left = elem.location['x']
        top = elem.location['y']
        right = elem.location['x'] + elem.size['width']
        bottom = elem.location['y'] + elem.size['height']
        print('crop screenshot...')
        im = Image.open(CONFIG.SCREENSHOT_NAME)
        im = im.crop((left, top, right, bottom))
        code_path = os.path.join(os.getcwd() , CONFIG.CODE_IMAGE_NAME)
        im.save(code_path)
        print('saved code image named %s at %s' % (CONFIG_IMAGE_NAME, os.getcwd()))
        os.remove(CONFIG.SCREENSHOT_NAME)
        print('removed %s' % CONFIG.SCREENSHOT_NAME)
        return code_path


    # use ocr lib recognized the code image
    # return the text result
    def recognize_with_ocr(code_path):
        p = subprocess.Popen(['tesseract', code_path, CONFIG.CODE_RECOGNIZED_FILE_NAME],
                stdout.subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        f = open(CONFIG.CODE_RECOGNIZED_FILE_NAME + '.txt', 'r')
        result = f.read()
        result = re.sub('(\n|\t|\r| )', '', result)
        return result

# login without verify code
class NormalLogin(Login):
    
    def login(self, username, password):
        pass

class Context(object):
    
    def __init__(self, login):
        self.__login = login

    def login(self, username, password):
        return self.__login.login(username, password)
