import socket

class Func:
    pass
  




class ConnectionHelper:
    
    def __init__(self, server):
        self.server = server
        self.host = socket.gethostname()
        self.port = 5000  # initiate port no above 1024
        if self.server:
            self.local_socket = socket.socket()  # get instance
            # look closely. The bind() function takes tuple as argument
            self.local_socket.bind((self.host, self.port))  # bind host address and port together

                # configure how many client the server can listen simultaneously
            self.local_socket.listen(2)
            self.conn, self.address = self.local_socket.accept()  # accept new connection
            #print("Connection from: " + str(address))
        if not self.server:
            self.local_socket = socket.socket()  # instantiate
            self.local_socket.connect((self.host, self.port))  # connect to the server
        self.message = "host"
        self.data = "client"
        


    def ConnectionProtocol(self, message):
        self.message = message
        if self.server:
            # receive data stream. it won't accept data packet greater than 1024 bytes
            self.data = self.conn.recv(1024).decode()
            if not self.data:
                # if data is not received break
                return False;
            #print("from connected user: " + str(data))
            self.conn.send(self.message.encode())  # send data to the client
        if not self.server:
            self.local_socket.send(self.message.encode())  # send message
            self.data = self.local_socket.recv(1024).decode()  # receive response

            #print('Received from server: ' + data)  # show in terminal

            #message = input(" -> ")  # again take input            
            return True
        

    def ParseData(self):
        #parse the data
        onlinex, onliney, onlineBulletX, onlineBulletY= self.data.split(' ')
        return  float(onlinex), float(onliney), float(onlineBulletX), float(onlineBulletY)