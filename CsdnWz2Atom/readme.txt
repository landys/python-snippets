CsdnWz2Atom

从CSDN网摘抓取某个帐号数据, 转化成标准的Atom格式文件, 可以导入到google notebook中.

程序的入口是cw2atom.py.
usage: python cw2atom.py csdn-username gmail notebook-title result-atom-xml
eg. python cw2atom.py tonywjd tonywjd@gmail.com "csdn bookmarks" "c:\tonywjd-atom.xml"

setup.py是py2exe生成单个exe文件的脚本, 生成之后的exe有3.37M.
直接执行python setup.py py2exe生成.

程序在Windows XP x86上执行通过. eclipse 3.3.2上使用Pydev插件开发.
Python 2.5.2. 使用的第三方python库中Cheetah-2.0.1, pytz 2008i.