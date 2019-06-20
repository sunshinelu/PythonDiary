import falcon
from werkzeug.serving import run_simple

app = falcon.API()  #instance


class HelloViewAPI:

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = "text/plain"
        resp.body = "Hello World!"

hobj = HelloViewAPI()

app.add_route('/hello', hobj)


if __name__ == '__main__':
    run_simple('0.0.0.0', 5000, app, use_reloader=True)