from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep, path
import glob
import subprocess
import datetime
from threading import Thread
import time

DIR = 'stored_images'
VARIANTS = 3
PORT_NUMBER = 8080


#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

    def index(self):
        pictures = list(set(glob.glob(DIR+"/*")))
        pictures.sort(reverse=True)

        print "found", len(pictures)

        html = '<html><head><title>Webhost</title></head><body>'
        for pic in pictures[:10]:
          basepath = pic.split('/')[-1]
          html += '<img style="width:30%" src="'+basepath+'"/>'
          
        html += '</body></html>'
        return html


    def log_message(self, format, *args):
              return


	#Handler for the GET requests
    def do_GET(self):
        if self.path=="/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.index())
            return


        try:
        #Check the file extension required and
        #set the right mime type
            print self.path
            sendReply = False
            if self.path.endswith(".html"):
            	mimetype='text/html'
            	sendReply = True
            if self.path.endswith(".jpg"):
            	mimetype='image/jpg'
            	sendReply = True
            if self.path.endswith(".gif"):
            	mimetype='image/gif'
            	sendReply = True
            if self.path.endswith(".js"):
            	mimetype='application/javascript'
            	sendReply = True
            if self.path.endswith(".css"):
            	mimetype='text/css'
            	sendReply = True

            if sendReply == True:
            	#Open the static file requested and send it
            	f = open(curdir + sep + DIR + sep + self.path)
            	self.send_response(200)
            	self.send_header('Content-type',mimetype)
            	self.end_headers()
            	self.wfile.write(f.read())
            	f.close()
            return


        except IOError:
        	self.send_error(404,'File Not Found: %s' % self.path)


class CameraVisualizerThread(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.port = port

    def run(self):
        print "run", self.port
        server_address = ('', self.port)
        httpd = HTTPServer(server_address, myHandler)
        httpd.serve_forever()


class CameraVisualizer(object):
  def __init__(self, port=8080):
      self.thread = CameraVisualizerThread(port)


  def start(self):
      self.thread.daemon = True
      self.thread.start()


if __name__ == "__main__":
  camera_vis = CameraVisualizer()
  camera_vis.start()

  while(True):
    time.sleep(0.5)