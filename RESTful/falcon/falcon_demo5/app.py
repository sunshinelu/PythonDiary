# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/8/8 上午11:25 
 @File    : app.py
 @Note    : 
 
 """

import falcon
import Test

api = application = falcon.API()
test = Test.Test()
# 添加路由控制
api.add_route('/test', test)

# falcon.API instances are callable WSGI apps
app = create_app()