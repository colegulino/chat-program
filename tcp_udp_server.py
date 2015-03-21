#!/usr/bin/env python

import socket
import sys
import threading
from SocketServer import ThreadingMixIn
import Queue
import struct

UDP = "UDP"
TCP = "TCP"
BUFFER_SIZE = 1024 # Normally 1024, but we want fast response
threads = []


class ClientThread(threading.Thread):

    def __init__(self,ip,port,conn, queue):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.conn = conn
        self.queue = queue
        print "[+] New thread started for "+ip+":"+str(port)

    def run(self):
        while True:
            data = self.conn.recv(4096)
            if not data: break
            print self.ip,": ", data
            self.queue.put(self.conn)
            self.queue.put(self.ip+": "+data)


class threadSend(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        try:
            sent_conn = self.queue.get(0)
            data = self.queue.get(0)
            for thread in threads:
                if sent_conn != thread.conn:
                    thread.conn.send(data+'\n')
            del data
            threading.Timer(.01, self.run).start()  
        except Queue.Empty:
            threading.Timer(.01, self.run).start()  

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("gmail.com",80))
print("Server IP Address: " + s.getsockname()[0])
ip = s.getsockname()[0]
s.close()

connection_type = raw_input("Please state whether you want to connect UDP or TCP: ")
connection_type = connection_type.upper()
if connection_type == TCP:

	TCP_IP = ip 
	TCP_PORT = 62

	tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	tcpsock.bind((TCP_IP, TCP_PORT))


	messagesQueue = Queue.Queue()
	sendThread = threadSend(messagesQueue)
	sendThread.start()
	sendThread.join()

	while True:
    		tcpsock.listen(10)
    		print "Waiting for incoming connections..."
    		(conn, (ip,port)) = tcpsock.accept()
    		newthread = ClientThread(ip,port,conn,messagesQueue)
    		newthread.daemon = True
    		newthread.start()
    		threads.append(newthread)


	for t in threads:
    		t.join()

elif connection_type == UDP:

    HOST = ip
    PORT = 5000

    # Datagram (udp) socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print 'Socket created'
    except socket.error, msg:
        print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    #Bind socket to local host and port
    try: 
        s.bind((HOST, PORT))
    except socket.error , msg:
        print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]

    print 'Socket bind complete'

    addresses = []
    while 1:
        # receive data from client (data, addr)
        d = s.recvfrom(1024)
        data = d[0]
        addr = d[1]

        if not data:
            break

        if addr not in addresses:
            addresses.append(addr)


        reply = addr[0] +": " + data + '\n'

        for address in addresses:
            if address != addr:
                s.sendto(reply, address)

        print 'Message[' + addr[0] + ':' + str(data)

    s.close()


else:
    print "Must input UDP or TCP"
    execfile("server.py")


