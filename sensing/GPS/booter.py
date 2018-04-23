from Queue import Queue
from command_listener import CommandListener
from gps_analyzer import GPSAnalyzer
import time


def start():
    q = Queue()
    cl = CommandListener(8085, q)
    ga = GPSAnalyzer(q)


    cl.start()
    ga.start()

if __name__ == "__main__":
   
    start()
    time.sleep(5000)

