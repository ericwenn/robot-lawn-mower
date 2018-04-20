from threading import Thread, Event
from Queue import Queue, Empty
import time
import json
import httplib
import dd_conv

class AnalyzerThread(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue
    
    def send(self,coord,verdict):
        conn = httplib.HTTPConnection("cmg-navigating", "8080")
        body = json.dumps({ 'coord': coord,'isInside': verdict })
        try:
            conn.request("POST", "/gps", body, { 'Content-Type': 'application/json' })
        except:
            pass
            
    def run(self):
        while True:
            self.send(str(dd_conv.getDDconv()), str(dd_conv.check_if_inside()))
            time.sleep(0.1)
            try:
                cmd = self.queue.get(block=False)
                if(cmd == "probe"):
                    dd_conv.save_point()
                elif(cmd == "enter_config"):
                    dd_conv.setup_config(True)
                elif(cmd == "exit_config"):
                    dd_conv.setup_config(False)
                
            except Empty:
                pass
            
            time.sleep(0.5)

    

class GPSAnalyzer(object):
    def __init__(self, queue=None):
        self.thread = AnalyzerThread(queue)
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
