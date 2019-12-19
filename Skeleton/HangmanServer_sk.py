#!/usr/bin/env python

# Useful link for sockets: https://realpython.com/python-sockets/
# Usefuk link for send/recv msgs in a socket cxn: https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data/17697651
# Useful link for encoding strings: https://www.programiz.com/python-programming/methods/string/encode
   
import socket
import struct
import Hangman

missedLetters = '' #string to keep track of incorrectly guessed letters
correctLetters = '' #string to keep track of correctly guessed letters
gameOver = False

TCP_IP = '' #loopback address
TCP_PORT = 5005 ## Port to listen on (non-privileged ports are > 1023)
BUFFER_SIZE = 4096  #bytes

s = socket.socket()
s.bind((TCP_IP, TCP_PORT))
s.listen()
conn, addr = s.accept() #connection with client established
print ('Connection address:', addr)

def send_one_message(sock, data):
    data = data.encode() #encoding message string to utf-8 bytes
    data = struct.pack('>I', len(data)) + data #Prefix each message with a 4-byte message length header (network byte order)
    sock.sendall(data)
def recv_one_message(sock):
    lengthbuf = recvall(sock, 4) #Read message length and unpack it into an integer
    if not lengthbuf:
        return None
    lengthbuf = struct.unpack('>I', lengthbuf)[0]
    return recvall(sock, lengthbuf).decode() #decode into Unicode string 
def recvall(sock, n): #recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def getWord():
    print("Enter your word: ")
    word = input()
    word = word.lower()
    return word

def displayBoard(ART, missedLetters, correctLetters, secretWord):
#TODO:
#Send correct picture to client (depends on how many inocorrect guesses the user has made)
#Send missed letters to client
#Sending secret word with correctly guessed letters appearing and remaining unguessed letters appearing as blanks in the word

def getGuess():
#TODO
#Prompt user to guess a letter
#Receive their guess

def playAgain():
#TODO
#Ask user if they want to play again
#Receive their response 

#Starting game
to_Send = Hangman.BANNER[0]
send_one_message(conn, to_Send)
secretWord = getWord()
print("You Entered: " + secretWord)
to_Send = "Ready to Rumble"
send_one_message(conn, to_Send)

#TODO
#Game loop:
# 1. Send the picture, missed letters, and secret word with correctly guessed letters appearing
#and remaining unguessed letters appearing as blanks in the word 
# 2. Get a letter guess from the user
# 3. If guess is correct, add the letter to correct letters string, and check to to see if ther user has won
# 4. Handle incorrect guess
# 5. When game is over, determine whether or not user wished to play again, and handle the situation

while 1:
    displayBoard(Hangman.ART, missedLetters, correctLetters, secretWord)		
    guess = getGuess()
    print("Guess received.")
    if guess in secretWord:
        print("CORRECT!")
        correctLetters = correctLetters + guess         
        foundAllLetters = True #Check to see if the openent has won
        for i in range(len(secretWord)):
            if secretWord[i] not in correctLetters:
                foundAllLetters = False
                break
        if foundAllLetters:
            displayBoard(Hangman.ART, missedLetters, correctLetters, secretWord)
            send_one_message(conn, "***You Won!***")
            gameOver = True 
    
conn.close()