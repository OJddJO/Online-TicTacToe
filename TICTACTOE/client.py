import socket
import pygame

class Network:

    def __init__(self):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.server = str(input('Server Address : '))
        if self.server == '':
            self.server = "127.0.0.1:5757"
        self.ip = str(self.server.split(":")[0])
        self.port = int(self.server.split(":")[1])
        print(self.ip, "/", self.port)
        self.addr = (self.ip, self.port)

        self.player = self.connect()


    def connect(self):
        try:
            self.client.connect(self.addr)
            print("Connected !")
            return self.client.recv(2048).decode()
        except:
            pass


    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)




class Cursor:
    def __init__(self, screen):
        self.x = 1
        self.y = 1
        self.width = 99
        self.height = 99
        self.surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.color = pygame.Color(150, 150, 150, 50)
        self.screen = screen

    def draw(self):
        self.rect = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.surface, self.color, self.rect)
        self.screen.blit(self.surface, self.rect)

    def update(self, pos):
        self.x = 100*pos[0]+1
        self.y = 100*pos[1]+1
        self.draw()




class Game:

    def __init__(self):

        pygame.font.init()
        self.font = pygame.font.SysFont('arial', 20)

        self.n = Network()
        self.playerNB = self.n.player
        self.playerTurn = '1'

        self.grid = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        self.clicked = [-1, -1]

        self.win = ''
        
        self.screen = pygame.display.set_mode((300, 400), pygame.SRCALPHA)
        pygame.display.set_caption("TicTacToe")

        self.cursor = Cursor(self.screen)


    def msg(self):
        txt = ''
        if self.playerNB == '1' or self.playerNB == '2':
            if self.win == '':
                if self.playerTurn == self.playerNB:
                    txt = "Your Turn"
                else:
                    txt = "Your Opponent Turn"
            elif self.win == 't':
                txt = "Tie!"
            elif self.win == self.playerNB:
                txt = "You won the game, GG!"
            else:
                txt = "You lost..."
        else:
            txt = "Spectating"

        text = self.font.render(txt, False, (255, 255, 255), (0, 0, 0))
        self.screen.blit(text, (150-(10*len(txt)/2), 350))


    def render(self):

        self.screen.fill((0, 0, 0))
        
        for x in range(1, 3):
            pygame.draw.line(self.screen, (255, 255, 255), (0, 100*x), (300, 100*x))
        for y in range(1, 3):
            pygame.draw.line(self.screen, (255, 255, 255), (100*y, 0), (100*y, 300))

        for row in range(0, 3):
            for column in range(0, 3):
                pos = [row, column]
                element = self.grid[row][column]

                if element == '':
                    None
                elif element == '1':
                    pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(100*pos[0]+25, 100*pos[1]+25, 50, 50))
                elif element == '2':
                    pygame.draw.circle(self.screen, (255, 255, 255), (100*pos[0]+50, 100*pos[1]+50), 25)


    def input(self):
        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0]<=100:
            mouseX = 0
        elif mouse_pos[0]<=200:
            mouseX = 1
        else:
            mouseX = 2

        if mouse_pos[1]<=100:
            mouseY = 0
        elif mouse_pos[1]<=200:
            mouseY = 1
        else:
            mouseY = 2

        self.clicked = [-1, -1]
        if self.grid[mouseX][mouseY] == '':
            self.cursor.update([mouseX, mouseY])
            if pygame.mouse.get_pressed()[0]:
                self.clicked = [int(mouseX), int(mouseY)]


    def getData(self, data):
        tmp = eval(data)
        self.playerTurn = tmp[0]
        self.grid = tmp[1]
        self.win = tmp[2]


    def makeData(self):
        data = str([self.clicked, self.playerNB])
        return data

    
    def run(self):

        clock = pygame.time.Clock()
        run = True

        while run:

            self.render()

            if self.playerTurn == self.playerNB:
                self.input()
                self.cursor.draw()

            self.msg()
            pygame.display.update()

            self.getData(self.n.send(self.makeData()))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            clock.tick(30)
        
        print(self.grid)
        pygame.quit


game = Game()
game.run()
