from threading import Thread, Event
from Queue import Queue, Empty
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json


def make_handler(queue):
    class Webserver(BaseHTTPRequestHandler):
        def do_POST(self):
            
            command = self.path[1:]
            queue.put(command)                
            self.send_response(200)
        
        def log_message(self, format, *args):
            return
    return Webserver



class WebserverThread(Thread):
    def __init__(self, queue, port):
        Thread.__init__(self)
        self.queue = queue
        self.port = port

    def run(self):
        server_address = ('', self.port)
        httpd = HTTPServer(server_address, make_handler(self.queue))
        httpd.serve_forever()


class CommandListener(object):
    def __init__(self, port=8080, queue=None):
        self.thread = WebserverThread(queue, port)
        self.isStarted = False

    def start(self):
        if self.isStarted:
            raise Exception("CommandListener already started")
        self.thread.daemon = True
        self.thread.start()
        self.isStarted = True
        print "CommandListener started"
