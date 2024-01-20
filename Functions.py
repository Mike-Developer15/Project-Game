import pygame
import socket

class Func:
    pass
  


class Button:
    def __init__(self, color, highlight, x, y, width, height, text=''):
        self.color = color
        self.highlight = highlight
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def Draw(self, win, pos, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        if self.IsOver(pos):
            pygame.draw.rect(win, self.highlight, (self.x, self.y, self.width, self.height), 0)
        else:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 14)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def IsOver(self, pos):
        # Pos is the mouse position or a tuple of (x, y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

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