#!/usr/bin/env python

import socket
import sys
import threading
import time
import Tkinter as tk
import Queue
import struct


#Get the ip address of the server that the user wants to connect to
server_ip = raw_input("Please enter the ip address of the server: ")
#Get the connection choice from the user
connection_choice = raw_input("Would you like to use TCP or UDP: ")
connection_choice = connection_choice.lower()

if connection_choice == "tcp":
	#Set up the connection variables
	SERVER_IP = server_ip
	TCP_PORT = 62
	BUFFER_SIZE = 1024
	MESSAGE = "Hello, "+SERVER_IP

	#Get the socket
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((SERVER_IP, TCP_PORT))
		s.send(MESSAGE)
	except socket.error as err_msg:
		print ("Error: could not create socket")
		print ("Description: " + str(err_msg))
		sys.exit()

	class clientApp():
		def __init__(self):
			self.root = tk.Tk()
			self.queue = Queue.Queue()
			self.thread = threadReceive(self.queue)
			self.thread.daemon = True
			self.thread.start()
			self.root.after(100, self.processData)
			self.text_output = tk.Text(height=25, insertwidth=3)
			self.input_label = tk.Label(text="User input: ")
			self.input_text = tk.Entry(bd=3, width=30)
			self.input_button = tk.Button(text="Enter", command=self.sendMessages)
			self.dis_button = tk.Button(text="Disconnect", command=self.Disconnect)
			self.dis_button.pack(side=tk.BOTTOM)
			self.input_button.config(relief = tk.SUNKEN)
			self.text_output.pack(side=tk.TOP)
			self.input_label.pack(side = tk.LEFT)
			self.input_text.pack(side=tk.LEFT)
			self.input_button.pack(side=tk.RIGHT)
			self.root.mainloop()

		def sendMessages(self):
			MESSAGE = self.input_text.get()
			self.input_text.delete(0, tk.END)
			self.text_output.insert(tk.INSERT, "You: "+MESSAGE)
			self.text_output.insert(tk.INSERT, '\n')
			s.send(MESSAGE)

		def processData(self):
			try:
				data = self.queue.get(0)
				self.text_output.insert(tk.INSERT, data)
				self.root.after(1000, self.processData)
			except Queue.Empty:
				self.root.after(1000, self.processData)

		def Disconnect(self):
			MESSAGE = "Disconnecting from "+SERVER_IP
			s.send(MESSAGE)
			self.text_output.insert(tk.INSERT, "Disconnected")
			self.root.destroy()

	class threadReceive(threading.Thread):
		def __init__(self, queue):
			threading.Thread.__init__(self)
			self.queue = queue

		def run(self):
			data = s.recv(BUFFER_SIZE)
			self.queue.put(data)
			threading.Timer(.01, self.run).start()

	application = clientApp()
	s.close()

elif connection_choice == "udp":
	SERVER_IP = server_ip
	UDP_PORT = 5000
	MESSAGE = "HELLO, "+SERVER_IP
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.sendto(MESSAGE, (SERVER_IP, UDP_PORT))
	except:
		print 'Failed to create socket'
		sys.exit()

	class clientApp():
		def __init__(self):
			self.root = tk.Tk()
			self.queue = Queue.Queue()
			self.thread = threadReceive(self.queue)
			self.thread.daemon = True
			self.thread.start()
			self.root.after(100, self.processData)
			self.text_output = tk.Text(height=25, insertwidth=3)
			self.input_label = tk.Label(text="User input: ")
			self.input_text = tk.Entry(bd=3, width=30)
			self.input_button = tk.Button(text="Enter", command=self.sendMessages)
			self.dis_button = tk.Button(text="Disconnect", command=self.Disconnect)
			self.dis_button.pack(side=tk.BOTTOM)
			self.input_button.config(relief = tk.SUNKEN)
			self.text_output.pack(side=tk.TOP)
			self.input_label.pack(side = tk.LEFT)
			self.input_text.pack(side=tk.LEFT)
			self.input_button.pack(side=tk.RIGHT)
			self.root.mainloop()

		def sendMessages(self):
			MESSAGE = self.input_text.get()
			self.input_text.delete(0, tk.END)
			self.text_output.insert(tk.INSERT, "You: "+MESSAGE)
			self.text_output.insert(tk.INSERT, '\n')
			s.sendto(MESSAGE, (SERVER_IP, UDP_PORT))

		def processData(self):
			try:
				data = self.queue.get(0)
				self.text_output.insert(tk.INSERT, data)
				self.root.after(1000, self.processData)
			except Queue.Empty:
				self.root.after(1000, self.processData)

		def Disconnect(self):
			MESSAGE = "Disconnecting from "+SERVER_IP
			s.sendto(MESSAGE, (SERVER_IP, UDP_PORT))
			self.text_output.insert(tk.INSERT, "Disconnected")
			self.root.destroy()

	class threadReceive(threading.Thread):
		def __init__(self, queue):
			threading.Thread.__init__(self)
			self.queue = queue

		def run(self):
			data, addr = s.recvfrom(1024)
			self.queue.put(data)
			threading.Timer(.01, self.run).start()

	application = clientApp()
	s.close()

else:
	print "Must input either TCP or UDP"
	execfile("client.py")
