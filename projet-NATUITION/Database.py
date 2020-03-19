import psycopg2
import datetime
from datetime import date
from datetime import datetime
from psycopg2.extensions import adapt, register_adapter, AsIs


class Database:
    
    host = ""
    db = ""
    user = ""
    password = ""
    port = ""
    robotSerialNumber = ""
    sessionID = 0

    
    def __init__(self,host, dbname, user, password, port):
        self.host = host
        self.dbName = dbname
        self.user = user
        self.password = password
        self.port = port

    def insertRobot(self,serialNumber):
    	global robotSerialNumber
    	robotSerialNumber = None
    	robotSerialNumber = serialNumber
    	sql = 'INSERT INTO robot(serial_number) VALUES(\'{}\');'.format(robotSerialNumber)
    	print(sql)
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
    		print(error)
    	finally:
    		if conn is not None:
    			conn.close()

    def startSession(self):
        global sessionID
        global robotSerialNumber
        sessionID=None

        '''
        coordinateLong = rtk.getLongitude()
        coordinateLat = rtk.getLatitude()
        '''

        now = datetime.now().time()
        DateSession = str(datetime.now())
        Begin_Hour = str(now.hour) + "h" + str(now.minute) + "min" + str(now.second) + "s"

        '''a supprimer quand RTK fait'''
        coordinateLong = -1.1520434
        coordinateLat = 46.1591126
        Start_Position = AsIs("'(%s,%s)'" % (adapt(coordinateLat), adapt(coordinateLong)))

        sql = """INSERT INTO "session"(date,Start_Position,Begin_Hour,robot)
                VALUES(%s,%s,%s,%s) RETURNING id"""

        conn = None
        try:
            # connect to the PostgreSQL database
            conn = psycopg2.connect(dbname=self.dbName, user=self.user, host=self.host, password=self.password)
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, (DateSession, Start_Position, Begin_Hour, robotSerialNumber))
            # get the generated id back
            sessionID = cur.fetchone()[0]
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def endSession(self):
        global sessionID
        now = datetime.now().time()
        End_Hour = str(now.hour) + "h" + str(now.minute) + "min" + str(now.second) + "s"

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
            cur.execute(sql, (End_Hour, sessionID))
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def insertResults(self,angle):
        '''
        weather = weatherApi.getWeather()
        temperature = weatherApi.getTemperature()
        humidity = weatherApi.getHumidity()
        coordinateLong = rtk.getLongitude()
        coordinateLat = rtk.getLatitude()
        '''

        # A supprimer quand il y aura rtk et weather
        weather = "Wow il fait beau"
        temperature = 15
        humidity = 1.1
        coordinateLong = -1.1520434
        coordinateLat = 46.1591126

        coordinate = AsIs("'(%s,%s)'" % (adapt(coordinateLat), adapt(coordinateLong)))
        time_hour = datetime.now().time()

        sql = """INSERT INTO resultat(angle,coordinates,timer_hour,weather,humidity,temperature,session)
                VALUES(%s,%s,%s,%s,%s,%s,%s);"""
        try:
            # connect to the PostgreSQL database
            conn = psycopg2.connect(dbname=self.dbName, user=self.user, host=self.host, password=self.password)
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, (angle, coordinate, time_hour, weather, humidity, temperature, sessionID,))
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

db = Database("postgresql-pts4.alwaysdata.net","pts4_db","pts4","13377997","5432")
var="N24632"
db.insertRobot(var)
db.startSession()
db.endSession()