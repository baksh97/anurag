from twisted.internet import protocol, reactor
from db import *

class Echo(protocol.Protocol):
	def __init__(self):
		self.state = 'init'
		self.db = Database()

	def dataReceived(self, packet):
		# self.transport.write(data)
		print("Rec : ", end="")
		print(packet)
		data = packet.decode("utf-8")
		print("Rec : ", end="")
		print(data)
		if self.state == 'init':
			if data =='l':
				self.send("us")
				self.state = 'user'
			elif data == 'xx':
				print("Connection terminated")
				self.transport.loseConnection()
		else:
			if self.state == 'user':
				self.send("pass")
				self.username = data
				self.state = 'pwd'			# go to password state

			elif self.state == 'pwd':
				valid = self.db.login(self.username, data)
				if not valid:
					self.send("fail")
					self.state = 'init'
					self.username = ""
				else:
					if self.isInst():
						self.send("isucc")
						self.state = 'i_input'
					else:
						st = 'succ'+ self.db.get_name(self.username)
						self.send(st)
						self.state = 's_input'
			elif self.state == 's_input':
				if data == '1':
					marks = self.db.get_marks_student(self.username)
					st = 'g' + self.convListtoStr(marks, ' ')
					self.send(st)
					self.state = 's_input'
				elif data == '2':
					aggr = self.db.get_aggr_student(self.username)
					st = 'h' + str(aggr)
					self.send(st)
					self.state = 's_input'
				elif data == '3':
					res = self.db.get_min_max_student(self.username)
					st = 'j' + self.convListtoStr(res)
					bst,wrst = self.db.get_subjectwise_bw()
					st += ',' + self.convListtoStr(bst) + "," + self.convListtoStr(wrst)
					self.send(st)
					self.state = 's_input'
				elif data == 'x':
					self.state = 'init'
					self.username=""
					self.send("logout")
			elif self.state == 'i_input':
				if data == '1':
					marks = self.db.get_marks_all()
					aggrs = self.db.get_aggr_all()
					st = 'all' + self.formatDict(marks,aggrs)
					self.send(st)
					self.state = 'i_input'
				elif data == '2':
					marks = self.db.get_class_mean()
					st = 'sca' + self.convListtoStr(marks, " ")
					self.send(st)
					self.state = 'i_input'

				elif data == '3':
					marks = self.db.get_num_failed()
					st = 'sf' + self.convListtoStr(marks, " ")
					self.send(st)
					self.state = 'i_input'

				elif data == '4':
					bst,wrst = self.db.get_bestnworst()
					st = 'bw' + self.convListtoStr(bst) + "," + self.convListtoStr(wrst)
					self.send(st)
					self.state = 'i_input'

				elif data == '5':
					self.state = 'update'
					self.send('up')
				elif data == 'x':
					self.state = 'init'
					self.username=""
					self.send("logout")
			elif self.state == 'update':
				params = data.split(',')
				# print(params[2])
				done = self.db.update(params[0], params[1], int(params[2]))
				if done:
					self.send('ups')
				else:
					self.send('upf')
				self.state = 'i_input'

	def convListtoStr(self, arr, sep=","):
			st = str(arr[0])
			arr = arr[1:]
			for e in arr:
				st += sep + str(e)
			return st

	def formatDict(self, d, a):
		st=""
		for name in d:
			st += name
			m = d[name]
			for num in m:
				st += ";" + str(num)
			st += ";" + str(a[name])
			st += ','
		return st[:-1]

	def isInst(self):
		return self.username == 'instructor'

	def send(self, data):
		self.transport.write(data.encode('utf8'))
		print("Sent " + data)

class EchoFactory(protocol.Factory):
	def buildProtocol(self, addr):
		return Echo()



reactor.listenTCP(8000, EchoFactory())
reactor.run()
print("Server Stopped")