studentID = -1

def signup(s):
	print("enter username and password:")
	username = (str)input()
	password = (str)input()
	s.send("signup".encode())
	s.send(username.encode())
	s.send(password.encode())
	instru = s.recv(10).decode()
	if(instru=='1'):
		teacherOptions()
	elif(instru==-1):
		print("invalid credentials")
		signup()
	else:
		studentID = (int)instru
		studentOptions()


def studentOptions():
	print("Choose action:")
	print("0- Signout")
	print("1- Marks")
	print("2- Aggregate")
	print("3- Max-Min")
	action = (int)input()
	if(action==1):

	elif(action==2):
	elif(action==3):
	elif(action==0):
	else:
		print("Invalid action")

def sMarks(s):
	# print("enter subject name or 0 to go back")
	# subject = (str)(input())
	# if(subject=="0"):
	# 	studentOptions()
	# else:
	s.send("sMarks".encode())
	# s.send(subject.encode())

	ans = s.recv(1024).decode()
	print(ans)
	print("\n\n")
	print("press any to go back")
	input()
	studentOptions()


def sAggregate():
	

def sMaxMin():


def tMarks():

def tAverage():


def tNumFailed():

def tBestWorst():

def tUpdate():



def teacherOptions():
