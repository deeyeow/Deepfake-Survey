from pymongo import MongoClient 


class Testdb():
	def __init__(self):
		try:
			self.client = MongoClient("mongodb+srv://matrixxd:test@sd-hacks-sjjrb.mongodb.net/test?retryWrites=true&w=majority")
			print("Connection success")
		except:
			print("Connection fail")
		
		self.db = self.client.SD_Hacks
		self.collection = self.db.facecount




	def printAll(self):
		self.cursor = self.collection.find()
		for self.record in self.cursor:
			print(self.record)

	def print(self, name):
		print(self.collection.find({"image_name": name})[0])




	def getReal(self, name):
		myCursor = self.collection.find_one({"image_name": name})
		return myCursor["real_count"]

	def getFake(self, name):
		myCursor = self.collection.find_one({"image_name": name})
		return myCursor["fake_count"]




	def incrementReal(self, name):
		if self.collection.count_documents({"image_name": name}, limit = 1) != 0:
			self.collection.update_one({"image_name": name}, {"$inc": {"real_count": 1}})
		else:
			self.collection.insert_one({"image_name": name, "real_count": 1, "fake_count": 0})

	def incrementFake(self, name):
		if self.collection.count_documents({"image_name": name}, limit = 1) != 0:
			self.collection.update_one({"image_name": name}, {"$inc": {"fake_count": 1}})
		else:
			self.collection.insert_one({"image_name": name, "real_count": 0, "fake_count": 1})


		

	def delete(self, name):
		self.collection.delete_one({"image_name": name})		#image_name must be unique

	def deleteAll(self):
		self.collection.drop()




	
def main():
	client = Testdb("localhost", 27017)
	client.printAll()
	print("\n")

	#client.insert("img1")
	#client.printAll()
	#print("\n")

	client.incrementReal("img1")
	client.incrementFake("img2")
	client.incrementReal("img2")
	client.printAll()

	

	#client.deleteAll()
	#client.printAll()
	

	
if __name__ == "__main__":
	main()

