import psycopg2
import datetime
import time
from APIWeather import APIWeather
from datetime import date
from datetime import datetime
import threading
import sys 
from psycopg2.extensions import adapt, register_adapter, AsIs
sys.path.append("./socket/") 
from Server import Server



class Database:
	   
	def __init__(self,host, dbname, user, password, port,robotSerialNumber, serveurPort):
		self.host = host
		self.dbName = dbname
		self.user = user
		self.password = password
		self.port = port
		self.robotSerialNumber = robotSerialNumber
		self.sessionID = None
		self.server = Server(int(serveurPort))
		self.APIWeather = APIWeather(self.server)


	def insertRobot(self,serialNumber):

		"""
		This method obtain the serial number of the robot and send them in the Database by a POSTGRESQL Request
		"""
		
		#INSERT INTO robot(serial_number) SELECT N189563 WHERE NOT EXISTS (SELECT serial_number FROM robot WHERE serial_number = N189563);

		sql = 'INSERT INTO robot(serial_number) SELECT \'{}\' WHERE NOT EXISTS (SELECT serial_number FROM robot WHERE serial_number = \'{}\');'.format(self.robotSerialNumber,self.robotSerialNumber)
		conn = None
		try:
			# connect to the PostgreSQL database
			conn = psycopg2.connect(dbname=self.dbName, user=self.user, host=self.host, password=self.password)
			# create a new cursor
			cur = conn.cursor()
			# execute the INSERT statement
			cur.execute(sql)
			# commit the changes to the database
			conn.commit()
			# close communication with the database
			cur.close()
		except(Exception,psycopg2.DatabaseError) as error:
			print("[Database]")
			print(error)
		finally:
			if conn is not None:
				conn.close()

	def startSession(self):

		"""
		This method format the start date, hour and coordinates and the put them in a POSTGRESQL request that is applicate to the alwaysData Database.
		"""

		now = datetime.now().time()
		DateSession = str(datetime.now())
		Begin_Hour = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
		coordinate = self.server.getLocation()
		coordinateLong = coordinate['latitude']
		coordinateLat = coordinate['longitude']
		Start_Position = AsIs("'(%s,%s)'" % (coordinateLat,coordinateLong))
		sql = """INSERT INTO "session"(date,Start_Position,Begin_Hour,robot)
				VALUES(%s,%s,%s,%s) RETURNING id"""

		conn = None
		try:
			# connect to the PostgreSQL database
			conn = psycopg2.connect(dbname=self.dbName, user=self.user, host=self.host, password=self.password)
			# create a new cursor
			cur = conn.cursor()
			# execute the INSERT statement
			cur.execute(sql, (DateSession, Start_Position, Begin_Hour, self.robotSerialNumber))
			# get the generated id back
			self.sessionID = cur.fetchone()[0]
			# commit the changes to the database
			conn.commit()
			# close communication with the database
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print("[Database]")
			print(error)
		finally:
			if conn is not None:
				conn.close()

	def endSession(self):
		"""
		This method is useful to complete the Database after the end of a session. It recover the end hour of the session and then use a SQL request to send it in the Database
		"""

		now = datetime.now().time()
		End_Hour = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)

		sql = """UPDATE session
				SET End_Hour = %s
				WHERE id = %s"""
		conn = None
		try:
			# connect to the PostgreSQL database
			conn = psycopg2.connect(dbname=self.dbName, user=self.user, host=self.host, password=self.password)
			# create a new cursor
			cur = conn.cursor()
			# execute the INSERT statement
			cur.execute(sql, (End_Hour, self.sessionID))
			# commit the changes to the database
			conn.commit()
			# close communication with the database
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print("[Database]")
			print(error)
		finally:
			if conn is not None:
				conn.close()

	def insertResults(self,angle):
		
		"""
		This method is the method call for inserting the angle and the weather in the Database table results.  
		We have to call the class weather to obtain the different data and we return all of this data as results in the DataBase table of the same name.
		"""

		weather = self.APIWeather.getWeather()
		temperature = self.APIWeather.getTemperature()
		humidity = self.APIWeather.getHumidity()
		coordinate = self.server.getLocation()
		coordinateLong = coordinate['latitude']
		coordinateLat = coordinate['longitude']

		# A supprimer quand il y aura rtk et weather
		now = datetime.now().time()
		coordinate = AsIs("'(%s,%s)'" % (coordinateLat, coordinateLong))
		time_hour = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)

		sql = """INSERT INTO resultat(angle,coordinates,timer_hour,weather,humidity,temperature,session)
				VALUES(%s,%s,%s,%s,%s,%s,%s);"""
		try:
			# connect to the PostgreSQL database
			conn = psycopg2.connect(dbname=self.dbName, user=self.user, host=self.host, password=self.password)
			# create a new cursor
			cur = conn.cursor()
			# execute the INSERT statement
			cur.execute(sql, (angle, coordinate, time_hour, weather, humidity, temperature, self.sessionID,))
			# commit the changes to the database
			conn.commit()
			# close communication with the database
			cur.close()
		except (Exception, psycopg2.DatabaseError) as error:
			print("[Database]")
			print(error)
		finally:
			if conn is not None:
				conn.close()

	def startServer(self):
		"""
			This method start the server for reiceve the location.
		"""
		self.server.start()

	def stopServer(self):
		"""
			This method stop the server.
		"""
		self.server.exit()


#print("[Database] Test")
#db = Database("postgresql-pts4.alwaysdata.net","pts4_db","pts4","13377997","5432","",0)
#var="N24632"
#db.insertRobot(var)
#db.startSession()
#db.endSession()