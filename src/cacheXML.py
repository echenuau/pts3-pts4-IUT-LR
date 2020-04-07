from lxml import etree
import xml.dom.minidom
import re
from xml.dom.minidom import parseString



class cacheXML(object):
	""" This class put given data in a XML cache file """
	def __init__(self):
		"""
			Class constructor 

			:param root: The root element of the xml tree used in cacheResult()
			:param latt: The root element of the xml tree used in cacheResultSol2()

			**Authors of this class :** ELOY Tyfenn.\n  

		"""
		self.root = etree.Element('root')
		self.root2 = etree.Element('root')

	def prettify(self, element, indent='  '):
		queue = [(0, element)]  # (level, element)
		while queue:
			level, element = queue.pop(0)
			children = [(level + 1, child) for child in list(element)]
			if children:
				element.text = '\n' + indent * (level+1)  # for child open
			if queue:
				element.tail = '\n' + indent * queue[0][0]  # for sibling open
			else:
				element.tail = '\n' + indent * (level-1)  # for parent close
			queue[0:0] = children  # prepend so children come before siblings


	def cacheResult(self,anAngle, aCoordinates, aTimer_hour, aWeather, aHumidity, aTemperature, aSession):
		"""
			Outdated
			Create a XML tree where each result is an element composed of other children element (heavier but more redable). Write result in /cache/result.xml
		"""
		result = etree.SubElement(self.root,"result")

		angle = etree.SubElement(result, "angle")
		angle.text = str(anAngle)

		coordinates = etree.SubElement(result, "coordinates")
		coordinates.text = str(aCoordinates)

		timer_hour = etree.SubElement(result, "timer_hour")
		timer_hour.text = str(aTimer_hour)

		weather = etree.SubElement(result, "weather")
		weather.text = str(aWeather)

		humidity = etree.SubElement(result, "humidity")
		humidity.text = str(aHumidity)

		temperature = etree.SubElement(result, "temperature")
		temperature.text = str(aTemperature)

		sessions = etree.SubElement(result, "sessions")
		sessions.text = str(aSession)

		self.prettify(self.root)

		tree = etree.ElementTree(self.root)
		tree.write('cache/result.xml', encoding='UTF-8', xml_declaration=True)
		print("0")

	def cacheResultSol2(self,anAngle, aCoordinates, aTimer_hour, aWeather, aHumidity, aTemperature, aSession):
		"""
			Create a XML tree where each result is an element defined by the 7 attributes inserted in batabase (lighter but more difficult to read). Write result in /cache/result.xml
		"""
		result = etree.SubElement(self.root2,"result")

		result.set("angle", str(anAngle))

		result.set("coordinates",  str(aCoordinates))

		result.set("timer_hour",  str(aTimer_hour))

		result.set("weather",  str(aWeather))

		result.set("humidity",  str(aHumidity))

		result.set("temperature",  str(aTemperature))

		result.set("session",  str(aSession))

		self.prettify(self.root2)

		tree = etree.ElementTree(self.root2)
		tree.write('cache/result.xml', encoding='UTF-8', xml_declaration=True)
		print("0")

	def readCache(self):
		"""
			Read all the elements in /cache/result.xml and returns it in a dict {LineNumber:{'angle': '0', 'coordinates': '0','timer_hour': '0', 'weather': '0', 'humidity': '0', 'temperature': '0', 'session': '0'}}
		
			:return: dict: Data structure of the request
		"""
		results = {0:{'angle': '0', 'coordinates': '0','timer_hour': '0', 'weather': '0', 'humidity': '0', 'temperature': '0', 'session': '0'}}
		i = 0
		tree = etree.parse("cache/result.xml")
		for element in tree.xpath("/root/result"):
			#print(i)
			i = i + 1
			results[i] = {}
			results[int(i)]['angle'] = element.get("angle")
			results[int(i)]['coordinates'] = element.get("coordinates")
			results[int(i)]['timer_hour'] = element.get("timer_hour")
			results[int(i)]['weather'] = element.get("weather")
			results[int(i)]['humidity'] = element.get("humidity")
			results[int(i)]['temperature'] = element.get("temperature")
			results[int(i)]['session'] = element.get("session")
		print(results)
		return results