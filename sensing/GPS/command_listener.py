from threading import Thread, Event
from Queue import Queue, Empty
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json


def make_handler(queue, probe_Q):
    class Webserver(BaseHTTPRequestHandler):
        def do_POST(self):
            
            command = self.path[1:]
            queue.put(command)
            if(command == "probe"):
                print"Waiting"
                resp = probe_Q.get()
                print"Done"
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(resp)
            else:
                self.send_response(200)
        
        def log_message(self, format, *args):
            return
    return Webserver



class WebserverThread(Thread):
    def __init__(self, queue, probe_Q, port):
        Thread.__init__(self)
        self.queue = queue
        self.port = port
        self.probe_Q = probe_Q

    def run(self):
        server_address = ('', self.port)
        httpd = HTTPServer(server_address, make_handler(self.queue,self.probe_Q))
        httpd.serve_forever()


class CommandListener(object):
    def __init__(self, port=8080, queue=None, probe_Q=None):
        self.thread = WebserverThread(queue, probe_Q, port)
        self.isStarted = False

    def start(self):
        if self.isStarted:
            raise Exception("CommandListener already started")
        self.thread.daemon = True
        self.thread.start()
        self.isStarted = True
        print "CommandListener started"
