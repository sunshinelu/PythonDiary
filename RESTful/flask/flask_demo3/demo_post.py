# -*- coding: utf-8 -*-

"""

参考链接：
https://dev.to/aligoren/building-basic-restful-api-with-flask-restful-57oh
"""

from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()

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


    def post(self):
        parser.add_argument('quote', type=str)
        args = parser.parse_args()

        return {
            'status': True,
            'quote': '{} added. Good'.format(args['quote'])
        }



api.add_resource(Quotes, '/')

if __name__ == '__main__':
    app.run(debug=True)