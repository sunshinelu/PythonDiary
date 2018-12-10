# -*- coding: utf-8 -*-

"""
参考链接：
Flask使用日志记录到文件示例
https://www.polarxiong.com/archives/Flask%E4%BD%BF%E7%94%A8%E6%97%A5%E5%BF%97%E8%AE%B0%E5%BD%95%E5%88%B0%E6%96%87%E4%BB%B6%E7%A4%BA%E4%BE%8B.html
"""

from flask import Flask
import logging

app = Flask(__name__)


@app.route('/')
def root():
    app.logger.info('info log')
    app.logger.warning('warning log')
    return 'hello'

if __name__ == '__main__':
    app.debug = True
    handler = logging.FileHandler('flask.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    app.run()