import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    server = HTTPServer(app)
    server.bind(8888)
    server.start(0) 
    tornado.ioloop.IOLoop.current().start()