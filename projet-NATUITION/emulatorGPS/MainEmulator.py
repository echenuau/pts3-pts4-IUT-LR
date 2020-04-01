import sys  
sys.path.append("../socket/") 
from EmulateGPS import EmulateGPS
from Client import Client
import time

#Create the client that sends localisation (RTK), start it just after SensorProcessing
gps = EmulateGPS()
client = Client(4000)
#-----------------------------------------------
#Use it to connect the client
if client.connectionToServer():
	print("[Client] Send data")
	for i in range(1000):
		#Replace the gps.getLatitude() and gps.getLongitude by your RTK functions
		if client.sendData("{};{}".format(gps.getLatitude(),gps.getLongitude())) :
			time.sleep(0.6)#waiting time between two angular capture (0.5sec)
		else:
			print("[Client] Connection closed !")
			break
#-----------------------------------------------	
	#Close the client connection when the robot work is finish
	client.closeConnection()