import sqlite3
from sqlite3 import Error
from getpass import getpass
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

User_List = ["Oprime","Client001","Client002","Client003","Client004","Client005",\
			"Client006","Client007","Client008","Client009","Client010",\
			"Client011","Client012","Client013","Client014","Client015",\
			"Client016","Client017","Client018","Client019","Client020"]


def String_PaddingX16(InString):
	Length = len(InString)
	PaddedString = InString
	PaddedString += ((16 - Length % 16)*'~')
	#print ('Padded',PaddedString)
	return PaddedString

HashingED_suit = AES.new('Keycodevalue1316',AES.MODE_CBC,'09876543210IV456')
Default_Password = getpass()
Padded_PASS = String_PaddingX16(Default_Password)
cipher_block_PSWD1 = HashingED_suit.encrypt(Padded_PASS)
cipher_block_PSWD= b64encode(cipher_block_PSWD1)


#try:
connectionFD = sqlite3.connect("MasterDB.db")

#except Error as e:
#print(e)

#creating tables
All_Post_Table_ST = """CREATE TABLE IF NOT EXISTS ALL_POSTS(
					POST_ID integer,
					By_USER text,
					ON_USER text,
					POST_TEXT text,
					TIME_STAMP text,
					SENT_TO_LIST text
					);"""

POST_IT_TABLE_ST = """CREATE TABLE IF NOT EXISTS POST_ID_MAX(
					MAX_ROWNUM integer
					);"""

USER_CREDS_Table_ST = """CREATE TABLE IF NOT EXISTS USER_CREDS(
					USER_NAME text,
					PASSWORD text
					);"""
#create the tables

DB_Cursor= connectionFD.cursor()
DB_Cursor.execute(All_Post_Table_ST)
DB_Cursor.execute(POST_IT_TABLE_ST)
DB_Cursor.execute(USER_CREDS_Table_ST)
print ('Tables Created')
	

#Populate the tables 

def Insert_Post(connectionFDP,Values):
	DB_Cursor_IP= connectionFD.cursor()
	InsertPost_ST = """INSERT INTO ALL_POSTS(POST_ID,By_USER,ON_USER,POST_TEXT,TIME_STAMP,SENT_TO_LIST)
						VALUES(?,?,?,?,?,?)"""	
	DB_Cursor_IP.execute(InsertPost_ST,Values)
	

def Update_Post(connectionFDP,Values):
	DB_Cursor_IP= connectionFD.cursor()
	InsertPost_ST = """UPDATE ALL_POSTS SET SENT_TO_LIST= ? 
						WHERE POST_ID= ? )"""	
	DB_Cursor_IP.execute(InsertPost_ST,Values)


def Select_Post(connectionFDP,UserNM):
	DB_Cursor_IP= connectionFD.cursor()
	DB_Cursor_IP.execute("SELECT * FROM ALL_POSTS WHERE POST_ID = ?",(UserNM,))
	Rows = DB_Cursor_IP.fetchall()
	StringRow=""
	for Row in Rows:
		StringRow = "%d | %s | %s | %s | %s | %s " % (Row[0],Row[1],Row[2],Row[3],Row[4],Row[5])
		#print(Row)
		#print(StringRow)
	
def Select_ALL_USER_CREDS(connectionFDP,UserNM):
	DB_Cursor_IP= connectionFD.cursor()
	DB_Cursor_IP.execute("SELECT * FROM ALL_POSTS WHERE POST_ID = ?",(UserNM,))
	Rows = DB_Cursor_IP.fetchall()
	StringRow=""
	for Row in Rows:
		StringRow = "%d | %s | %s | %s | %s | %s " % (Row[0],Row[1],Row[2],Row[3],Row[4],Row[5])
		#print(Row)
		#print(StringRow)



def Populate_UserCreds():
	
	DB_Cursor_IP = connectionFD.cursor()
	for USR_NM in User_List:
		RowVals=(USR_NM,cipher_block_PSWD)
		DB_Cursor_IP.execute("INSERT INTO USER_CREDS(USER_NAME,PASSWORD)VALUES(?,?)",RowVals)



First_Post = (1,'Client001','Client002','Hello User 2','2018-12-03 07:05:10.889828 ','Client020')
Insert_Post (connectionFD,First_Post)
#print('inserted1')

First_Post2 = (2,'Client001','Client003','Hello and have a beautiful day','2018-12-04 07:05:10.889828 ','Client020')
Insert_Post (connectionFD,First_Post2)

DB_Cursor_IP = connectionFD.cursor()
DB_Cursor_IP.execute("INSERT INTO POST_ID_MAX(MAX_ROWNUM)VALUES(2)")



PUserNM = 1
Select_Post(connectionFD,PUserNM)

Populate_UserCreds()

print("Database created successfully!!")


	#finally:
connectionFD.commit()
connectionFD.close()
