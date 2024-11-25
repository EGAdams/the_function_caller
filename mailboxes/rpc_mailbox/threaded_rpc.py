from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn

class ThreadingXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass
