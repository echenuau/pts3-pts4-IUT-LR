import sys  
sys.path.append("../socket/") 
from EmulateGPS import EmulateGPS
from Client import Client
import time


gps = EmulateGPS()
client = Client(4010)
if client.connectionToServer():
	print("Send data")
	for i in range(1000):
		if client.sendData("{};{}".format(gps.getLatitude(),gps.getLongitude())) :
			time.sleep(0.5)
		else:
			print("Connection closed !")
			break
	client.closeConnection()