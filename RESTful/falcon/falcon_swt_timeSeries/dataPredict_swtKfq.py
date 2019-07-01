#!/usr/bin/python
#-*-coding:utf-8-*-
'''
Created on 2019-06-24 17:43
@author:wangrs
@note:时间序列预测模型训练或加载已有模型并预测接口（商务厅开发区数据）
'''
'''
{
"input_sql_url":{
    "host":"172.23.7.174",
    "port":"3306",
    "user":"root",
    "passwd":"root",
    "database":"swt"
    },
"table_info":{
    "table":"analysis_data",
    "Kfqnum":12,
    "Zd":"M1",
    "value_column":"Zdsj_0",
    "Nian_min":2014,
    "Nian_max":2019  
   },
    "modelpath":"d:/model/arima",
    "params_train":[5,5],
    "params_predict":[2],
    "model_isExist":0   
}
'''

import mysql.connector
from sklearn.externals import joblib
from pyramid.arima import auto_arima
import numpy as np
import falcon
import json
from wsgiref import simple_server

def data_preprocessing(input_sql_url,table_info):
    '''
    :param input_sql_url:
    :param table_info:
    :return:result
    '''
    mydb = mysql.connector.connect(
        host = input_sql_url["host"],
        port = input_sql_url["port"],
        user = input_sql_url["user"],
        passwd = input_sql_url["passwd"],
        database = input_sql_url["database"]
    )
    mycursor = mydb.cursor()
    mycursor.execute("select CONCAT(Nian,'.',Yue) as date ,{value_column}  from {table} where Kfqnum= {Kfqnum} and Zd= '{Zd}' and Nian>={Nian_min} and Nian <= {Nian_max} ORDER BY Nian,Yue"
                     .format(value_column=table_info["value_column"],table=table_info["table"],Kfqnum=table_info["Kfqnum"],Zd=table_info["Zd"],Nian_min=table_info["Nian_min"],Nian_max=table_info["Nian_max"]))
    result = mycursor.fetchall()  # fetchall() 获取所有记录
    return result

# 训练arima时序模型并预测
def arima_train_predict(train_df, modelpath, params_train,params_predict):
    """
    :param modelpath:
    :param params_train:
    :return:
    """
    model = auto_arima(train_df,
                          max_p=int(params_train[0]),
                          max_q=int(params_train[1]), trace=True,
                          error_action='ignore', suppress_warnings=True)
    joblib.dump(model, modelpath, compress=1)
    preds = model.predict(n_periods=params_predict[0])
    return preds

# 加载arima时序模型并预测
def arima_load_predict(modelpath, params_predict):
    """
    :param modelpath:
    :param params_train:
    :return:
    """
    model = joblib.load(modelpath)
    preds = model.predict(n_periods=params_predict[0])
    return preds

class JSONTranslator(object):
    # NOTE: Starting with Falcon 1.3, you can simply
    # use req.media and resp.media for this instead.
    def process_request(self, req, resp):
        # req.stream corresponds to the WSGI wsgi.input environ variable,
        # and allows you to read bytes from the request body.
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

# 数据预测
class DataPredict(object):
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
            input_sql_url = doc['input_sql_url']
            table_info = doc['table_info']
            model_isExist = doc['model_isExist']
            if model_isExist == 0:
                result = data_preprocessing(input_sql_url,table_info)
                data_ndarray = np.array(result)
                #训练arima模型并预测
                rtn['preds'] = list(arima_train_predict(data_ndarray[:, 1],
                              doc['modelpath'],
                              doc['params_train'],
                              doc['params_predict']))
            elif model_isExist == 1:
                # 加载arima模型并预测
                rtn['preds'] = list(arima_load_predict(doc['modelpath'],
                                                        doc['params_predict']))
            else:
                rtn['ModelError'] = "'model_isExist' parameter value is wrong!"

        except Exception as e:
            rtn['Code'] = 1
            rtn['Mesg'] = str(e)

        # 返回未加密的json结果
        resp.body = json.dumps(rtn, ensure_ascii=False)
        resp.content_type = falcon.MEDIA_JSON
        # 返回状态
        resp.status = falcon.HTTP_200

def create_app():
    swtDataPredict = DataPredict()
    api = falcon.API(middleware=[JSONTranslator()])
    api.add_route('/swt/timeSeries/swtDataPredict', swtDataPredict)
    return api

app = create_app()

if __name__ == '__main__':
    httpd = simple_server.make_server('0.0.0.0',8802,app)
    httpd.serve_forever()
