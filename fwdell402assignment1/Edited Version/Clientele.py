from twisted.internet import reactor,protocol,task
import time
import os
import sys

class EchoClient(protocol.Protocol):
	def __init__(self, message):
		self.message = message
		self.state = "init"
	def dataReceived(self,data):	
		self.handleData(data)
	def connectionMade(self):
		self.transport.write("l".encode("utf8"))

	def handleData(self,data):
		os.system('clear')
		if(data=="us"):					
			print("Please Enter Username:\n")
			x = input();
			self.send(x)
		elif(data=="usa"):
			self.send("l")		
		elif(data=="pass"):
			print("Enter Password:\n")
			x = input();
			self.send(x)
		elif(data=="fail"):
			print("Login Failed.")
			self.handleData("usa")
		elif(data[0:4]=="succ"):
			if(len(data)>4):
				self.studentName = data[4:]
			
			print("Welcome " + self.studentName)
			print("\n")
			print("Choose Option:") 
			print("1. Grades")
			print("2. Aggregate")
			print("3. Min/Max")
			print("\n")
			print("Press x to logout") 
			
			x = input()
			while(x not in ['1','2','3','x']):
				print("Enter 1,2,3 or x")
				x = input()
			self.send(x)

		elif(data=="logout"):
			
			print("Press L to login, X to exit") 
			x = input()
			while(x not in ['l','x']):
				print("Enter l or x")
				x = input()
			if(x=="l"):
				self.send("l")
			if(x=="x"):
				self.send("xx")
				self.transport.loseConnection()
	
				
		elif(data[0:1]=="g"):			
			s = data[1:].split(" ")
			
			for i in range(5):
				print(self.getSubject(i) + " - " + s[i])
			print("\n")
			print("Press x to go back") 
			x=input()
			while(x!="x"):
				x=input()
			self.handleData("succ")
		elif(data[0:1]=="h"):
			
			print("Aggregate :" + data[1:])
			print("\n")
			print("Press x to go back") 
			x=input()
			while(x!="x"):
				x=input()
			self.handleData("succ")
		elif(data[0:1]=="j"):
			s = data[1:].split(",")
			print("Personal Record")
			print("\n")
			print("\tMinimum Marks in " + s[0] + " : " + s[1])
			print("\tMaximum Marks in " + s[2] + " : " + s[3])
			print("\n\n")
			print("Overall Record")
			print("\n")
			print("Subject\t\t\tMax\tMin")
			print(self.getSubject(0) + "\t\t:\t"+s[4]+"\t"+s[9])
			print(self.getSubject(1) + "\t\t:\t"+s[5]+"\t"+s[10])
			print(self.getSubject(2) + "\t\t:\t"+s[6]+"\t"+s[11])
			print(self.getSubject(3) + "\t:\t"+s[7]+"\t"+s[12])
			print(self.getSubject(4) + "\t:\t"+s[8]+"\t"+s[13])		


			print("\n")
			print("Press x to go back") 
			x=input()
			while(x!="x"):
				x=input()
			self.handleData("succ")


		elif(data=="isucc"):
			print("Welcome Instructor") 
			
			print("Choose Option:") 
			print("1. Show Student Grades")
			print("2. Show Class Average")
			print("3. Number of Failing Students")
			print("4. Performance Wise Data")
			print("5. Update Marks")
			print("\n")
			print("Press x to logout") 
			
			x = input()
			while(x not in ['1','2','3','4','5','x']):
				print("Enter 1,2,3,4,5 or x")
				x = input()
			self.send(x)			

		elif(data[0:3]=="all"):
			s = data[3:]
			sp = s.split(",")
			sName=["Name\t\t\t"]
			s1=["English\t\t"]
			s2=["Math\t\t"]
			s3=["Physics\t\t"]
			s4=["Chemistry\t"]
			s5=["Computers\t"]
			sagg=["Aggregate"]
			for sps in sp:
				sd = sps.split(";")
				if(len(sd[0]) > 20):
					sd[0] = sd[0][:20]
				else:
					n = 20-len(sd[0])
					sd[0] = sd[0] + ' '*n

				sName.append(sd[0]+"\t")
				s1.append(sd[1]+"\t\t")
				s2.append(sd[2]+"\t\t")
				s3.append(sd[3]+"\t\t")
				s4.append(sd[4]+"\t\t")
				s5.append(sd[5]+"\t\t")
				sagg.append(sd[6]+"\t\t")
			for row in zip(sName,s1,s2,s3,s4,s5,sagg):
				print('\t'.join(row))

			print("\n")
			print("Press x to go back") 
			x=input()
			while(x!="x"):
				x=input()
			self.handleData("isucc")
		elif(data[0:3]=="sca"):
			s=data[3:].split(" ")
			print("Subject \t:\t Class Averages")
			print("\n")
			print(self.getSubject(0) + "\t\t:\t" + s[0])
			print(self.getSubject(1) + "\t\t:\t" + s[1])
			print(self.getSubject(2) + "\t\t:\t" + s[2])
			print(self.getSubject(3) + "\t:\t" + s[3])
			print(self.getSubject(4) + "\t:\t" + s[4])
			print("\n")
			print("Press x to go back") 
			x=input()
			while(x!="x"):
				x=input()
			self.handleData("isucc")

		elif(data[0:2]=="sf"):
			s=data[2:].split(" ")
			print("Subject \t:\t No. of Failures")
			print("\n")
			print(self.getSubject(0) + "\t\t:\t" + s[0])
			print(self.getSubject(1) + "\t\t:\t" + s[1])
			print(self.getSubject(2) + "\t\t:\t" + s[2])
			print(self.getSubject(3) + "\t:\t" + s[3])
			print(self.getSubject(4) + "\t:\t" + s[4])
			print("\n")
			print("Press x to go back") 
			x=input()
			while(x!="x"):
				x=input()
			self.handleData("isucc")

		elif(data[0:2]=="bw"):
			s=data[2:].split(",")
			print("Subject \t\t Best\t\t Worst")
			print("\n")
			print(self.getSubject(0) +"\t\t\t"+ s[0] + "\t\t" + s[6])
			print(self.getSubject(1) +"\t\t\t"+ s[1] + "\t\t" + s[7])
			print(self.getSubject(2) +"\t\t\t"+ s[2] + "\t\t" + s[8])
			print(self.getSubject(3) +"\t\t"+ s[3] + "\t\t" + s[9])
			print(self.getSubject(4) +"\t\t"+ s[4] + "\t\t" + s[10])

			print("Aggregate \t\t"+ s[5] + "\t\t" + s[11])
			print("\n")
			print("Press x to go back") 
			x=input()
			while(x!="x"):
				x=input()
			self.handleData("isucc")
		elif(data=="up"):
			print("Enter Student Name") 
			sname = input()
			print("Enter Subject to change")
			print("1. English\n2. Math\n3. Physics\n4. Chemistry\n5. Computers")
			ssub= input()
			while(ssub not in ('1','2','3','4','5')):
				print("enter correct subject code")
				ssub=input()
			print("Enter New Marks")
			smark = input()
			while(not(str.isdigit(smark)) or ( int(smark) < 0 or int(smark) > 100) ):
				print("Enter marks within bounds and of proper type")
				smark = input()
			
			self.send(sname+","+self.getSubject(int(ssub)-1)+","+smark);
		elif(data=="ups"):
			print("Update Sucessfull")
			time.sleep(2)
			self.handleData("isucc")
		elif(data=="upf"):
			print("Update Failed") 
			time.sleep(2)
			self.handleData("isucc")
			
			
			 
	def getSubject(self,s):
		if (s==0):
			return "English"
		elif (s==1):
			return "Math"
		elif (s==2):
			return "Physics"
		elif (s==3):
			return "Chemistry"
		elif (s==4):
			return "Computers"
		


	def send(self,data):
		self.transport.write(data.encode("utf8"))
		

class EchoFactory(protocol.ClientFactory):
	def __init__(self,message):
		self.message=message

	def buildProtocol(self, addr):
		return EchoClient(self.message)
	def clientConnectionLost(self, connector, reason):
		reactor.stop()
	def clientConnectionFailed(self,connector, reason):
		reactor.stop()



def main():
	if len(sys.argv) == 2:
		reactor.connectTCP(sys.argv[1],8000, EchoFactory("abcd"))
		reactor.run() 
		print("Connection Terminated")
	else:
		print("Incorrect number of arguments. Correct usage: python Clientele.py <server-ip-address>")

if __name__ == '__main__':
	main()
