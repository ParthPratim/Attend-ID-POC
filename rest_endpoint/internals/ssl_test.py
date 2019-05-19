import os
import ssl

from tornado.web import Application, RequestHandler , HTTPServer
from tornado.ioloop import IOLoop


ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_ctx.load_cert_chain("server.pem", "server.key")

class HelloHandler(RequestHandler):
  def get(self):
    self.write({'message': 'hello world'})

def make_app():
  urls = [("/", HelloHandler)]
  return Application(urls)

if __name__ == '__main__':
    app = make_app()
    http = HTTPServer(app,ssl_options=ssl_ctx)
    http.listen(3000)
    IOLoop.instance().start()
