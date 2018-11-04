# -*- coding: utf-8 -*-

"""

参考链接：
https://dev.to/aligoren/building-basic-restful-api-with-flask-restful-57oh

测试：
postman中，get方法输入以下链接：
http://127.0.0.1:5000/
"""

# -*- coding: utf-8 -*-

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Quotes(Resource):
    def get(self):
        return {
            'ataturk': {
                'quote': ['Yurtta sulh, cihanda sulh.', 'Egemenlik verilmez, alınır.',
                          'Hayatta en hakiki mürşit ilimdir.']
            },
            'linus': {
                'quote': ['Talk is cheap. Show me the code.']
            }

        }


api.add_resource(Quotes, '/')

if __name__ == '__main__':
    app.run(debug=True)