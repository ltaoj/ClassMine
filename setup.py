import os
import re
from setuptools import setup, find_packages

with open('requirements.txt') as reqs_file:
    REQS = reqs_file.read()

setup(
    name='csujwc',
    version='1.0',
    packages=find_packages(exclude=['tests']),
    install_requires=REQS,
    
    package_data={
        '': ['*.txt', '*.rst'],   
    },

    author='ltaoj',
    author_email='taojiangli@foxmail.com',
    description='中南大学教务管理系统抢课软件',
    license='MIT',
    keywords='csujwc',
    url='https://www.ltaoj.cn',
)
