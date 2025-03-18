# coding: utf-8
# from __future__ import unicode_literals

from setuptools import find_packages, setup

import re
import codecs

from setuptools import find_packages, setup

with codecs.open('__init__.py', encoding='utf-8') as fp:
    content = fp.read()
    version = re.search(r"__version__\s*=\s*'([\w\-.]+)'", content).group(1)
    name = re.search(r"__title__\s*=\s*'([\w\-.]+)'", content).group(1)
setup(
    name=name,
    version=version,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "logging",
        "python-memcached",
        "pyMysql",
        "pymongo",
        "yapf",
        "setproctitle",
        "flask",
        "flask-debugtoolbar",
        "flask-uploads",
        "flask-cache",
        'future',
    ],
    url='https://github.com/jimmydong/YEPY2',
    license='MIT',
    author='JimmyDong',
    author_email='jimmy.dong@gmail.com',
    description='关于本软件的简单描述',
    long_description='这里是详细的描述和使用介绍',
    keywords=[
        'YEPY',
        '简易框架',
        'Server'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
    ]
)