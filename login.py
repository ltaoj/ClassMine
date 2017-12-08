from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup
import subprocess
import time
from selenium import webdriver
import re
from PIL import Image

# image为必须参数，可以为url地址或本地文件路径
# image为本地路径时download参数需为False
# download参数默认为True
def getImageCode(image,download=True):
    if download:
        urlretrieve(image, "code.jpg")
        p = subprocess.Popen(["tesseract", "code.jpg", "code"], 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        p = subprocess.Popen(["tesseract", image, "code"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    f = open("code.txt", "r")
    code = f.read()
    code = re.sub('(\n|\t|\r| )+', "", code)
    return code


driver = webdriver.PhantomJS('./lib/phantomjs')
driver.get("http://csujwc.its.csu.edu.cn/")

time.sleep(3)
# 输入账号密码
driver.find_element_by_id("userAccount").send_keys("123456789")
driver.find_element_by_id("userPassword").send_keys("password")

# 点击更换验证码
#driver.find_element_by_id("SafeCodeImg").click()
#time.sleep(1)
# 获取验证码链接
#image = driver.find_element_by_id("SafeCodeImg").get_attribute("src")
#print("code url is " + image)

# 原先是通过src属性链接来获取图片，因为在下载时会重新请求后台，
# 导致页面上的验证码和下载的不一致，所以改为截屏获取验证码图片
driver.save_screenshot('screenshot.png')
elem = driver.find_element_by_id("SafeCodeImg")
left = elem.location['x']
top = elem.location['y']
right = elem.location['x'] + elem.size['width']
bottom = elem.location['y'] + elem.size['height']

# 截取验证码
im = Image.open('screenshot.png')
im = im.crop((left, top, right, bottom))
im.save('screenshot1.png')

# OCR识别验证码内容
code = getImageCode('./screenshot1.png', False)
print("code is " + code)
driver.find_element_by_id("RANDOMCODE").send_keys(code)

# 页面提交前内存浏览器快照
driver.save_screenshot('screenshot2.png')
driver.find_element_by_id("btnSubmit").click()
time.sleep(3)

# 重定向后页面内容
print(driver.page_source)
driver.close()
