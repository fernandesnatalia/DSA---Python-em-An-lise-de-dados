#Interpretação pessoal do jogo Ping Pong

#importar interface e funções relacionadas ao tempo e randômicas
from tkinter import *
import random
import time

# Aceitar entrada de nível do jogo, escolha do usuário
level = int(input("Qual nível você gostaria de jogar? 1/2/3/4/5 \n"))

# Estabelecer o tamanho da barra de acordo com o nível de jogo, maior nível = menor barra
length = 500/level

# Criar objeto tk alinhado à janela
# Abrirá outra janela
root = Tk()

#Título
root.title("Ping Pong")

# Definir redimensionamento da janela
root.resizable(0, 0)

# Deixar a janela na frente das demais
root.wm_attributes("-topmost", -1)

# Definir as dimensões da interface com funcao canvas
canvas = Canvas(root, width=800, height=600, bd=0,highlightthickness=0)
canvas.pack()
root.update()

# Definir a manipulacao do jogo
count = 0
lost = False

# Declarar os atributos da classe pra movimentar bola
class Bola:
    def __init__(self, canvas, Barra, color):
        self.canvas = canvas
        self.Barra = Barra
        self.id = canvas.create_oval(0, 0, 15, 15, fill=color) #definir formato oval para a bolinha
        self.canvas.move(self.id, 245, 200) #definir movimento da bolinha

        # definir as posições de ínício para a bolinha
        starts_x = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts_x)

        #movimentação com coordenadas
        self.x = starts_x[0]
        self.y = -3

        #altura e largura
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()

    #Declarar imagem da classe bola
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)

        pos = self.canvas.coords(self.id)

        if pos[1] <= 0:
            self.y = 3

        if pos[3] >= self.canvas_height:
            self.y = -3

        if pos[0] <= 0:
            self.x = 3
            
        if pos[2] >= self.canvas_width:
            self.x = -3

        self.Barra_pos = self.canvas.coords(self.Barra.id)

        #condição para pontuação da partida
        if pos[2] >= self.Barra_pos[0] and pos[0] <= self.Barra_pos[2]:
            if pos[3] >= self.Barra_pos[1] and pos[3] <= self.Barra_pos[3]:
                self.y = -3
                global count
                count +=1
                score()

        #condição para perda da partida
        if pos[3] <= self.canvas_height:
            self.canvas.after(10, self.draw)
        else:
            game_over()
            global lost
            lost = True

# Declarar os atributos da classe pra movimentar barra
class Barra:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, length, 10, fill=color) #definir formato da barra
        self.canvas.move(self.id, 200, 400) #definir movimentação da barra

        # definir a posição de ínício para a barra
        self.x = 0

        self.canvas_width = self.canvas.winfo_width()

        # Declarar movimentação da barra com as setas
        self.canvas.bind_all("<KeyPress-Left>", self.move_left)
        self.canvas.bind_all("<KeyPress-Right>", self.move_right)

    #Declarar imagem da classe barra
    def draw(self):
        self.canvas.move(self.id, self.x, 0)

        self.pos = self.canvas.coords(self.id)

        if self.pos[0] <= 0:
            self.x = 0
        
        if self.pos[2] >= self.canvas_width:
            self.x = 0
        
        global lost
        
        if lost == False:
            self.canvas.after(10, self.draw)

    def move_left(self, event):
        if self.pos[0] >= 0:
            self.x = -3

    def move_right(self, event):
        if self.pos[2] <= self.canvas_width:
            self.x = 3


# Definir como iniciar a partida
def start_game(event):
    global lost, count
    lost = False
    count = 0
    score()
    canvas.itemconfig(game, text=" ")

    time.sleep(1)  #tempo para iniciar novamente a partida
    Barra.draw()  #aparecer bolinha e barra
    Bola.draw()

# Declarar mensagem para printar pontuacao
def score():
    canvas.itemconfig(score_now, text="Pontos: " + str(count))

# Declarar a mensagem em perda do jogo
def game_over():
    canvas.itemconfig(game, text="Game over!")

# Definir cores dos objetos
Barra = Barra(canvas, "orange")
Bola = Bola(canvas, Barra, "purple")

# Declarar atualização da pontuação
score_now = canvas.create_text(430, 20, text="Pontos: " + str(count), fill = "green", font=("Arial", 16))

# Declarar estética do texto de game over
game = canvas.create_text(400, 300, text=" ", fill="red", font=("Arial", 40))

# Declarar botão para iniciar novamente
canvas.bind_all("<Button-1>", start_game)

#repetição do jogo
root.mainloop()