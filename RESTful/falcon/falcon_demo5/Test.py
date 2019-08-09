# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/8/8 上午11:25 
 @File    : Test.py
 @Note    : 
 
 """

import falcon

class Test(object):
    def on_get(self, req, resp):
        resp.body = '{"message": "Hello world!"}'
        resp.status = falcon.HTTP_200