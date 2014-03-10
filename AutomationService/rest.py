import web
import json
from index import Index

from CM19aDriver import CM19aDevice

REFRESH = 1.0               # Refresh rate (seconds) for polling the transceiver for inbound commands

jsonFile = open('house.json', 'r')
jsonData = json.load(jsonFile)
jsonFile.close()
route = jsonData["rooms"][0]["path"]
print route

urls = (
  '/', 'Index',
  '/(.*?)', 'Index',
  '',  'Index',
  '/office/(on|off)', 'office',
  '/room', 'room_redirect',
  '/room/(.*?)', 'room',
  route + '/(.*?)', "dynamic")

app = web.application(urls, globals())
  

class room_redirect: #This is temporary
	def GET(self):
		raise web.seeother('/room/')
		
class room: # This is temporary
    def GET(self, name):
        print "User asked for rooms list."
    def PUT(self, name):
        print "User tried to put " + name

class office: #This is temporary and will be moved to a light controller
	def GET(self, name):
		cm19a = CM19aDevice()       # Initialise device. Note: auto receiving in a thread is turned off for this example
		if cm19a.initialised:
			result = cm19a.send('A', '1', name)
		else:
			print "Error initialising the CM19a...exiting..."
		
		cm19a.finish()

class dynamic:
	def GET(self): # Show all lights in this room
		print "User wants all lights in room " + web.ctx.path
	def PUT(self, nameOfLight): # This is going to be how users add lights to a room
		print "Request to add light named " + nameOfLight + " to room " +	 web.ctx.path
	def POST(self, nameOfLight, state): #This is going to be how users turn lights on and off 
		print "User wants to set light " + nameOfLight + " in room " + web.ctx.path + " to state " + state


if __name__ == "__main__":
    app.run()
