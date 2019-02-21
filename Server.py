import socket
import sys
import errno
import select
from getpass import getpass
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from simplecrypt import encrypt,decrypt
from thread import *
import threading
import os
import time
import sqlite3
from sqlite3 import Error
#from datetime import datetime
import datetime
import time


HashingED_suit = AES.new('Keycodevalue1316',AES.MODE_CBC,'09876543210IV456')
Cryptokey='Keycodevalue1316'

#connect to Database
connectionFD = sqlite3.connect("MasterDB.db")

def String_Strip_Padding(InString):
	return InString.strip('~')

def RetrivrPassFor(ClientString):
	DB_Cursor_IP= connectionFD.cursor()
	DB_Cursor_IP.execute("SELECT PASSWORD FROM USER_CREDS WHERE USER_NAME = ?",(ClientString,))
	Rows = DB_Cursor_IP.fetchall()
	for row in Rows:
		#print(row[0])
		StrofRow = (row[0])
	return StrofRow

	


def Query_Creat_UserList():
	
	DB_Cursor_IP= connectionFD.cursor()
	DB_Cursor_IP.execute("SELECT * FROM USER_CREDS")
	Rows = DB_Cursor_IP.fetchall()
	DB_USR_LIST=""
	
	for row in Rows:
		StrofRow = "%s,"%(row[0])
		DB_USR_LIST += str(StrofRow)
	return DB_USR_LIST

NEW_DB_USER = Query_Creat_UserList()
NEW_DB_USER_LIST = NEW_DB_USER.split(',')
#print(NEW_DB_USER_LIST)

User_List = NEW_DB_USER_LIST

#LoggedinUser=""

def Autenticate_User():
	global LoggedinUser
	while True:
		#Authentication
		Creds = Recive_Decrypt()
		#print (Creds)
		UserNameAuth = Request_Decoder(Creds)
		if 	UserNameAuth == "Valid":
			#print (UserNameAuth)
			Encrypt_Send("USR_Valid")
			
			while True:
				#ServerEP_Connectedclient.sendall("USR_Valid")
				CredsPass = Recive_Decrypt()
				#print(CredsPass)
				AuthPass = Match_Pass_User(Creds,CredsPass)
				if AuthPass == "Pass_Valid":
					Encrypt_Send("Pass_Valid")
					LoggedinUser = Extract_Embeded_string(Creds)
					#print(LoggedinUser)
					return 0
				else:
					Encrypt_Send("Pass_InValid")	
		else:
			print (UserNameAuth)
			Encrypt_Send("USR_Invalid")
		#AuthEnd


#haspassword and querry DB
def Match_Pass_User(Creds,CredsPass):
	#Figure it out
	RequestType = CredsPass[:8]
	if RequestType == "<USRPSD>":
		PassString = Extract_Embeded_string(CredsPass)
		USER_name = Extract_Embeded_string(Creds)
		#print(PassString)
		if PassString == "000":
			return "Pass_Valid"
		else:
			return "Pass_invalid"



def CreateNotification_TO_Send(Row):
	StringRow=""
	StringRow = "------------------------||Notification||--------------------------------\
					[N|L]Post From: %s | T0: %s | Date: %s |\
					[N|L]Message  : %s | \
					[N|L]------------------------------------------------------------------------[N|L]"% (Row[1],Row[2],Row[4],Row[3])
	Encrypt_Send(StringRow)		
	#print(Row)
	#print(StringRow)


def The_Notification_service():
	DB_Cursor_IP= connectionFD.cursor()
	DB_Cursor_IP.execute("SELECT * FROM ALL_POSTS")
	Rows = DB_Cursor_IP.fetchall()
	for row in Rows:
		StrofRow = "%s"%(row[5])
		if LoggedinUser not in StrofRow:
			CreateNotification_TO_Send(row)	
			New_SENT_to_LIST = "%s,%s"%(StrofRow,LoggedinUser)
			Args = (New_SENT_to_LIST,row[0])	
			DB_Cursor_IP.execute("UPDATE ALL_POSTS SET SENT_TO_LIST= ? WHERE POST_ID= ? ",Args)
			connectionFD.commit()


