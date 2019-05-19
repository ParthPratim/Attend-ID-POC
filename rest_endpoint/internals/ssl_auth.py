import pickle
import struct
import os
from OpenSSL import crypto, SSL

def CreateServerCertAndKey():
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)

    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = "IN"
    cert.get_subject().ST = "Karnataka"
    cert.get_subject().L = "Banglore"
    cert.get_subject().O = "AttendID"
    cert.get_subject().OU = "BroCode Inc."
    cert.get_subject().CN = "localhost"
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*6)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')

    return {"cert":cert,"key":k}

def CreateUserCertAndKey(uname):
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)

    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().CN = uname
    sn = ""
    for i in struct.unpack('IIIIIII', os.urandom(28)):
        sn = sn + str(i)
    cert.set_serial_number(int(sn))
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*6)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')
    #return {"Object":cert,"cert":crypto.dump_certificate(crypto.FILETYPE_PEM, cert) , "key" :  crypto.dump_privatekey(crypto.FILETYPE_PEM, k)}
    return {"cert" : cert , "key" : k}



def create_cert(deviceCsr,CAprivatekey):
    cert = crypto.X509()
    cacert = crypto.X509()
    cert.set_serial_number(1)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*6)
    cacert.get_subject().C = "IN"
    cacert.get_subject().ST = "Karnataka"
    cacert.get_subject().L = "Banglore"
    cacert.get_subject().O = "AttendID"
    cacert.get_subject().OU = "BroCode Inc."
    cacert.get_subject().CN = "localhost"
    cert.set_issuer(cacert.get_subject())
    cert.set_subject(deviceCsr.get_subject())
    cert.set_pubkey(deviceCsr.get_pubkey())
    cert.sign(CAprivatekey, "sha256")
    return cert

"""
server = CreateServerCertAndKey()
open("../../keys/ssl/server.pem","wb").write(crypto.dump_certificate(crypto.FILETYPE_PEM, server['cert']))
open("../../keys/ssl/server.key","wb").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, server['key']))
pk = crypto.PKCS12()
pk.set_certificate(server['cert'])
pk.set_privatekey(server['key'])
open("server.p12","wb").write(pk.export())

x = 1000
for uname in ["Alice","Bob"]:
    client = CreateUserCertAndKey(uname,x)
    x = x+1000
    cert = create_cert(client["cert"],server['key'])
    pk = crypto.PKCS12()
    pk.set_certificate(cert)
    pk.set_privatekey(client['key'])
    open(uname+".pem","wb").write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    open(uname+".key","wb").write(crypto.dump_privatekey(crypto.FILETYPE_PEM, client['key']))
    open(uname+".p12","wb").write(pk.export())
"""
