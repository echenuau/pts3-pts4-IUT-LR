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
    # Is Modified when insertClient() is call
    clientID = 0
    # Is odifeid when insertSession() is call
    sessionID = 0
    
    def __init__(self,host, dbname, user, password, port):
        self.host = host
        self.dbName = dbname
        self.user = user
        self.password = password
        self.port = port

    def insertClient(self,surname, name):
        global clientID
        sql = """INSERT INTO "client"(surname,name)
                VALUES(%s,%s) RETURNING id"""
        conn = None
        try:
            # read database configuration
            # params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(dbname=self.dbName, user=self.user, host=self.host, password=self.password)
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, (surname, name))
            # get the generated id back
            client_id = cur.fetchone()[0]
            clientID = client_id
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def startSession(self):
        global sessionID
        '''
        coordinateLong = rtk.getLongitude()
        coordinateLat = rtk.getLatitude()
        '''
        DateSession = str(date.today())
        Begin_Hour = str(date.today())

        '''a supprimer quand RTK fait'''
        coordinateLong = -1.1520434
        coordinateLat = 46.1591126
        Start_Position = AsIs("'(%s,%s)'" % (adapt(coordinateLat), adapt(coordinateLong)))

        sql = """INSERT INTO session(date,Start_Position,Begin_Hour,client)
                VALUES(%s,%s,%s,%s) RETURNING id"""
        try:
            # read database configuration
            # params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(dbname=self.dbName, user=self.user, host=self.host, password=self.password)
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql, (DateSession, Start_Position, Begin_Hour, clientID))
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
        End_Hour = str(now.hour) + str(now.minute) + str(now.second)

        sql = """UPDATE session
                SET End_Hour = %s
                WHERE id = %s"""
        try:
            # read database configuration
            # params = config()
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
            # read database configuration
            # params = config()
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