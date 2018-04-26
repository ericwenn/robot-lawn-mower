from Queue import Queue
from command_listener import CommandListener
from gps_analyzer import GPSAnalyzer
import time


def start():
    q = Queue()
    probe_Q = Queue()
    cl = CommandListener(8085, q, probe_Q)
    ga = GPSAnalyzer(q, probe_Q)


    cl.start()
    ga.start()

if __name__ == "__main__":
   
    start()
    time.sleep(100)

