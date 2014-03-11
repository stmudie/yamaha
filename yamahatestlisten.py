import socket

IP = "localhost"
PORT = 50000

srvsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srvsock.bind((IP,PORT))
srvsock.listen(1)

conn, addr = srvsock.accept()
print "connected by:", addr

while 1:
    data = conn.recv(1024)
    if not data: break
    
conn.close()