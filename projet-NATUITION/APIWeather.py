#!/usr/bin/env python3
import requests 
from pprint import pprint
import time
import json

class APIWeather(object):
	"""This class calls the API"""
	def __init__(self, longi, latt):
		"""
			Inits the class.

			:param apiKey: The key used to call the api.
			:param latt: latitude of the curent location
			:param longi: longitude of the curent location
			:param url: formated url which will call the api
			:param lastData: last data received by the api
			:param lastTime: Last time since the api was sucessfully called (seconds since epoch)
			:param secIntervall: Seconds to pass between each sucessfull call of the api 
			
			**Authors of this class :**ELOY Tyfenn.\n  
		"""
		self.apiKey = "5848ff07bb54b0148626562ffda70065"
		self.lat = latt
		self.lon = longi
		self.url = 'http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric'.format(self.lat,self.lon,self.apiKey)
		res = requests.get(self.url)
		self.lastData = res.json()
		self.lastTime = time.time()
		self.secIntervall = 600 #600 seconds between each api call

	def strAll(self):
		"""
			A to string function which show when was the api called last time and the last data received
		"""
		print(self.url + "\n " + str(self.lastData) + "\n" + str(self.lastTime)) 

	def isAPIRested(self):
		"""
			Checks if the api is "rested" it is rested if more than x second passed since it's last sucessfull call (defined by secIntervall)
		"""
		curTime = time.time()
		if curTime > self.lastTime+self.secIntervall :
			self.lastTime = curTime
			return 1
		else: 
			return 0

	def callAPI(self):
		"""
			Calls the api from OpenWeather 
			:return: dict: Data structure of the request
		"""
		res = requests.get(self.url)
		dataB = res.json()
		return dataB

	def getWeather(self):
		"""
			Return the weather
			:return: string: Current weather.
		"""
		if self.isAPIRested() == 1:
			print("rested")
			data = self.callAPI()
			print(data['weather'][0]['description'])
			return data['weather'][0]['description']
		else:
			data = self.lastData
			print("noRest")
			print(data['weather'][0]['description'])
			return data['weather'][0]['description']

	def getTemperature(self):
		"""
			Return the weather
			:return: float: Current temperature. (xx.xx)
		"""
		if self.isAPIRested() == 1:
			print("rested")
			data = self.callAPI()
			print(data['main']['temp'])
			return data['main']['temp']
		else:
			data = self.lastData
			print("noRest")
			print(data['main']['temp'])
			return data['main']['temp']

	def getHumidity(self):
		"""
			Return the weather
			:return: int: Current humidity. (0-100%)
		"""
		if self.isAPIRested() == 1:
			print("rested")
			data = self.callAPI()
			print(data['main']['humidity'])
			return data['main']['humidity']
		else:
			data = self.lastData
			print("noRest")
			print(data['main']['humidity'])
			return data['main']['humidity']