def CreatePost_TO_Send(Rows):
	StringRow=""
	for Row in Rows:
		StringRow = "------------------------------------------------------------------------\
					[N|L]Post From: %s | T0: %s | Date: %s |\
					[N|L]Message  : %s | \
					[N|L]------------------------------------------------------------------------[N|L]"% (Row[1],Row[2],Row[4],Row[3])
		Encrypt_Send(StringRow)		
		#print(Row)
		#print(StringRow)

def Querry_Post_for_wall(UserName):
	#print('quering')
	#print(UserName)
	#print(LoggedinUser)
	if UserName in User_List:
		DB_Cursor_IP= connectionFD.cursor()
		DB_Cursor_IP.execute("SELECT * FROM ALL_POSTS WHERE ON_USER = ?",(UserName,))
		Rows = DB_Cursor_IP.fetchall()
		CreatePost_TO_Send(Rows)
		return "[N|L]||End OF WALL||[N|L]"
	else:
		return "[N|L]||User Doesn't Exist||[N|L]"

def String_PaddingX16(InString):
	Length = len(InString)
	PaddedString = InString
	PaddedString += ((16 - Length % 16)*'~')
	#print ('Padded',PaddedString)	 
	return PaddedString



def Recive_Decrypt():
	D_block = ServerEP_Connectedclient.recv(1024)
	#print('recieved: ',D_block)
	#baseDecode = b64decode(D_block)
	Plain_block = HashingED_suit.decrypt(D_block)
	Striped_Plain_Block = String_Strip_Padding(Plain_block)
	#Plain_block = decrypt(Cryptokey,D_block)
	#print('resolved: ',Striped_Plain_Block)
	return Striped_Plain_Block;

def Encrypt_Send(E_Block):
	E_BlockX16 = String_PaddingX16(E_Block)
	Cipher_block = HashingED_suit.encrypt(E_BlockX16)
	#Cipher_block = encrypt (Cryptokey,E_Block)
	#baseCode= b64encode(Cipher_block)
	ServerEP_Connectedclient.sendall(Cipher_block)






def send_User_List():
	Encrypt_Send("[N|L]------All Users-------[N|L]")
	i=1
	space=" "
	for Name in User_List:
		sNAme=Name.strip()
		Stringg = "%d)  %s   %s[N|L]" %(i,space,sNAme)
		Encrypt_Send(Stringg)
		i=i+1
		if i==10:
			space=""
	Encrypt_Send("----------------------")



def Insert_Post(Values):
	DB_Cursor_IP= connectionFD.cursor()
	InsertPost_ST = """INSERT INTO ALL_POSTS(POST_ID,By_USER,ON_USER,POST_TEXT,TIME_STAMP,SENT_TO_LIST)
						VALUES(?,?,?,?,?,?)"""	
	DB_Cursor_IP.execute(InsertPost_ST,Values)
	connectionFD.commit()



def Process_POST(Exact_Request_String):
	User_NAME,Message = Exact_Request_String.split('[D|L]')
	User_NAME = Extract_Embeded_string(User_NAME)
	Message = Extract_Embeded_string(Message)
	if User_NAME in User_List:
		#CalRowID
		DB_Cursor_IP= connectionFD.cursor()
		DB_Cursor_IP.execute("SELECT MAX(POST_ID) FROM ALL_POSTS")
		RowsID = DB_Cursor_IP.fetchall()
		for rowpin in RowsID:		
			MaxRowID = rowpin[0]
		#print(MaxRowID)
		MaxRowID = MaxRowID+1
		time_now = datetime.datetime.now()
		DT_string = str(time_now)
		Values=(MaxRowID,LoggedinUser,User_NAME,Message,DT_string,LoggedinUser)
		Insert_Post(Values)
	else:
		return "[N|L]||User Doesn't Exist||[N|L]"

	return "[N|L]||Message Posted||[N|L]"



