import socket
import threading
import sys

# Los tres nombres del lobo
clientes = []
buffer = 1024
direccion = ("50.19.0.71", 8000)

class Cliente(threading.Thread):
	def __init__(self, socket_cliente, datos_cliente):
		#declaro que tiene propiedades de un hilo, y le asigno los atributos
		threading.Thread.__init__(self)
		self.socket = socket_cliente
		self.datos = datos_cliente[0] + ":" + str(datos_cliente[1])
		global buffer
		nick = str(self.socket.recv(buffer))
		self.nick = nick
		print ("Se conecto ", self.nick)
		
	def run(self):
		global buffer, clientes
		while True:
			# Espero mensaje
			mensaje_recibido = self.socket.recv(buffer)
			try:
				if not(mensaje_recibido == ":salir"):
					print (mensaje_recibido.decode("utf-8"))
					for cliente in clientes:
						print ("Enviando mensaje a todos")
						# Envia su mensaje a todos menos a el mismo (todos aquellos que esten en la lista)
						if cliente.nick != self.nick:
							mensaje_completo = self.nick + ": " + mensaje_recibido.decode("utf-8")
							cliente.socket.send(mensaje_completo.encode("utf-8"))
				
				else:
					self.cerrar_conexion()
					break
			except:
				self.cerrar_conexion()
				print ("se rompio")
				break	
	
	def cerrar_conexion(self):
		global clientes
		for cliente in clientes:
				 	mensaje_completo = str("El desubicado de " + self.nick + "se desconecto")
				 	self.socket.send(mensaje_completo.encode("utf-8"))
		self.socket.close()
		clientes.remove(self)





socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socket_servidor.bind(direccion)
socket_servidor.listen(5)
print ("Estoy esperando una conexion...")

try:
	while True:
		# Espero conexion, a menos que aprete Ctrl + C para que cierre el servidor 
		try:
			socket_cliente, datos_cliente = socket_servidor.accept()
		
		except KeyboardInterrupt:
			for cliente in clientes:
				cliente.shutdown()
			print ("Chauchiiiii")
			break
		# Creo el nuevo hilo cliente
		nuevo_cliente = Cliente(socket_cliente, datos_cliente)
		nuevo_cliente.start()
		# Si actualizo la lista despues se supone que este nuevo cliente no se veria a si mismo en la lista por lo tanto no se mandaria
		# mensajes a si mismo, o probablemente si			
		clientes.append(nuevo_cliente)



except:
	print("Ocurrio un problema durante el procesamiento mistico de los putos datos que se rompieron, carajo..")
	socket_servidor.close()


socket_servidor.close()



