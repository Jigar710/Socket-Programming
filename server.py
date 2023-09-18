import socket

from _thread import *
import threading

print_lock = threading.Lock()

dict = {
	"101":{'name':'jigar','id':'202211004'},
	"102":{'name':'sneha','id':'202211016'},
}

def threaded(c):
	global dict
	try:
		while True:
			data = str(c.recv(1024).decode('ascii'))
			print("client sent :",data)
			if not data:
				print('client disconnect')
				print_lock.release()
				break
			if data == 'exit':
				print('client disconnect')
				print_lock.release()
				break
			message = dict.get(str(data),"not found")
			print("msg sent successfully({})".format(message))
			c.send(str(message).encode())
	except:
		print("client disconnect forcefully")
	c.close()


def Main():
	host = ""
	port = 12345
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((host, port))
	print("socket binded to port", port)

	s.listen(5)
	print("socket is listening")

	while True:
		c, addr = s.accept()

		print_lock.acquire()
		print('Connected to :', addr[0], ':', addr[1])

		start_new_thread(threaded, (c,))
	s.close()


if __name__ == '__main__':
	Main()
