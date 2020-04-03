# -*- coding: utf-8 -*-
import os.path
from os import path
import threading
import time
import re
from Database import Database
from AnalogDigitalConverter import AnalogDigitalConverter

class SensorProcessing:
	"""
		Class managing the sensor's class and the database's class. 
	"""
		
	def __init__(self,pathConfig,channel):
		"""
			Inits SensorProcessing with path of the configuration file.\n
			Create an instance of AnalogDigitalConverter, Database and thread.\n
			And if configuration file doesn't exist he create it.

			:param pathConfig: Path of the configuration file.    
			:param channel: Channel number where the potentiometer is connected [0|1|2].
			
			**Authors of this class :** CHENUAUD Emmanuel and LAMBERT Vincent.\n  
		"""

		self.pathConfig = pathConfig + '/config.data'
		
		if(not path.exists(self.pathConfig)):
			self.initFileConfiguration()

		host = self.getPropertyInFileConfiguration("Host")
		dbName = self.getPropertyInFileConfiguration("Database\ name")
		login = self.getPropertyInFileConfiguration("Login")
		password = self.getPropertyInFileConfiguration("Password")
		port = self.getPropertyInFileConfiguration("Port")
		robotSerialNumber = self.getPropertyInFileConfiguration("Serial\ number")
		serverPort = self.getPropertyInFileConfiguration("Server\ port")


		self.thread = threading.Thread(target=self.loop , args=({0.5}))
		self.analogDigitalConverter = AnalogDigitalConverter(channel)
		self.database = Database(host,dbName,login,password,port,robotSerialNumber,serverPort)
		
	def startSession(self):
		"""
			Lauch robot session.\n
			This method :
				* create in database the robot if doesn't exist,
				* start session in Database,
				* start the thread.

		"""

		robotSerialNumber = self.getPropertyInFileConfiguration("Serial\ number")

		#insertRobot() of Database class
		self.database.insertRobot(robotSerialNumber)
		
		#startSession() of Database class
		self.database.startSession()
		
		#startThread
		self.thread.start()
		
	def endSession(self):
		"""
			Stop robot session.\n    
			This method :
				* stop session in Database,
				* stop the thread.

		"""

		#stopThread
		self.thread.do_run = False
		self.thread.join()
		
		#endSession() of Database class
		self.database.endSession()
		
	def loop(self,delay):
		"""
			Loop of robot's thread.    

			:param delay: Waiting time between each iteration (in millisecond). 
		"""

		t = threading.currentThread()
		while getattr(t, "do_run", True):
			print("[SensorProcessing] Wheels degree : "+str(self.getAngle()))
			self.database.insertResults(self.getAngle())
			time.sleep(delay)
			
	def getAngle(self):
		"""
			Allows to recover the value of wheels' angle (in degree).   

			:return: float: Wheels' angle (in degree), postive degrees : wheels turn right and negative degrees for left.
		"""

		voltage = self.analogDigitalConverter.getFormattedVoltage()
		print("[SensorProcessing] Voltage : {}".format(voltage))
		turns = float(self.getPropertyInFileConfiguration("Turns"))
		zero = float(self.getPropertyInFileConfiguration("0°"))
		ratioMP = float(self.getPropertyInFileConfiguration("Ratio\ M&P"))
		ratioMW = float(self.getPropertyInFileConfiguration("Ratio\ M&W"))
		reference = float(self.getPropertyInFileConfiguration("Reference"))
		
		voltageSigne = (voltage - zero)
		
		minusDegree = zero / (180*turns)
		plusDegree = (reference-zero) / (180*turns)
		
		potentiometreDegree = voltageSigne/plusDegree
		if(voltageSigne < zero):
			potentiometreDegree = voltageSigne/minusDegree
						
		motorDegree = potentiometreDegree / ratioMP
		wheelsDegree = motorDegree / ratioMW

		return float("{0:.3f}".format(wheelsDegree))
		
	def getPropertyInFileConfiguration(self,name):
		"""
			Allows to recover a value of property in file configuration.

			:param name: Name of property in file configuration.

			:return: str: Property value.
        """

		file = open(self.pathConfig, 'r')
		reg = '^'+name+':\ (.*)'
		for line in file.readlines():
			matchObj = re.match( reg, line, re.X|re.I)
			if(matchObj is not None):
				return matchObj.group(1)
		
	def startServer(self):
		"""
			This method call server start in Database.
		"""
		self.database.startServer()

	def stopServer(self):
		"""
			This method call server stop in Database.
		"""
		self.database.stopServer()

	def initFileConfiguration(self):
		"""
			Allows to create blank file configuration.\n 
			Fields with the value 'value' must be completed.
        """

		file = open(self.pathConfig,'w')
		
		#   # --------------------------------------------------------------------------------------------------------------
		file.write("# --------------------------------------------------------------------------------------------------------------\n")
		#   # | Configuration file for the purple robot retrieving the steering angle project and saving it to a database. |
		file.write("# | Configuration file for the purple robot retrieving the steering angle project and saving it to a database. |\n")
		#   # | To comment in this file use '#'.                                                                           |
		file.write("# | To comment in this file use '#'.                                                                           |\n")
		#   # --------------------------------------------------------------------------------------------------------------
		file.write("# --------------------------------------------------------------------------------------------------------------\n\n")


		#   # ------------------------------------------
		file.write("# ------------------------------------------\n")
		#   # | Analog digital converter configuration |
		file.write("# | Analog digital converter configuration |\n")
		#   # ------------------------------------------
		file.write("# ------------------------------------------\n\n")

		#   # The voltage in volt of the zero angle :
		file.write("# The voltage in volt of the zero angle :\n")
		#   0°: value
		file.write("0°: value\n")
		#   # Potentiometer reference voltage :
		file.write("# Potentiometer reference voltage :\n")
		#   Reference: value
		file.write("Reference: value\n")
		#   # Maximum number of turns that the potentiometer can make :
		file.write("# Maximum number of turns that the potentiometer can make :\n")
		#   Turns: value
		file.write("Turns: value\n")
		#   # Multiplication ratio between the motor and the potentiometer :
		file.write("# Multiplication ratio between the motor and the potentiometer :\n")
		#   Ratio M&P: value
		file.write("Ratio M&P: value\n")
		#   # Multiplication ratio between the motor and wheels :
		file.write("# Multiplication ratio between the motor and wheels :\n")
		#   Ratio M&W: value
		file.write("Ratio M&W: value\n\n")

		#   # ---------------------
		file.write("# ---------------------\n")
		#   # | Robot information |
		file.write("# | Robot information |\n")
		#   # ---------------------
		file.write("# ---------------------\n\n")

		#   # The robot's serial number :
		file.write("# The robot's serial number :\n")
		#   Serial number: value
		file.write("Serial number: value\n\n")

		#   # The port number of the server which receives the location data :
		file.write("# The port number of the server which receives the location data :\n")
		#   Server port: value
		file.write("Server port: value\n\n")

		#   # ------------------------
		file.write("# ------------------------\n")
		#   # | Database information |
		file.write("# | Database information |\n")
		#   # ------------------------
		file.write("# ------------------------\n\n")

		#   # The host of database :
		file.write("# The host of database :\n")
		#   Host: value
		file.write("Host: value\n\n")
		
		#   # The port of database :
		file.write("# The port of database :\n")
		#   Port: value
		file.write("Port: value\n\n")

		#   # The name of database user :
		file.write("# The name of database user :\n")
		#   Login: value
		file.write("Login: value\n\n")

		#   # The password of database user :
		file.write("# The password of database user :\n")
		#   Password: value
		file.write("Password: value\n\n")
		
		#   # The database name :
		file.write("# The database name :\n")
		#   Database name: value
		file.write("Database name: value\n")

		file.close() 
