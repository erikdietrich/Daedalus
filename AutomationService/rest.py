import web

from CM19aDriver import CM19aDevice

REFRESH = 1.0               # Refresh rate (seconds) for polling the transceiver for inbound commands

urls = (
  '/', 'index',
  '',  'index',
  '/office/(on|off)', 'office')

app = web.application(urls, globals())
  
class index:
	def GET(self):
		print "Hello, world!"
		
class office:
	def GET(self, name):
		cm19a = CM19aDevice()       # Initialise device. Note: auto receiving in a thread is turned off for this example
		if cm19a.initialised:
			result = cm19a.send('A', '1', name)
			result = cm19a.send('A', '2', name)
			result = cm19a.send('A', '3', name)
			result = cm19a.send('A', '4', name)
			result = cm19a.send('A', '5', name)
			result = cm19a.send('A', '6', name)
			result = cm19a.send('A', '7', name)
			result = cm19a.send('A', '8', name)
		else:
			print "Error initialising the CM19a...exiting..."
		
		cm19a.finish()
if __name__ == "__main__":
    app.run()
