# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/8/7 上午9:33 
 @File    : run.py
 @Note    : 
 
 """

"""
将python项目进行打包

使用
pyinstaller --onefile --add-data 'templates:templates' single_flaskapp.py 
打包

测试：
curl http://127.0.0.1:5000/123

参考链接：
ciscomonkey/flask-pyinstaller 《https://github.com/ciscomonkey/flask-pyinstaller》
"""
import sys
import os
from flask import Flask, render_template

if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    app = Flask(__name__, template_folder=template_folder)
else:
    app = Flask(__name__)


@app.route('/')
@app.route('/<name>')
def hello_world(name=None):
    return render_template('hello.html', name=name)


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True) # host='0.0.0.0' 使服务器外部可见