import web
import json

from CM19aDriver import CM19aDevice

class Lights:

	def __init__(self):
		try:
			open('house.json', 'r')

		except IOError:
			self.createDefaultJson()

	def GET(self): #Return the list of lights
		jsonData = self.getFileJson()
		lights = jsonData['lights']
		web.header('Content-Type', 'application/json')
		return json.dumps(jsonData)

	def POST(self): #Add a new light

		global app

		jsonData = self.getFileJson()
		lights = jsonData['lights']
		newLight = json.loads(web.data())
		lights.append(newLight)

		self.writeFileJson(jsonData)

	def DELETE(self, lightId): #Delete a light
		jsonData = self.getFileJson()
		
		updatedLights = [light for light in jsonData['lights'] if light['lightId'] != lightId]
		jsonData['lights'] = updatedLights

		self.writeFileJson(jsonData)

	def PUT(self, lightId, command):
		cm19a = CM19aDevice()
		jsonData = self.getFileJson()
		light = next(node for node in jsonData['lights'] if node['lightId'] == lightId)

		result = cm19a.send(light['houseCode'], light['unitCode'], command)
		cm19a.finish()

	def createDefaultJson(self):
		jsonFile = open('house.json', 'w+')
		defaultJson = json.dumps({"lights":[]})
		jsonFile.write(defaultJson)


	def writeFileJson(self, jsonData):
		with open("house.json", "w") as jsonFile:
			jsonFile.write(json.dumps(jsonData))	


	def getFileJson(self):
		jsonFile = open('house.json', 'r')
		jsonData = json.load(jsonFile)
		jsonFile.close()
		return jsonData