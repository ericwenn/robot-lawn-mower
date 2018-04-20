from threading import Thread, Event
from Queue import Queue, Empty
import time
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import commands

def make_handler(command_queue, position_queue):
  class Webserver(BaseHTTPRequestHandler):
    def do_POST(self):
      if self.path == '/config/position':
        try:
          while True:
            pos = position_queue.get(block=False)
        except Empty:
          pass
        self.send_response(pos)
        return

      if self.path == '/config/left':
        command_queue.put(commands.LEFT)
      if self.path == '/config/right':
        command_queue.put(commands.RIGHT)
      if self.path == '/config/forward':
        command_queue.put(commands.FORWARD)
      if self.path == '/config/backward':
        command_queue.put(commands.BACKWARD)
      if self.path == '/config/stop':
        command_queue.put(commands.STOP)

      if self.path == '/config/config_on':
        command_queue.put(commands.CONFIG_ON)
      if self.path == '/config/config_off':
        command_queue.put(commands.CONFIG_ON)

      if self.path == '/config/probe':
        command_queue.put(commands.PROBE)
      self.send_response(200)
    
    def log_message(self, format, *args):
      return
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


class ConfigListener(object):
  def __init__(self, port=8080):
    self.command_queue = Queue()
    self.position_queue = Queue()
    self.port = port
    self.thread = WebserverThread(self.command_queue, self.position_queue, port)
    self.isStarted = False

    self.command = None
    self.config_mode = False

  def start(self):
    if self.isStarted:
      raise Exception("ConfigListener already started")
    self.thread.daemon = True
    self.thread.start()
    self.isStarted = True
    print "ConfigListener now listening on port", self.port

  def register_position(self, position):
    self.position_queue.put(position)

  def last_command(self):
    try:
      while True:
        command = self.command_queue.get(block=False)
        if command == commands.CONFIG_ON:
          self.config_mode = True
        
        if command == commands.CONFIG_OFF:
          self.config_mode = False
        self.command = command
    except Empty:
      pass
    
    if not self.config_mode:
      return None
    
    return self.command
  