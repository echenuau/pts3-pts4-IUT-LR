import sys  
sys.path.append("../socket/") 
from EmulateGPS import EmulateGPS
from Client import Client
import time


gps = EmulateGPS()
client = Client(4000)
if client.connectionToServer():
	print("[Client] Send data")
	for i in range(1000):
		if client.sendData("{};{}".format(gps.getLatitude(),gps.getLongitude())) :
			time.sleep(0.5)
		else:
			print("[Client] Connection closed !")
			break
	client.closeConnection()