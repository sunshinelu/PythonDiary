# -*- coding: utf-8 -*-

"""
 @Author  : sunlu 
 @Date    : 19/8/9 下午1:03
 @File    : falcon_api.py
 @Note    : 
 
 """
import json
from wsgiref import simple_server

import falcon
from falcon_multipart.middleware import MultipartMiddleware

# from falcon_require_https import RequireHTTPS
# 数据库
from MySQL_conn import *
# 预处理
from data_preprocess import *

# 数据统计

# 算法库

# 模型库

# NLP


class JSONTranslator(object):
    # NOTE: Starting with Falcon 1.3, you can simply
    # use req.media and resp.media for this instead.

    def process_request(self, req, resp):

        # req.stream corresponds to the WSGI wsgi.input environ variable,
        # and allows you to read bytes from the request body.
        #
        # See also: PEP 3333
        if req.content_length in (None, 0):
            # Nothing to do
            return

        body = req.bounded_stream.read()
        if not body:
            raise falcon.HTTPBadRequest('Empty request body',
                                        'A valid JSON document is required.')

        try:
            req.context.doc = json.loads(body.decode('utf-8'))
            # req.name = req.get_param('name')

        except (ValueError, UnicodeDecodeError):
            raise falcon.HTTPError(falcon.HTTP_753,
                                   'Malformed JSON',
                                   'Could not decode the request body. The '
                                   'JSON was incorrect or not encoded as '
                                   'UTF-8.')
    """ 
    def process_response(self, req, resp, resource):
        if not hasattr(resp.context, 'result'):
            return

        resp.body = json.dumps(resp.context.result)
    """


# 预处理
class PreProcess(object):

    def on_post(self, req, resp):
        """
        :param req: HTTP请求
        :param resp: 对应请求的HTTP响应
        :return:
        """
        rtn = dict()
        # 获取HTTP请求参数
        try:
            doc = req.context.doc
            # name = req.name
            sql_type_dict = {
                'mysql': MySQL,  # mysql数据库
                # 'oscar': Oscar  # 神通数据库
            }
            if doc['input_sql_url']['sql_type'] in sql_type_dict.keys():
                input_sql_url = doc['input_sql_url']
                input_sql_type = sql_type_dict[doc['input_sql_url']['sql_type']](input_sql_url['username'],
                                                                                 input_sql_url['password'],
                                                                                 input_sql_url['host'],
                                                                                 input_sql_url['database'])


                output_sql_url = doc['output_sql_url']
                output_sql_type = sql_type_dict[doc['output_sql_url']['sql_type']](output_sql_url['username'],
                                                                                   output_sql_url['password'],
                                                                                   output_sql_url['host'],
                                                                                   output_sql_url['database'])

                rtn['Code'], rtn['Mesg'] = data_preprocess(input_sql_type,
                                                           output_sql_type,
                                                           doc['temp_table'],
                                                           doc['new_table'],
                                                           doc['process'],
                                                           doc['params'])

        except Exception as e:
            rtn['Code'] = 1
            rtn['Mesg'] = str(e)

        rtn['Data'] = ''

        # 返回未加密的json结果
        resp.body = json.dumps(rtn, ensure_ascii=False)
        resp.content_type = falcon.MEDIA_JSON

        # 返回状态
        resp.status = falcon.HTTP_200


# 算法库

# 模型应用

# 模型评估



def create_app():
    # 数据预处理
    preprocess = PreProcess()

    api = falcon.API(middleware=[MultipartMiddleware(), JSONTranslator(), ])

    # 数据预处理
    api.add_route('/v2.0/preprocess', preprocess)

    return api


# falcon.API instances are callable WSGI apps
app = create_app()

if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0', 8080, app)
    httpd.serve_forever()
