import web
import json

class Index:
	def GET(self): #Dump a list of all rooms as JSON
		jsonData = self.getFileJson();
		web.header('Content-Type', 'application/json')
		return json.dumps(jsonData)

	def PUT(self): #Add the room and return 200 or some server error if room exists

		jsonData = self.getFileJson()
		rooms = jsonData["rooms"]
		newRoom = json.loads(web.data());
		rooms.append(newRoom)

		self.writeFileJson(jsonData)

	def DELETE(self, path): #Delete a room from the database
		jsonData = self.getFileJson()
		
		updatedRooms = [room for room in jsonData["rooms"] if room["path"] != web.ctx.path]

		self.writeFileJson(updatedRooms)

	def writeFileJson(self, jsonData):
		with open("house.json", "w") as jsonFile:
			jsonFile.write(json.dumps(jsonData))	


	def getFileJson(self):
		jsonFile = open('house.json', 'r')
		jsonData = json.load(jsonFile)
		jsonFile.close()
		return jsonData
