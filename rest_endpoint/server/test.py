import tornado.ioloop
import tornado.web
import tornado.escape
from tornado.httpserver import HTTPServer

class MainHandler(tornado.web.RequestHandler):
    def post(self):
        print((len(self.request.files['filename'])))
        print((self.get_body_argument("folder_id", default=None, strip=False)))

        self.write("Hello, world")

def setup_app():
    return tornado.web.Application([
        (r"/", MainHandler)
    ])

def server_init():
    app = setup_app()
    server = HTTPServer(app)
    server.bind(6667)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()

server_init()
