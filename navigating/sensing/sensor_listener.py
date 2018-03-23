from threading import Thread, Event
from Queue import Queue, Empty
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import json


def make_handler(gps_queue, camera_queue):
    class Webserver(BaseHTTPRequestHandler):
        def do_POST(self):
            length = int(self.headers.getheader('content-length'))
            data = self.rfile.read(length)
            parsed_data = {
                'payload': json.loads(data),
                'timestamp': time.time()
            }

            if self.path == '/camera':
                camera_queue.put(parsed_data)
            if self.path == '/gps':
                gps_queue.put(parsed_data)
            self.send_response(200)
    return Webserver



class WebserverThread(Thread):
    def __init__(self, gps_queue, camera_queue, port):
        Thread.__init__(self)
        self.gps_queue = gps_queue
        self.camera_queue = camera_queue
        self.should_exit = Event()
        self.port = port

    def run(self):
        server_address = ('', self.port)
        httpd = HTTPServer(server_address, make_handler(self.gps_queue, self.camera_queue))
        httpd.serve_forever()


class SensorListener(object):
    def __init__(self, port=8080):
        self.gps_queue = Queue()
        self.gps_stack = []
        self.camera_queue = Queue()
        self.camera_stack = []
        self.port = port
        self.thread = WebserverThread(self.gps_queue, self.camera_queue, port)
        self.isStarted = False

    def start(self):
        if self.isStarted:
            raise Exception("SensorListener already started")
        self.thread.daemon = True
        self.thread.start()
        self.isStarted = True
        print "SensorListener now listening on port", self.port

    def get_camera_events(self, n=1):
        # Read all events from sensors
        try:
            while True:
                event = self.camera_queue.get(block=False)
                self.camera_stack.append(event)
        except Empty:
            pass

        return self.camera_stack[-n:]

    def get_gps_events(self, n=1):
        # Read all events from sensors
        try:
            while True:
                event = self.gps_queue.get(block=False)
                self.gps_stack.append(event)
        except Empty:
            pass

        return self.gps_stack[-n:]
