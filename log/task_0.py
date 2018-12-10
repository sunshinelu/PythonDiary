# -*- coding: utf-8 -*-

from flask import Flask
import logging
from logging import Formatter, FileHandler

app = Flask(__name__)



@app.route('/')
def hello_world():
    app.logger.debug('second test message...')
    return 'Hello World!'


if __name__ == '__main__':
    #Setup the logger
    file_handler = FileHandler('output.log')
    handler = logging.StreamHandler()
    file_handler.setLevel(logging.DEBUG)
    handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
     ))
    handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
     ))
    app.logger.addHandler(handler)
    app.logger.addHandler(file_handler)
    app.logger.error('first test message...')
    app.run(debug=True)