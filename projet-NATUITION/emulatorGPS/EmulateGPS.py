class EmulateGPS:
	def __init__(self):
		self.latitude_start = 46.141993
		self.longitude_start = -1.151800

		self.latitude_end = 46.154292
		self.longitude_end = -1.118223
		
		self.curr_latitude = self.latitude_start
		self.curr_longitude = self.longitude_start

		self.calculateCoeff()				

		self.counter = 0

	def calculateCoeff(self):
		self.coef_latitude = abs(abs(self.latitude_end)-abs(self.latitude_start))/1000
		self.coef_longitude = abs(abs(self.longitude_end)-abs(self.longitude_start))/1000

	def getLatitude(self):
		if self.latitude_start<self.latitude_end :
			self.curr_latitude += self.coef_latitude
		else:
			self.curr_latitude -= self.coef_latitude
		return self.curr_latitude

	def getLongitude(self):
		if self.longitude_start<self.longitude_end :
			self.curr_longitude += self.coef_longitude
		else:
			self.curr_longitude -= self.coef_longitude
		self.countIncrement()
		return self.curr_longitude

	def countIncrement(self):
		self.counter += 1

	def getLatitude_N(self,N):
		if self.latitude_start<self.latitude_end:
			latitudeN = self.latitude_start + N*self.coef_latitude
		else:
			latitudeN = self.latitude_start - N*self.coef_latitude
		return latitudeN

	def getLongitude_N(self,N):
		if self.longitude_start<self.longitude_end:
			longitudeN = self.longitude_start + N*self.coef_longitude
		else:
			longitudeN = self.longitude_start - N*self.coef_longitude
		return longitudeN
