#!/usr/bin/env python

import socket, struct

TCP_IP = 'localhost'
TCP_PORT = 5005
BUFFER_SIZE = 4096

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

def end_game(msg, socket):
#TODO
#Check if server is saying game over (i.e., the user has won or lost)
#If game is over, recv msg from svr asking if you want to play again then send your response
#If response is no, close the socket 

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
    #TODO:
    #Check if msg says game is over

def recvall(sock, n):
    #recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def recv_board(): #receive picture
	#print("get BOARD function")
	recv_msg(s)

def recv_missed(): #receive missed letters
	#print("get missed function")
	recv_msg(s)

def recv_letters(): #receive correctly guessed and missing letters in secret word
	#print("get letters function")
	recv_msg(s)

def recv_getGuess(): #receive guess prompt from server, you win message, or you lose message
	#print("get Guess function")
	resp = recv_msg(s)
	return resp

def recv_game(): #this function gets all of the info needed for each turn from the server before the user guesses a letter
	#TODO
	#receive picture
	#receive missed letters
	#receive correctly guessed and missing letters in secret word
	if recv_getGuess(): #receive prompt from server to guess a letter, you win message, or you lose message
		return True #game over, user wants to play again
	return False	

def send_guesses():
	msg = input("Letter: ")
	send_msg(s, msg)


recv_msg(s) #first game is starting, receiving banner here 
print("Waiting for oponent to choose word...")
recv_msg(s) #receiving 'Ready to rumble' message 

#game loop
#TODO
#receive board, misses, correct letters, and if game isn't over, the guess prompt too
#send letter guess
#if game is over, do not send a guess, wait for openent to choose new secret word
while True:



		



	
	









