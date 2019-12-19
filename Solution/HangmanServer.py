#!/usr/bin/env python

# Useful link for sockets: https://realpython.com/python-sockets/
# Usefuk link for send/recv msgs in a socket cxn: https://stackoverflow.com/questions/17667903/python-socket-receive-large-amount-of-data/17697651
# Useful link for encoding strings: https://www.programiz.com/python-programming/methods/string/encode
   
import socket
import struct
import Hangman

missedLetters = ''
correctLetters = ''
gameOver = False

TCP_IP = 'localhost' #loopback address
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
    to_Send = Hangman.ART[len(missedLetters)]
    send_one_message(conn, to_Send)
    to_Send = ('\nMissed letters: ' + missedLetters + '\n')
    send_one_message(conn, to_Send)
    blanks = '_' * len(secretWord)  
    #Replace blanks with correctly guessed letters 
    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]
    
    blanksSpaced = ''
    for i in blanks:
        blanksSpaced += i+' '
    blanksSpaced = blanksSpaced + '\n' #Show secret word with spaces in between each letter 
    to_Send = blanksSpaced
    send_one_message(conn, to_Send)

def getGuess():
    to_Send = 'Guess a letter.'
    send_one_message(conn, to_Send)
    guess = recv_one_message(conn)
    print('Got the guess: ' + guess)
    guess = guess.lower()
    return guess 
    #Good to add input checks to this function (i.e., Is it a letter? Was it already guessed?)

def playAgain():
    to_Send = 'Do you want to play again?'
    send_one_message(conn, to_Send)
    resp = recv_one_message(conn)
    print("Answer: " + resp)
    return resp.lower().startswith('y')

#Starting game
to_Send = Hangman.BANNER[0]

send_one_message(conn, to_Send)
secretWord = getWord()
print("You Entered: " + secretWord)
to_Send = "Ready to Rumble"
send_one_message(conn, to_Send)

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
            send_one_message(conn, "***You Won!***")
            gameOver = True 
    else:
        print("INCORRECT!")
        missedLetters = missedLetters + guess       
        #Check if too many wrong guesses
        if len(missedLetters) == len(Hangman.ART) - 1:
            displayBoard(Hangman.ART, missedLetters, correctLetters, secretWord)
            send_one_message(conn, "****You have lost!***")
            gameOver = True
    
    if gameOver:
        if playAgain():
            missedLetters = ''
            correctLetters = ''
            gameOver = False 
            secretWord = getWord()
        else: 
            break
conn.close()