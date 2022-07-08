import socket
from _thread import *

class Server:

    def __init__(self):
        
        self.ip = str(input("Ip (default: 127.0.0.1): "))
        if self.ip == "":
            self.ip = "127.0.0.1"

        self.port = str(input("Port (default: 5757): "))
        if self.port == "":
            self.port = 5757
        self.port = int(self.port)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind((self.ip, self.port))
        except socket.error as e:
            print(e)

        self.server.listen(2)
        print(f"Server started at {self.ip}:{self.port}")

        self.playercount = 0
        self.grid = [
            ['', '', ''],
            ['', '', ''],
            ['', '', '']
        ]
        self.playerTurn = '1'
        self.win = ''


    def clientConn(self, conn, addr):
        self.playercount += 1
        playerNB = str(self.playercount)
        conn.send(str.encode(playerNB))
        reply = ""

        while True:
            try:
                recvData = conn.recv(2048).decode()
                if not recvData:
                    print("Client", addr, ": Disconnected")
                else:
                    
                    self.getData(recvData)
                    self.win = self.checkWin()
                    sendData = str(self.makeData(self.playerTurn, self.grid, self.win))
                    reply = str.encode(sendData)

                conn.sendall(reply)

            except:
                print("Lost Connection")
                break
        
        self.playercount -= 1


    def getData(self, data):
        if self.win == '':

            tmp = eval(data)

            if tmp[0] == [-1, -1]:
                pass

            else:

                playerNB = tmp[1]
                pos = tmp[0]
                if self.grid[pos[0]][pos[1]] == '':
                    self.grid[pos[0]][pos[1]] = playerNB
                    if self.playerTurn == '1':
                        self.playerTurn = '2'
                    elif self.playerTurn == '2':
                        self.playerTurn = '1'


    def makeData(self, playerTurn, grid, win):
        data = [playerTurn, grid, win]
        return data
        

    def checkWin(self):
        for player in range(1, 3):
            #check rows
            p = str(player)
            for r in range(3):
                win = p
                for c in range(3):
                    if self.grid[r][c] != p:
                        win = ''
                if win:
                    return win
            #check columns
            for c in range(3):
                win = p
                for r in range(3):
                    if self.grid[r][c] != p:
                        win = ''
                if win:
                    return win
            
            #check diagonals
            win = p
            for i in range(3):
                if self.grid[i][i] != p:
                    win = ''
            if win:
                return win
            
            win = p
            for i in range(3):
                if self.grid[i][2-i] != p:
                    win = ''
            if win:
                return win

        win = 't'
        for c in range(3):
            for r in range(3):
                if self.grid[c][r] == '':
                    win = ''
        if win:
            return win

        return ''


    def run(self):

        while True:
            #wait until a connection is etablished
            conn, addr = self.server.accept()
            print("Client Connected:", addr)

            if self.playercount == 0:
                self.grid = [
                    ['', '', ''],
                    ['', '', ''],
                    ['', '', '']
                ]
                self.playerTurn = '1'
                self.win = ''

            #start async connection for client
            start_new_thread(self.clientConn, (conn, addr))


server = Server()
server.run()