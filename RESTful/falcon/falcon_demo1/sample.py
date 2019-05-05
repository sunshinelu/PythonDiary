import falcon

"""
source activate python36
pip install falcon
cd /Users/sunlu/Workspaces/PyCharm/PythonDiary/RESTful/falcon/falcon_demo1
gunicorn sample:api

postman中使用get方法，输入"http://127.0.0.1:8000/quote"
"""
class QuoteResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        quote = {
            'quote': (
                "I've always been more interested in "
                "the future than in the past."
            ),
            'author': 'Grace Hopper'
        }

        resp.media = quote

api = falcon.API()
api.add_route('/quote', QuoteResource())