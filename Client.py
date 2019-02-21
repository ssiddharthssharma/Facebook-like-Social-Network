import socket
import sys
import select
import errno
from getpass import getpass
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from simplecrypt import encrypt,decrypt
import time

HashingED_suit = AES.new('Keycodevalue1316',AES.MODE_CBC,'09876543210IV456')
Cryptokey='Keycodevalue1316'



def String_PaddingX16(InString):
	Length = len(InString)
	PaddedString = InString
	PaddedString += ((16 - Length % 16)*'~')
	#print ('Padded',PaddedString)
	return PaddedString

def String_Strip_Padding(InString):
	retstring = InString.strip('~')
	retstring2 = retstring.replace('~','')
	return retstring2

def printWelcome():
	print("""\n
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
+                            WELCOME TO THE APPLICATION                               +
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
		\n""")

def take_ToCenter():
	print("							")

def Authenticate_Session():
	while True:
		#Authentication
		#print('username:')
		
		sys.stdout.write('Username:'.rjust(40))
		Username = sys.stdin.readline()
		WriteAuthDataToSock(Username,1,MyClientSock)
		Auth_Reply = Decrypt_recieve()
		if Auth_Reply == "USR_Valid":
			while True:
				#print('password')
				#Password = sys.stdin.readline()
				Password = getpass(prompt='Password:'.rjust(40))
				WriteAuthDataToSock(Password,2,MyClientSock)
				Auth_Reply_Pass = Decrypt_recieve()
				if Auth_Reply_Pass == "Pass_Valid":					
					print("successful login\n".rjust(46))
					return 0
				else:
					print("Auth_Reply_Pass")
					print("Invalid Password".rjust(46))
		else:
			
			print("Invalid user Try again".rjust(49))
		#EndAuth



def WriteAuthDataToSock(String,StrType,MyClientSock):
	#username type 1	
	if StrType == 1:
		#String.replace('\n','')
		#String.splitlines(0)
		stripedString = String.strip()
		req = "<USRNME>%s<USRNME/>" % (stripedString)
		#MyClientSock.sendall(req)
		Encrypt_send(req)
		sys.stdout.flush()	
	#PSWD type 2	
	if StrType == 2:
		req = "<USRPSD>%s<USRPSD/>" % (String)
		#MyClientSock.sendall(req)
		Encrypt_send(req)
		sys.stdout.flush()
	#ReadAuthAck = MyClientSock.recv(1024)
	#if ReadAuthAck == ""

def Encrypt_send(E_Block):
	E_BlockX16 = String_PaddingX16(E_Block)
	cipther_block = HashingED_suit.encrypt(E_BlockX16)
	#cipther_block = encrypt (Cryptokey,E_Block)
	#baseCode= b64encode(cipther_block)
	MyClientSock.sendall(cipther_block)

def Decrypt_recieve():
	Recieved_D = MyClientSock.recv(1024)
	#print("recieved",Recieved_D)
	#baseDecode = b64decode(Recieved_D)
	Plain_block = HashingED_suit.decrypt(Recieved_D)
	Striped_Plain_Block = String_Strip_Padding(Plain_block)
	Striped_Plain_Block = Striped_Plain_Block.replace("[N|L]","\n")
	#Plain_block = decrypt(Cryptokey,Recieved_D)
	#print("resolved",Striped_Plain_Block)
	return Striped_Plain_Block

def Creat_PostReq_from_UI():
	
	sys.stdout.write("To Username:")
	USER_NME = sys.stdin.readline()
	USER_NME = USER_NME.strip()
	sys.stdout.write("Enter_Message:")
	Message = sys.stdin.readline()
	Message = Message.strip()
	ReturnString = "<PTOUSR>%s<PTOUSR/>[D|L]<PTOMSG>%s<PTOMSG/>"%(USER_NME,Message)
	return ReturnString

def Handle_Encode_USRCommand(Command_String):
	Command_String = Command_String.upper()
	stripedString = Command_String.strip()
	request = ""
	if stripedString=="EXIT":
		Encrypt_send("<USRCMD>EXIT<USRCMD/>")
		MyClientSock.close()
		time.sleep(1)
		exit("Good Bye..".rjust(45))
	
	if stripedString=="POST":
		#print('handle Posts')
		Post_Request = Creat_PostReq_from_UI() 
		request = "<USRCMD>%s<USRCMD/>" % (Post_Request)
	
	elif stripedString=="LIST_USERS":
		request = "<USRCMD>%s<USRCMD/>" % (stripedString)
	
	elif stripedString=="SHOW_MY_WALL":
		request = "<USRCMD>%s<USRCMD/>" % (stripedString)
	
	elif stripedString=="SHOW_OTHER_WALL":
		sys.stdout.write("Enter Username:")
		USER_NME = sys.stdin.readline()
		request = "<USRCMD>%s %s<USRCMD/>" % (stripedString,USER_NME)
	else:
		request = "INVAL_CMD"
		print("Not a Valid Command Try again")
	
	return request

def SendRequestToServer():
	ScanLineStr = sys.stdin.readline()
	RequestString = Handle_Encode_USRCommand(ScanLineStr)
	if RequestString != "INVAL_CMD":
		Encrypt_send(RequestString)
	sys.stdout.flush()

def ProcessServerResponse():
	RLine_Server = Decrypt_recieve()
	#sys.stdout.write(RLine_Server)
	print(RLine_Server)
	sys.stdout.flush()
	#print("client sent %s ",RLine_Server)

#create socket
MyClientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
MyClientSock.settimeout(50)
#declaring server address and connecting to it
MyServer_Address = ('localhost', 9090)
MyClientSock.connect(MyServer_Address)
print ('connecting to %s port %s' % MyServer_Address)

printWelcome()
Authenticate_Session()



#communication
wall = "Send me wall data"
#MyClientSock.setblocking(0)
while True:
	
	ReadReady,WriteReady,InError = select.select([MyClientSock,sys.stdin],[MyClientSock],[],0)
	for ReadListIteam in ReadReady:
	    if ReadListIteam == sys.stdin:
			
			SendRequestToServer()
	    if ReadListIteam == MyClientSock:
			ProcessServerResponse()

MyClientSock.close()



