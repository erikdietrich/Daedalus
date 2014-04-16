import web
import json
import sys

sys.path.append('/var/www/lights')

from CM19aDriver import CM19aDevice

urls = (
	'/lights/(.*?)/(on|off)', 'Lights',
	'/lights/(.*?)', 'Lights',
	'/lights', 'Lights'
	)

application = web.application(urls, globals()).wsgifunc()

class Lights:

	FILE_STORE_PATH = '/var/www/lights/house.json'

	def __init__(self):
		try:
			open(self.FILE_STORE_PATH, 'r')
		except IOError:
			self.createDefaultJsonStore()

	def GET(self, lightId = None):
		web.header('Content-Type','application/json')
		if(lightId is None):
			return json.dumps(self.retrieveLightsFromStore())
		else:
			return json.dumps(self.getMatchingLight(lightId))

	def POST(self):
		newLight = json.loads(web.data())
		fullJson = self.retrieveLightsFromStore()
		currentLights = fullJson['lights']
		currentLights.append(newLight)
		self.writeLightsToStore(fullJson)

	def DELETE(self, lightId):
		jsonData = self.retrieveLightsFromStore()
		updatedLights = [light for light in jsonData['lights'] if light['lightId'] != lightId]
		jsonData['lights'] = updatedLights
		self.writeLightsToStore(jsonData)

	def PUT(self, lightId, command):
		
		matchingLight = self.getMatchingLight(lightId)

		cm19a = CM19aDevice()
		result = cm19a.send(matchingLight['houseCode'], matchingLight['unitCode'], command)
		cm19a.finish()

	def getMatchingLight(self, lightId):
		jsonInStore = self.retrieveLightsFromStore()
		matchingLight = next(node for node in jsonInStore['lights'] if node['lightId'] == lightId)
		return matchingLight

	def retrieveLightsFromStore(self):
		jsonFile = open(self.FILE_STORE_PATH, 'r')
		jsonData = json.load(jsonFile)
		jsonFile.close()
		return jsonData

	def writeLightsToStore(self, pythonJson):
		with open(self.FILE_STORE_PATH, 'w') as jsonFile:
			jsonFile.write(json.dumps(pythonJson))

	def createDefaultJsonStore(self):
		jsonFile = open(self.FILE_STORE_PATH, 'w+')
		defaultJson = json.dumps({"lights":[]})
		jsonFile.write(defaultJson)


if __name__ == '__main__':
  app.run()
