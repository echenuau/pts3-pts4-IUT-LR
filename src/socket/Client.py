import socket

class Client():
	"""
		Class manage the client which sends location data.   
	"""
	def __init__(self,port):
		"""
			Inits the client structure.

			:param port: The server port.
			
			**Authors of this class :** CHENUAUD Emmanuel and LAMBERT Vincent.\n  
		"""
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.port = port

	def connectionToServer(self):
		"""
			This method allows client to establish connection with server.

			:return: True or False
			True = client connected, False = connection refused.
		"""
		try:
			self.socket.connect(('127.0.0.1',self.port))
			print("Client connected")
			return True
		except:
			print("Connection refused !")
			return False

	def sendData(self,data):
		"""
			This method allows client to send data at server.

			:param data: The data you want send at server.
		"""
		data = data.encode("utf8")
		try:
			self.socket.send(data)
			return True
		except:
			return False

	def closeConnection(self):
		"""
			This method allows to close the connection with server.
		"""
		self.sendData("Close connection")
		self.socket.close()