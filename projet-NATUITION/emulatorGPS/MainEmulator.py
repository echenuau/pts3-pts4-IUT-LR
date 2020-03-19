from EmulateGPS import EmulateGPS

gps = EmulateGPS()

for i in range(1000):
	print(gps.getLatitude())
	print(gps.getLongitude())
