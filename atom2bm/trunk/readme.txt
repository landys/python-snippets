atom2bm

从google notebook中导出的标准的Atom格式文件, 转化成bookmark html文件, 可导入到delicious中.

程序的入口是atom2bm.py.
usage: python atom2bm.py input-atom-xml output-bookmark-html
eg. python atom2bm.py "c:\my-atom.xml" "c:\my-bookmark.html"

setup.py是py2exe生成单个exe文件的脚本, 生成之后的exe有2.68M.
直接执行python setup.py py2exe生成.

程序在Windows XP x86上执行通过. eclipse 3.3.2上使用Pydev插件开发. python 2.5标准库开发。