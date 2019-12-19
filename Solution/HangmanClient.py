#!/usr/bin/env python

import socket, struct

TCP_IP = 'localhost'
TCP_PORT = 5005
BUFFER_SIZE = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

def end_game(msg, socket):
	if '*' in msg: # '*' signifies game is over 
		print(msg)
		recv_msg(s) #server asking you if you want to play again
		message = input("(y/n): ")
		if 'n' in message:
			print("Bye. Thanks for playing.")
			send_msg(s, message)
			s.close()
			exit() #kill client program, game is over, and user doesn't want to play again
		send_msg(s, message)
		return False #game is over, and user wants to play again
	return True	#game is not over 	

def send_msg(sock, msg):
    msg = msg.encode() #encoding message string to utf-8 bytes
    msg = struct.pack('>I', len(msg)) + msg #Prefix each message with a 4-byte message length header (network byte order)
    sock.sendall(msg)

def recv_msg(sock):
    raw_msglen = recvall(sock, 4) #Read message length and unpack it into an integer
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    data = (recvall(sock, msglen)).decode() #decode into Unicode string 
    if not end_game(data, s): #if game is over 
    	return True #game over
    print(data)
    return False

def recvall(sock, n):
    #recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def recv_board():
	#print("get BOARD function")
	recv_msg(s)

def recv_missed():
	#print("get missed function")
	recv_msg(s)

def recv_letters():
	#print("get letters function")
	recv_msg(s)

def recv_getGuess():
	#print("get Guess function")
	resp = recv_msg(s)
	return resp

def recv_game(): #this function gets all of the info needed for each turn from the server before the user guesses a letter
	recv_board() #picture
	recv_missed() #missed letters
	recv_letters() #correctly guessed and missing letters in secret word
	if recv_getGuess(): #receive prompt from server to guess a letter
		return True #game over (conditional above checking if game is over)
	return False	

def send_guesses():
	msg = input("Letter: ")
	send_msg(s, msg)


recv_msg(s) #first game is starting, receiving banner here 
print("Waiting for oponent to choose word...")
recv_msg(s) #receiving 'Ready to rumble' message 

while True:
	if recv_game(): #previous game is over, and a new game is starting 
		print("Waiting for opponent to choose word...")
		continue
	else:
		send_guesses()


		



	
	









