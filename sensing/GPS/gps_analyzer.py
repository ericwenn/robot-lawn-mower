from threading import Thread, Event
from Queue import Queue, Empty
import time
import json
import httplib
import dd_conv

class AnalyzerThread(Thread):
  def __init__(self, queue, probe_Q):
    Thread.__init__(self)
    self.queue = queue
    self.probe_Q = probe_Q
    try:
      dd_conv.load_file("config_data.conf")
      self.configured = True
    except:
      self.configured = False
    
  def send(self,coord,verdict):
    conn = httplib.HTTPConnection("cmg-navigating", "8080")
    if(self.configured):
      body = json.dumps({ 'coord': coord,'isInside': verdict, 'configured' : True})
    else:
      body = json.dumps({ 'coord': coord,'isInside': None, 'configured' : False})
    try:
        conn.request("POST", "/gps", body, { 'Content-Type': 'application/json' })
        conn.getresponse()
    except Exception as e:
      pass
            
  def run(self):
    while True:

      try:
        conv = dd_conv.getDDconv()
      except Exception:
        conv = None
      try:
        inside = dd_conv.check_if_inside()
      except Exception:
        inside = None
      self.send(conv, inside)

      try:
        cmd = self.queue.get(block=False)
        if(cmd == "probe"):
          print "Got Probe"
          save = dd_conv.save_point()
          self.probe_Q.put(json.dumps({ 'coord': save,'isInside': None, 'configured' : False}))
          print "hello"
        elif(cmd == "enter_config"):
          print "Got enter_config"
          dd_conv.setup_config(True)
        elif(cmd == "exit_config"):
          print "got exit_config"
          dd_conv.setup_config(False)
          self.configured = True
      except Exception as e:
        pass
      
      time.sleep(0.05)

    

class GPSAnalyzer(object):
  def __init__(self, queue=None, probe_Q=None):
    self.thread = AnalyzerThread(queue,probe_Q)
    self.isStarted = False

  def start(self):
    if self.isStarted:
      raise Exception("CommandListener already started")
    self.thread.daemon = True
    self.thread.start()
    self.isStarted = True
    print "AnalyzerListener started"


if __name__ == '__main__':
  q = Queue()
  ga = GPSAnalyzer(q)

  ga.start()

  time.sleep(1)

  q.put("Hello")

  time.sleep(10)
