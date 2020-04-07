import sys
import os
import json
import uuid
import logging
from queue import  Queue

class Chat:
	def __init__(self):
		self.sessions={}
		self.users = {}
		self.users['adip']={ 'nama': 'Adip dwi yanto', 'negara': 'Argentina', 'password': 'surabaya', 'incoming' : {}, 'outgoing': {}}
		self.users['jisoo']={ 'nama': 'Kim Jisoo', 'negara': 'Inggris', 'password': 'surabaya', 'incoming': {}, 'outgoing': {}}
		self.users['lisa']={ 'nama': 'Lalisa Manoban', 'negara': 'Inggris', 'password': 'surabaya','incoming': {}, 'outgoing':{}}
		self.users['lutfiyanti']={ 'nama': 'Lutfiyanti', 'negara': 'Indonesia', 'password': 'lalalala','incoming': {}, 'outgoing':{}}
	def proses(self,data):
		j=data.split(" ")
		try:
			command=j[0].strip()
			if (command=='auth'):
				username=j[1].strip()
				password=j[2].strip()
				logging.warning("AUTH: auth {} {}" . format(username,password))
				return self.autentikasi_user(username,password)
			elif (command=='send'):
				sessionid = j[1].strip()
				usernameto = j[2].strip()
				message=""
				for w in j[3:]:
					message="{} {}" . format(message,w)
				usernamefrom = self.sessions[sessionid]['username']
				logging.warning("SEND: session {} send message from {} to {}" . format(sessionid, usernamefrom,usernameto))
				return self.send_message(sessionid,usernamefrom,usernameto,message)
			elif (command=='inbox'):
				sessionid = j[1].strip()
				username = self.sessions[sessionid]['username']
				logging.warning("INBOX: {}" . format(sessionid))
				return self.get_inbox(username)

			#
			# FITUR BARU: MELIHAT LIST USER YANG SEDANG AKTIF
			#
			elif (command=='active'):
				sessionid = j[1].strip()
				logging.warning("ACTIVE USER: {}" . format(sessionid))
				return self.active()	
    				
			#
			# FITUR BARU: LOGOUT
			#
			elif (command=='logout'):
				sessionid = j[1].strip()
				logging.warning("LOGOUT: {}" . format(sessionid))
				return self.logout(sessionid)
			
    				
			else:
				return {'status': 'ERROR', 'message': 'Sorry, wrong protocol'}
		except KeyError:
			return { 'status': 'ERROR', 'message' : 'Information not found [Key Error]'}
		except IndexError:
			return {'status': 'ERROR', 'message': 'Sorry, wrong protocol [Index Error]'}
	def autentikasi_user(self,username,password):
		if (username not in self.users):
			return { 'status': 'ERROR', 'message': 'Sorry, user not found. Check again.' }
		if (self.users[username]['password']!= password):
			return { 'status': 'ERROR', 'message': 'Sorry, wrong password. Check again.' }
		tokenid = str(uuid.uuid4()) 
		self.sessions[tokenid]={ 'username': username, 'userdetail':self.users[username]}
		return { 'status': 'OK', 'tokenid': tokenid }
	def get_user(self,username):
		if (username not in self.users):
			return False
		return self.users[username]
	def send_message(self,sessionid,username_from,username_dest,message):
		if (sessionid not in self.sessions):
			return {'status': 'ERROR', 'message': 'Session not found'}
		s_fr = self.get_user(username_from)
		s_to = self.get_user(username_dest)
		
		if (s_fr==False or s_to==False):
			return {'status': 'ERROR', 'message': 'Sorry, user not found. Check again.'}

		message = { 'msg_from': s_fr['nama'], 'msg_to': s_to['nama'], 'msg': message }
		outqueue_sender = s_fr['outgoing']
		inqueue_receiver = s_to['incoming']
		try:	
			outqueue_sender[username_from].put(message)
		except KeyError:
			outqueue_sender[username_from]=Queue()
			outqueue_sender[username_from].put(message)
		try:
			inqueue_receiver[username_from].put(message)
		except KeyError:
			inqueue_receiver[username_from]=Queue()
			inqueue_receiver[username_from].put(message)
		return {'status': 'OK', 'message': 'Message Sent'}

	def get_inbox(self,username):
		s_fr = self.get_user(username)
		incoming = s_fr['incoming']
		msgs={}
		for users in incoming:
			msgs[users]=[]
			while not incoming[users].empty():
				msgs[users].append(s_fr['incoming'][users].get_nowait())
			
		return {'status': 'OK', 'messages': msgs}
	#
	# FITUR BARU: LOGOUT
	#
	def logout(self, sessionid):
		del self.sessions[sessionid]
		return {'status': 'OK', 'messages': "Logout success!"}
	#
	# FITUR BARU: MELIHAT LIST USER YANG SEDANG AKTIF
	#
	def active(self):
		token = list(self.sessions.keys())
		active = ""
		for i in token:
			active = active + self.sessions[i]['username']+ ", "
		return {'status': 'OK', 'message': '{}' .format(active)}


if __name__=="__main__":
	j = Chat()
	sesi = j.proses("auth messi surabaya")
	print(sesi)
	#sesi = j.autentikasi_user('messi','surabaya')
	#print sesi
	tokenid = sesi['tokenid']
	print(j.proses("send {} henderson hello gimana kabarnya son " . format(tokenid)))
	print(j.proses("send {} messi hello gimana kabarnya mess " . format(tokenid)))

	#print j.send_message(tokenid,'messi','henderson','hello son')
	#print j.send_message(tokenid,'henderson','messi','hello si')
	#print j.send_message(tokenid,'lineker','messi','hello si dari lineker')


	print("isi mailbox dari messi")
	print(j.get_inbox('messi'))
	print("isi mailbox dari henderson")
	print(j.get_inbox('henderson'))
















