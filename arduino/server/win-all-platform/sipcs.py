#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
import os
import serial
import time

arduino = None

op = [ False for i in range(20)]

#Create custom HTTPRequestHandler class
class sipcs_server(BaseHTTPRequestHandler):
    
    #handle GET command
    def do_GET(self):
        #rootdir = 'c:/xampp/htdocs/' #file location
        try:
			self.send_response (200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			#self.wfile.write ("<br>SIPCS aSimple IP/Control System</br>")
		
			#template info
			f = open ("index.html")
			html = f.read()
			
			if self.path.find('d') > 0:
				number = self.path.split ('=')
				print number[1]
				
				#we got a value, we need to do something
				
				if arduino != None:
					arduino.write (chr(int(number[1])))
					value = arduino.read (20)
					value = value[0:20]
					for x in value:
						if ord(x) < 100:
							op[ord(x)] = False
						if ord(x) > 100:
							op[ord(x)-101] = True	
							 
					#print op
			
			for x in range(20):
				if op[x] == True:
					html = html.replace('value="'+str(x)+'" CSSH', 'value="'+str(x)+'" class="control enable"')
				else:
					html = html.replace('value="'+str(x)+'" CSSH', 'value="'+str(x)+'" class="control"')
			#html.replace("CSSH", 'class="control"')
			self.wfile.write (html)
			f.close()
			return
            #if self.path.endswith('.html'):
			'''
         		f = open(rootdir + self.path) #open requested file

                #send code 200 response
                self.send_response(200)

                #send header first
                self.send_header('Content-type','text-html')
                self.end_headers()

                #send file content to client
                self.wfile.write(f.read())
                f.close()
                return'''
            
        except IOError:
            self.send_error(500, 'SIPCS Internal System Error')
    
def init():
    print('[INFO] SIPCS server starting ..')

    #ip and port of servr
    #by default http server port is 80
    server_address = ('127.0.0.1', 80)
    httpd = HTTPServer(server_address, sipcs_server)
    print('[INFO] SIPCS server is running')
    httpd.serve_forever()
    
if __name__ == '__main__':
 print "[INFO] Connecting to SIPCS controller"
 try:
	arduino = serial.Serial('COM21', 9600)
 except:
	print "[Error] Error connecting to SIPCS controller"
	exit()
 time.sleep (2)
 print "[INFO] Waiting for firmware to boot"
 msg = "nothing"
 while "SIPCS READY" not in msg:
	msg = arduino.readline ()
	print "[RX] "+msg
 print "[INFO] SIPCS Controller ready"
 
 try:
    init()
 except KeyboardInterrupt:
	print "[INFO] Closing"