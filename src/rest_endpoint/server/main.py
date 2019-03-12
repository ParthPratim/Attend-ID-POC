import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer
from rest_endpoint.orgs.handler import OrgsHandler

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def setup_app():
    return tornado.web.Application([
        (r"/api/v1/core/orgs/tx_connector", OrgsHandler),
    ])

def server_init():
    app = setup_app()
    server = HTTPServer(app)
    server.bind(8888)
    server.start(0) 
    tornado.ioloop.IOLoop.current().start()