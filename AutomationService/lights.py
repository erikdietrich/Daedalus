import web
import json

class Lights:

	def GET(self):
		jsonData = self.getFileJson()
		lights = jsonData['lights']
		web.header('Content-Type', 'application/json')
		return json.dumps(jsonData)

	def PUT(self): #Add the room and return 200 or some server error if room exists

		global app

		jsonData = self.getFileJson()
		lights = jsonData['lights']
		newLight = json.loads(web.data())
		lights.append(newLight)

		self.writeFileJson(jsonData)

	def DELETE(self, lightId): #Delete a room from the database
		jsonData = self.getFileJson()
		
		updatedLights = [light for light in jsonData['lights'] if light['lightId'] != lightId]
		jsonData['lights'] = updatedLights

		self.writeFileJson(jsonData)

	def writeFileJson(self, jsonData):
		with open("house.json", "w") as jsonFile:
			jsonFile.write(json.dumps(jsonData))	


	def getFileJson(self):
		jsonFile = open('house.json', 'r')
		jsonData = json.load(jsonFile)
		jsonFile.close()
		return jsonData