#You need a way to talk over the network. 
# Python gives you this via the socket module. 
# You need to decide two things:
#Address family: are we using IPv4? → AF_INET or AF_INET6 (IPv6)
#Socket type: do we want a reliable, 
# ordered connection (like a phone call) or fire-and-forget packets? → 
# SOCK_STREAM = TCP (reliable) OR SOCK_DGRAM = UDP (unreliable)
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#A socket needs to know where to listen — which IP and which port.
#localhost = '127.0.0.1'  your own machine
server.bind(('localhost', 8080))

#This tells the OS "start queuing incoming connection 
# attempts on this socket." 
# The 1 is how many pending connections can queue up before 
# you handle them.
server.listen(1)

#A server doesn't handle one request and quit — 
# it waits for the next one, forever.
# accept() blocks (pauses your program) 
# until someone actually connects. When they do, it gives you back:
# conn — a new socket just for talking to that one client
# addr — their IP/port
while True:
    conn, addr = server.accept()