def Build_Response_From_Request(Exact_Request_String):
	
	if Exact_Request_String == "EXIT":
		ServerEP_Connectedclient.close()
		exit()
		
	elif Exact_Request_String == "LIST_USERS":
		send_User_List()
		ClientResponse = "[N|L]||END OF LIST||[N|L]"

	elif Exact_Request_String == "SHOW_MY_WALL":
		WallData = Querry_Post_for_wall(LoggedinUser)
		ClientResponse = WallData

	elif Exact_Request_String[:15] == "SHOW_OTHER_WALL":
		Other_user =  Exact_Request_String [16:]
		OWallData = Querry_Post_for_wall(Other_user)
		ClientResponse = OWallData

	elif Exact_Request_String[:8] == "<PTOUSR>":
		#print(Exact_Request_String)
		ResponsetoPost = Process_POST(Exact_Request_String)
		ClientResponse = ResponsetoPost
	else:
		print(Exact_Request_String)
		ClientResponse = "Server Does not support this command"
	return ClientResponse

def Read_User_Command():
	#print('command called')
	#RLine_client = ServerEP_Connectedclient.recv(1024)
	RLine_client = Recive_Decrypt()
	#sys.stdout.write(RLine_client)
	ExtractedString = Extract_Embeded_string(RLine_client)
	Respone_to_Client = Build_Response_From_Request(ExtractedString)
	Encrypt_Send(Respone_to_Client)
	sys.stdout.flush()
	#print("client sent %s ", RLine_client)

def Send_stdin():
	ScanLineStr = sys.stdin.readline()
	ScanLineStr = ScanLineStr.strip()
	#ServerEP_Connectedclient.sendall(ScanLineStr)
	if ScanLineStr[:4]=="exit":
		ServerEP_Connectedclient.close()
		
		exit()
	Encrypt_Send(ScanLineStr)
	sys.stdout.flush()

def Extract_Embeded_string(Request_string):
	tmp = Request_string	
	req_str = tmp[8:]
	tmp2 = req_str[::-1]
	final_str = tmp2[9:]
	actual_str = final_str[::-1]
	#print (actual_str)
	return actual_str.strip()

def Request_Decoder(Request_string):
	RequestType = Request_string[:8]
	if RequestType == "<USRNME>":
		username = Extract_Embeded_string(Request_string)
		if username in User_List:
			#LoggedinUser = username
			#print(LoggedinUser)
			return "Valid"
		else:
			return "Invalid"
	





def ThreadEntry(ServerEP_Connectedclient):
	
	
	Autenticate_User()
	time.sleep(2)
	The_Notification_service()
	dbchange = 0
	#ServerEP_Connectedclient.settimeout(2)
	while True:
		#Myserversocket.setblocking(0)
		ReadReady,WriteReady,InError = select.select([ServerEP_Connectedclient,sys.stdin],[ServerEP_Connectedclient],[],0)
		for ReadySock in ReadReady:
			if ReadySock == ServerEP_Connectedclient:
				Read_User_Command()
			

			#ScanLineStr = raw_input("> ")
			if ReadySock == sys.stdin:
				Send_stdin()
			
			    
		if dbchange == 0:
			The_Notification_service()
		

	#releasing the resources
	ServerEP_Connectedclient.close()
	









##main
#creating socket
Myserversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#Myserversocket.setblocking(0)

#server socket bind and listen
server_address = ('localhost', 9090)
Myserversocket.bind(server_address)
Myserversocket.listen(10)
print('listening...')


while True:
	try:
		# accepting a client
		ServerEP_Connectedclient, client_address = Myserversocket.accept()
		ServerEP_Connectedclient.settimeout(100)
		#print ('accepted..',client_address)
	
		#print("ParentPID {}".format(os.getpid()))
		try:
			pid = os.fork()
		except OSError:
			exit("Could not creat a Child Process")

		if pid == 0:
			#print("ChildPID {}".format(os.getpid()))
			Myserversocket.close()
			ThreadEntry(ServerEP_Connectedclient)
			exit()

		if pid > 0:
			ServerEP_Connectedclient.close()
	except KeyboardInterrupt:
		Myserversocket.close()
		exit()
	
	
#releasing Resources
connectionFD.close()
Myserversocket.close()
