import os.path
from os import path
import threading
import time
import re
from Database import Database

class SensorProcessing:
    def __init__(self,pathConfig,analogDigitalConverter):
        
        self.pathConfig = pathConfig + '/config.data'
        
        if(not path.exists(self.pathConfig)):
            self.initFileConfiguration()
        
        self.analogDigitalConverter = analogDigitalConverter
        
        host = self.getPropertyInFileConfiguration("Host")
        dbName = self.getPropertyInFileConfiguration("Database\ name")
        login = self.getPropertyInFileConfiguration("Login")
        password = self.getPropertyInFileConfiguration("Password")
        port = self.getPropertyInFileConfiguration("Port")
        
        self.database = Database(host,dbName,login,password,port)
        
        
    def startSession(self):
        surname = self.getPropertyInFileConfiguration("Surname")
        name = self.getPropertyInFileConfiguration("Name")
        #insertClient() of Database class
        self.database.insertClient(surname,name)
        
        #startSession() of Database class
        self.database.startSession()
        
        #startThread
        self.thread = threading.Thread(target=self.loop , args=({0.5}))
        self.thread.start()
        
    def endSession(self):
        #stopThread
        self.thread.do_run = False
        self.thread.join()
        
        #endSession() of Database class
        self.database.endSession()
        
    # Define a function for the thread
    def loop(self,delay):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            print("Wheels degree : "+str(self.getAngle()))
            #insertResults(self.getAngle()) of Database class
            self.database.insertResults(self.getAngle())
            time.sleep(delay)
            
    def getAngle(self):
        voltage = self.analogDigitalConverter.getFormattedVoltage()
        print(voltage)
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
        file = open(self.pathConfig, 'r')
        reg = '^'+name+':\ (.*)'
        for line in file.readlines():
            matchObj = re.match( reg, line, re.X|re.I)
            if(matchObj is not None):
                return matchObj.group(1)
        
    def initFileConfiguration(self):
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
        file.write("0°: 2.047\n")
        #   # Potentiometer reference voltage :
        file.write("# Potentiometer reference voltage :\n")
        #   Reference: value
        file.write("Reference: 4.094\n")
        #   # Maximum number of turns that the potentiometer can make :
        file.write("# Maximum number of turns that the potentiometer can make :\n")
        #   Turns: value
        file.write("Turns: 1\n")
        #   # Multiplication ratio between the motor and the potentiometer :
        file.write("# Multiplication ratio between the motor and the potentiometer :\n")
        #   Ratio M&P: value
        file.write("Ratio M&P: 3\n")
        #   # Multiplication ratio between the motor and wheels :
        file.write("# Multiplication ratio between the motor and wheels :\n")
        #   Ratio M&W: value
        file.write("Ratio M&W: 3.6\n\n")

        #   # ------------------------
        file.write("# ------------------------\n")
        #   # | Customer information |
        file.write("# | Customer information |\n")
        #   # ------------------------
        file.write("# ------------------------\n\n")

        #   # The customer's name :
        file.write("# The customer's name :\n")
        #   Name: value
        file.write("Name: value\n\n")

        #   # The customer's surname :
        file.write("# The customer's surname :\n")
        #   Surname: value
        file.write("Surname: value\n\n")

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