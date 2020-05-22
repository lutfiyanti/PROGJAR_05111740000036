import socket
import time
import sys
import asyncore
import logging
from http import HttpServer

httpserver = HttpServer()
rcv = ""

class ProcessTheClient(asyncore.dispatcher_with_send):
	def handle_read(self):
		global rcv
		data = self.recv(1024)
		if data:
			d = data.decode()
			rcv = rcv + d
			if rcv[-2:] == '\r\n':
				# end of command, proses string
				#logging.warning("data dari client: {}".format(rcv))
				hasil = httpserver.proses(rcv)
				#hasil sudah dalam bentuk bytes
				hasil = hasil + "\r\n\r\n".encode()
				#agar bisa dioperasikan dengan string \r\n\r\n maka harus diencode dulu => bytes

				#nyalakan ketika proses debugging saja, jika sudah berjalan, matikan
				#logging.warning("balas ke  client: {}".format(hasil))
				self.send(hasil) #hasil sudah dalam bentuk bytes, kirimkan balik ke client
				rcv = ""
				self.close()

		#self.send('HTTP/1.1 200 OK \r\n\r\n'.encode())
			#self.send("{}" . format(httpserver.proses(d)))
		self.close()

class Server(asyncore.dispatcher):
	def __init__(self,addr):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind(addr)
		self.listen(5)
		logging.warning("running on address {}" . format(addr))

	def handle_accept(self):
		pair = self.accept()
		if pair is not None:
			sock, addr = pair
			logging.warning("connection from {}" . format(repr(addr)))
			handler = ProcessTheClient(sock)

def server_run(addrs):
	address=addrs
	svr_ls = []
	for addr in address:
		svr = Server(addr)
		svr_ls.append(svr)
	asyncore.loop()

if __name__=="__main__":
	server_run([9002])

