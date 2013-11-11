import web

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
		print name
		
if __name__ == "__main__":
    app.run()
