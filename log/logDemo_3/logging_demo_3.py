# -*- coding: utf-8 -*-

"""
参考链接：
第四期 · 简单了解logging模块 ：结合Flask理解和使用try……except与logging模块
https://zhuanlan.zhihu.com/p/23682543
"""

from flask import Flask
import logging

app = Flask(__name__)

# 日志系统配置
handler = logging.FileHandler('app.log', encoding='UTF-8')
logging_format = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)


@app.route('/')
def index():
    try:
        no_thing = []
        i = no_thing[0]  # 这里会报错，因为列表根本是空的
        return 'Hello!'
    except Exception, e:
        app.logger.error('%s', e)
        # app.logger.exception(e)
        # logging.exception(e)



if __name__ == '__main__':
    app.run()