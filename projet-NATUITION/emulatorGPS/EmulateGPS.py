class EmulateGPS:
	"""
		This class emulate a route between UIT of La Rochelle and Natuition's office.\n
		This route is composed by one thousand point. One point is defiend by a latitude and a longitude.\n
		This class has to be used to test inserting potentiometer results in database whitout use the robot.
	"""
	def __init__(self):
		"""
			This method initialize the route parameters : 
				* start point of route,
				* end point of route.

			These values can be modified to create other routes (it's useless).

			**Authors of this class :** CHENUAUD Emmanuel.
		"""
		self.latitude_start = 46.141993
		self.longitude_start = -1.151800

		self.latitude_end = 46.154292
		self.longitude_end = -1.118223
		
		self.curr_latitude = self.latitude_start
		self.curr_longitude = self.longitude_start

		self.calculateCoeff()				

		self.counter = 0

	def calculateCoeff(self):
		"""
			This method calculates spacing between two route points for routes composed by one thousand points :
				* latitude coefficient,
				* longitude coefficient.

		"""
		self.coef_latitude = abs(abs(self.latitude_end)-abs(self.latitude_start))/1000
		self.coef_longitude = abs(abs(self.longitude_end)-abs(self.longitude_start))/1000

	def getLatitude(self):
		"""
			Get the latitude of current point.

			:return: float: The latitude of current point.
		"""
		if self.latitude_start<self.latitude_end :
			self.curr_latitude += self.coef_latitude
		else:
			self.curr_latitude -= self.coef_latitude
		return self.curr_latitude

	def getLongitude(self):
		"""
			Get the longitude of current point.

			:return: float: The longitude of current point.
		"""
		if self.longitude_start<self.longitude_end :
			self.curr_longitude += self.coef_longitude
		else:
			self.curr_longitude -= self.coef_longitude
		self.countIncrement()
		return self.curr_longitude

	def countIncrement(self):
		"""
			This method increments the position on the route by one.\n
			Don't use it method. It's already used in getLongitude().
		"""
		self.counter += 1

	def getLatitude_N(self,N):
		"""
			Get the latitude of the N-th point in the route.

			:param N: The latitude of targeted point.
		"""
		if self.latitude_start<self.latitude_end:
			latitudeN = self.latitude_start + N*self.coef_latitude
		else:
			latitudeN = self.latitude_start - N*self.coef_latitude
		return latitudeN

	def getLongitude_N(self,N):
		"""
			Get the longitude of the N-th point in the route.

			:param N: The longitude of targeted point.
		"""
		if self.longitude_start<self.longitude_end:
			longitudeN = self.longitude_start + N*self.coef_longitude
		else:
			longitudeN = self.longitude_start - N*self.coef_longitude
		return longitudeN
