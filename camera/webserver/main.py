#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep, path
import glob
import subprocess
import datetime

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):

    def index(self):
        pictures = list(glob.glob("pictures/*")).sort()
        print pictures
        html = '<html><head><title>Webhost</title></head><body>'

        for pic in pictures:
            basepath = pic.split('/')[-1]
            html += '<img src="'+basepath+'"/>'
        html += '</body></html>';
        return html

    def take_picture(self):
        cmd = "raspistill -w 910 -h 700 -vf -q 20 -o %s/pictures/%s.jpg" % (path.abspath(path.dirname(__file__)), datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        print cmd
        subprocess.Popen(cmd.split())


	#Handler for the GET requests
    def do_GET(self):
        if self.path=="/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.index())
            return

        if self.path=='/shoot':
            self.take_picture()
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('ok')
            return

        try:
        #Check the file extension required and
        #set the right mime type

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
            	f = open(curdir + sep + 'pictures' + sep + self.path)
            	self.send_response(200)
            	self.send_header('Content-type',mimetype)
            	self.end_headers()
            	self.wfile.write(f.read())
            	f.close()
            return


        except IOError:
        	self.send_error(404,'File Not Found: %s' % self.path)

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER

	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
