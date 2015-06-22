import serial
import socket


#print("setting up socket")
#server_address = ('192.168.0.3',5001)

#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.connect(server_address)



print("attempting first connection")
conn1 = serial.Serial("/dev/ttyACM0")
print("conn1 connected")
conn2 = serial.Serial("/dev/ttyACM1")
print("conn2 connected")
print("flushing connection buffers")
conn1.flush()
conn2.flush()

message = ''
id = []
id_string = ""
while 1:
	if conn1.inWaiting()>0:
		message = conn1.read()
		if message=='i':
			#we are receiving an ID, wait for ID ack signal
			while message is not 'k':
				message = conn1.read()
				if message is not 'k':
					print("got id character: " + message)
					id.append(message)
			#send message to database file, also, send to GUI tool	
			id_string = ''.join(id)
			id = []
			print("ID received, ID is: "+id_string);

#		messageBytes = bytes(message)
#		sock.sendall(messageBytes)
		print("conn1 received character " + message)
		conn2.write(message)
		conn1.flush()
		conn2.flush()
	elif conn2.inWaiting()>0:
		message = conn2.read()
#		messageBytes = bytes(message)
#		sock.sendall(messageBytes)
		print("conn2 received character " + message)
		conn1.write(message)
		conn1.flush()
		conn2.flush()

