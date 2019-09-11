from data_storage import *


class generator : 

	def __init__(self,name,values,region):
		self.name = name 
		self.atts = ["DC(MW)" , "Schedule(MW)" , "Actual(MW)" , "(+)OI/(-)UI(MW)"]
		self.region = region

		if values is not None :
			self.values = values 
			self.data = self.create_data(values)

		else:
			self.values = None
			self.data = None 

	

	def __repr__(self):
		return f'Name : {self.name} Region : {self.region} Current : {self.data}'


	def create_data(self,values):
		return dict(zip(self.atts,values))


	def update_data(self,values):
		self.values = values 
		self.json = self.create_data(values)



	def send_data(self):
		if(insertPost(self.data , self.region) == self.region):
			return 200 




		






if __name__ == "__main__":
	gen = generator("AN" , [460,493,350,42], "UPS")
	print(gen)
	print(gen.send_data())


