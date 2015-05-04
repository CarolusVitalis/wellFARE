from __future__ import print_function
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import argparse
import re
import cgi
import json


import wellfare.json_api




class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):	
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', "http://localhost")#'http://iae-spring.upmf-grenoble.fr') # needs to be changed
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-type")
	
    def do_POST(self):

        command = self.path.split('/')[-1]

        # parse data from client
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

        if ctype == 'application/json':

            length = int(self.headers.getheader('content-length'))
            data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
            input_data = json.loads(data['json'][0])
            
            output_data = wellfare.json_api.json_process(command, input_data)
            
            #except AssertionError as err:
            #    self.send_response(500, "Internal server error: %s"%err.message)
            #else:
                # send results to client
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', "http://localhost")#'http://iae-spring.upmf-grenoble.fr')			
            self.end_headers()

            json_output_data = json.dumps(output_data)
            self.wfile.write(json_output_data)

        else:

            self.send_response(
                400, "Bad Request: 'Content-Type: application/json' expected in POST query")
            self.send_header('Content-Type', 'application/json')
            self.end_headers()


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True

    def shutdown(self):
        self.socket.close()
        HTTPServer.shutdown(self)


class SimpleHttpServer():

    def __init__(self, ip, port):
        self.server = ThreadedHTTPServer((ip, port), HTTPRequestHandler)

    def start(self):
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def wait_for_thread(self):
        self.server_thread.join()

    def stop(self):
        self.server.shutdown()
        self.waitForThread()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='HTTP Server')
    parser.add_argument('port', type=int,
                        help='Listening port for HTTP Server')
    parser.add_argument('ip', help='HTTP Server IP')
    args = parser.parse_args()

    server = SimpleHttpServer(args.ip, args.port)
    print ('HTTP Server Running...........')
    server.start()
    server.wait_for_thread()
