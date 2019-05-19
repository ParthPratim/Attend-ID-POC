import tornado.ioloop
import tornado.web
from tornado.httpserver import HTTPServer
from rest_endpoint.orgs.handler import OrgsHandler, OrgInfo
from rest_endpoint.digital_id.handler import DigitalIDHandler
from rest_endpoint.whoisit.globals import GlobalWhoisItHandler
from rest_endpoint.whoisit.org import OrgWhoisItHandler, AttendanceSession
from bigchaindb.asset_logic.orgs import OrgsAssets
from bigchaindb_driver.crypto import generate_keypair
from bigchaindb.utils.bdb_ukey import Key

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

def setup_app():
    return tornado.web.Application([
        (r"/api/v1/core/orgs/tx_connector", OrgsHandler),
        (r"/api/v1/core/digital_id/tx_connector", DigitalIDHandler),
        (r"/api/v1/whoisit/global", GlobalWhoisItHandler),
        (r"/api/v1/whoisit/org", OrgWhoisItHandler),
        (r"/api/v1/org/attendance/new_session", AttendanceSession),
        (r"/api/v1/org/members", OrgInfo),
        (r"/", MainHandler)
    ])

def server_init():
    app = setup_app()
    server = HTTPServer(app)
    server.bind(2020)
    server.start(0)
    tornado.ioloop.IOLoop.current().start()
    #alice = Key("7XnqTVhyCvRtDREoeBJ6KzkEpvAXjrZDYZpyShwNnoFr","3Dzhmj32NnTFh6X2cVmNJAeSbA8QjHxcuieVYL6fd8K1")
    #bob = Key("8Nbp87qX9ft5avP3kbQDgwPdfT1PDTokoVxhhBaWyqth","A4eY5hMm9rqs9ZLDdtyWcYydFkRLcLjqst9Kp8n87QSR")
    #matt = Key("Aa3AQV29yFYMPz6wxG1QzwWMSTh53u3JEDgmoSKaEBrv","ErqehsDCkjYoYLYEkA4rAPU7U3Xynk2bskaNBTEAhayZ")
    #d = OrgsAssets.NewMember("ijklm",alice)
    #d = OrgsAssets.TransferMember("7661a9ee1aebf17a8a315c75d52ec3b2eb922010f9045e49ac913f9fe33d818a",bob,matt)
    #print(d)
