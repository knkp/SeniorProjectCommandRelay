import serial
import socket
from time import sleep

CABINET_ID = 0


def checkIfInDatabase(ID, file):
        with open(file) as DB_FILE:
                for line in DB_FILE:
                        splitLine = line.split()
			print("current value in file is: "+splitLine[0])
			print("current ID value is: "+ID)
                        if splitLine[0] == ID:
                                return 1
		return 0

def register(ID, file, CB_ID):
        DB = open(file,'a+')
	CB_ID, C_ID_string = getNextCabinet(CABINET_ID)
        DB.write(ID + ' ' + C_ID_string+'\n')
	return CB_ID

def getNextCabinet(cabinetID):
        if cabinetID is 0:
                cabinetID = 1
        else:
                cabinetID = 0
        return cabinetID, str(cabinetID)

def open_cabinet(cabinetID,arduino):
	arduino.write('x') #tell the arduino that we are going to send it a cabinet ID to open
	arduino.read() #wait for acknowledge
	arduino.write(bytes(cabinetID))  #send id
	arduino.read() #receive ack
	sleep(5) #wait for 5 seconds before closing cabinet
	arduino.write('M') #tell arduino we are going to close a cabinet
	arduino.write(bytes(cabinetID)) #send id to close
	arduino.read()
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
			#we are receiving an ID
			while message is not 'k':
				conn1.write('a')
				message = conn1.read()
#				conn1.write('a')
				if message is not 'k':
					print("got id character: " + message)
					id.append(message)
			#send message to database file, also, send to GUI tool	
			id_string = ''.join(id)
			id = []
			print("ID received, ID is: "+id_string);
			conn1.flush()
			if checkIfInDatabase(id_string,'./DB_FILE') is 1:
				open_cabinet(CABINET_ID, conn2)
			else:
				CABINET_ID = register(id_string, './DB_FILE', CABINET_ID)

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
