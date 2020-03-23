import socket
import threading

class Server(threading.Thread):
	"""
		Class manage the server which recives location data.   
	"""
	def __init__(self,port):
		"""
			Inits the server structure in a new thread.

			:param port: The server port.
			
			**Authors of this class :** CHENUAUD Emmanuel and LAMBERT Vincent.\n  
		"""
		self.port = port
		self.running = True
		threading.Thread.__init__(self)
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind(('', self.port))
		self.connection = None
		self.location = dict()

	def run(self):
		"""
			This method :
				* create a listener in the server thread to wait client connection,
				* recovery and processing of data received in socket.
		"""
		self.socket.listen(5)
		self.socket.settimeout(1.0)

		print("[Server] : Waiting client...")

		while self.running:
			try:
				self.connection, adresse = self.socket.accept()
				print("[Server] : Client is connecting.")
				
				while self.running:
					data = self.connection.recv(1024)
					data = data.decode('utf8')
					if data == "" or data == "Close connection":
						print("[Server] : Client was disconnected.")
						self.connection.close()
						break
					else:
						self.location = data.split(";",-1)
						#A enlever
						#print(self.getLocation())

			except socket.timeout:
				continue
			except :
				print("[Server] : Server is stopping.")
				self.running = False
					

	def exit(self):
		"""
			This method allows to stop server and cut existing connection with any client.
		"""
		if self.connection is not None : self.connection.close()
		self.socket.close()

	def getLocation(self):
		"""
			This method allows to recover actual location given by client.

			:return: dict(lat,long)
			lat = latitude of location, long = longitude of location
		"""
		return self.location