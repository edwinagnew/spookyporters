import pygame
import pygame_textinput
import time
import random
from microqiskit import QuantumCircuit, simulate
import numpy as np
import math

black = (0, 0, 0)
background = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
dark_green = (0, 255, 0)
dark_red = (255, 0, 0)
background = (173,216,230)

n = 0
qlist = []
aliceBases = []
bobBases = []
bobBits = []
aliceBits = []
key = []

clicked = 0


pygame.init()
textinput = pygame_textinput.TextInput()
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Quantum Communication')
pygame.display.set_icon(pygame.image.load('icon.png'))
clock = pygame.time.Clock()

x0 = pygame.image.load('0x.png')
x1 = pygame.image.load('1x.png')
z1 = pygame.image.load('1z.png')
z0 = pygame.image.load('0z.png')
axisx = pygame.image.load('x.png')
axisz = pygame.image.load('y.png')
P = pygame.image.load('Capture.PNG')


def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def button(text, x, y, w, h, dark, light, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, light, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, dark, (x, y, w, h))

    smallText = pygame.font.SysFont("comicsansms", 20)
    textSurf, textRect = text_objects(text, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)

def createTextLeft(x, y, text, fontsize):
    smallText = pygame.font.SysFont("comicsansms", fontsize)
    textSurf, textRect = text_objects(text, smallText)
    textRect.midleft = (x, y)
    gameDisplay.blit(textSurf, textRect)

def createTextCenter(x, y, text, fontsize):
    smallText = pygame.font.SysFont("comicsansms", fontsize)
    textSurf, textRect = text_objects(text, smallText)
    textRect.center = (x, y)
    gameDisplay.blit(textSurf, textRect)

def Qubit():
    global qlist, aliceBases, aliceBits
    qlist = []
    aliceBases = []
    aliceBits = []


    if textinput.get_text() != "":
        n = int(textinput.get_text())

        for i in range(n):
            qc = QuantumCircuit(1, 1)
            bit = random.choice("01")
            base = random.choice("zx")
            qlist.append(bit + base)
            aliceBases.append(base)
            aliceBits.append(bit)

def randomBase():
    global bobBases, bobBits, aliceBases, aliceBits
    bobBases = []
    bobBits = []

    if textinput.get_text() != "":
        n = int(textinput.get_text())

        for i in range(n):
            base = random.choice("zx")
            bobBases.append(base)
            if base == aliceBases[i]:

                bobBits.append(aliceBits[i])
            else:
                bobBits.append("-")

def quitgame():
    pygame.quit()
    quit()

def compare():
    global key
    key = []
    for i,x in zip(aliceBits,bobBits):
        if i == x:
            key.append(i)

#Schemes
def game_intro():
    global n,qlist,aliceBits,aliceBases,bobBits,bobBases,key, clicked

    #reset to default for play again
    n = 0
    qlist = []
    aliceBases = []
    bobBases = []
    bobBits = []
    aliceBits = []
    key = []
    textinput.clear_text()
    clicked = 0

    #start
    intro = True

    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(background)

        createTextCenter((display_width / 2), (display_height / 3), "Quantum Communication", 40)
        createTextCenter((display_width / 2), (display_height / 2), "A game to simulate the Quantum Communication process", 20)

        mouse = pygame.mouse.get_pos()
        button("Start", 150, 450, 100, 50, dark_green, green, tutorial)
        button("Quit", 550, 450, 100, 50, dark_red, red, quitgame)

        pygame.display.update()
        clock.tick(15)

def tutorial():
    tutorial = False
    while not tutorial:
        events = pygame.event.get()
        for event in events:
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(background)

        createTextCenter((display_width / 2), (display_height / 4),
                         "In Quantum Communication, one way to encrypy the message", 20)
        createTextCenter((display_width / 2), (display_height / 4 + 30),
                         "is to use the method called Quantum Key Distribution.", 20)

        createTextCenter((display_width / 2), (display_height / 4 + 80),
                       "It's not using Qubits to carry messages but is using Qubits to", 20)
        createTextCenter((display_width / 2), (display_height / 4 + 110),
                         "generate a unique key for the message that known only to", 20)
        createTextCenter((display_width / 2), (display_height / 4 + 140),
                         "the sender and receiver.", 20)

        createTextCenter((display_width / 2), (display_height / 4 + 190),
                         "In this game, We are going to simulate the process of", 20)
        createTextCenter((display_width / 2), (display_height / 4 + 220),
                         "generating a random secret key shared between the sender", 20)
        createTextCenter((display_width / 2), (display_height / 4 + 250),
                         "and receiver by using BB84 protocol.", 20)

        button("Continue!", 250, 480, 300, 50, dark_green, green, game_Sender)
        pygame.display.update()
        clock.tick(15)

def showImg(x, y, img):
    gameDisplay.blit(img, (x,y))


def game_Sender():
    sender = False

    while not sender:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(background)

        createTextCenter((display_width / 2), (display_height / 20), "Message Sender", 40)
        showImg(10, 10, P)

        createTextCenter(display_width / 2, 120, "Please choose the number of Qubits you want to send to generate the key:", 20)

        textinput.update(events)
        pygame.draw.rect(gameDisplay, pygame.Color("white"), (display_width / 2-50, 145, 120, 40))
        gameDisplay.blit(textinput.get_surface(), (display_width / 2, 150))

        button("OK", 600, 150, 30, 30, green, dark_green, Qubit)

        createTextLeft(50, 220, "Random qubits in Random bases are:", 20)
        #createTextCenter((display_width / 2), 250, str(qlist), 20)
        #showImg((display_width / 2 + 30), 270, x0)
        i = 0
        while i < len(qlist):
            if qlist[i] == '1x':
                showImg((100 + i*40), 270, x1)
                showImg((100 + i * 40), 350, axisx)
            elif qlist[i] == '0x':
                showImg((100 + i*40), 270, x0)
                showImg((100 + i * 40), 350, axisx)
            elif qlist[i] == '1z':
                showImg((100 + i*40), 270, z1)
                showImg((100 + i * 40), 350, axisz)
            else:
                showImg((100 + i*40), 270, z0)
                showImg((100 + i * 40), 350, axisz)
            i = i + 1

        createTextLeft(50, 320, "Bases are:", 20)
        #createTextCenter((display_width / 2), 350, str(aliceBases), 20)
        createTextLeft(50, 420, "Bit Sequence is:",20)
        createTextCenter((display_width / 2), 450, str(aliceBits), 20)

        if qlist != []:
            button("Send", 600, 500, 100, 50, dark_green, green, receiver)

        pygame.display.update()
        clock.tick(15)

def receiver():
    receiver = False

    while not receiver:
        events = pygame.event.get()
        for event in events:
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(background)

        createTextCenter((display_width / 2), (display_height / 20), "Message Receiver", 40)
        showImg(10, 10, P)

        createTextCenter(display_width / 2, 170, "The qubits received are:", 20)
        i = 0
        while i < len(qlist):
            if qlist[i] == '1x':
                showImg((100 + i * 40), 200, x1)
            elif qlist[i] == '0x':
                showImg((100 + i * 40), 200, x0)
            elif qlist[i] == '1z':
                showImg((100 + i * 40), 200, z1)
            else:
                showImg((100 + i * 40), 200, z0)
            i = i + 1
        #createTextCenter((display_width / 2), 200, str(qlist), 20)
        createTextCenter(display_width / 2, 300, "Please randomly select bases", 20)
        button("Random!", 650, 300, 100, 30, dark_green, green, randomBase)
        #createTextCenter((display_width / 2), 350, str(bobBases), 20)
        j = 0
        while j < len(bobBases):
            if bobBases[j] == 'x':
                showImg((100 + j * 40), 350, axisx)
            else:
                showImg((100 + j * 40), 350, axisz)
            j = j + 1
        #createTextLeft(20, 320, "Your Bit Sequence is:",20)
        #createTextCenter((display_width / 2), 350, str(bobBits), 20)

        button("Send back Bases!", 250, 480, 300, 50, dark_green, green, generate)

        pygame.display.update()
        clock.tick(15)

def generate():
    global clicked
    generate = False

    while not generate:
        events = pygame.event.get()
        for event in events:
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(background)

        createTextCenter((display_width / 2), (display_height / 20), "Key Comparing", 40)

        createTextCenter((display_width / 2), 120, "The Qubit Sequence is:", 20)
        #createTextCenter((display_width / 2), 150, str(qlist), 20)
        i = 0
        while i < len(qlist):
            if qlist[i] == '1x':
                showImg((100 + i * 40), 150, x1)
            elif qlist[i] == '0x':
                showImg((100 + i * 40), 150, x0)
            elif qlist[i] == '1z':
                showImg((100 + i * 40), 150, z1)
            else:
                showImg((100 + i * 40), 150, z0)
            i = i + 1
        createTextCenter((display_width / 2), 230, "The Base Sequence of Sender is:",20)
        #createTextCenter((display_width / 2), 230, str(aliceBases), 20)
        k = 0
        while k < len(aliceBases):
            if aliceBases[k] == 'x':
                showImg((100 + k * 40), 260, axisx)
            else:
                showImg((100 + k * 40), 260, axisz)
            k = k + 1

        createTextCenter((display_width / 2), 360, "The Base Sequence of Receiver is:", 20)
        #createTextCenter((display_width / 2), 330, str(bobBases), 20)
        j = 0
        while j < len(bobBases):
            if bobBases[j] == 'x':
                showImg((100 + j * 40), 390, axisx)
            else:
                showImg((100 + j * 40), 390, axisz)
            j = j + 1

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if 350 + 100 > mouse[0] > 350 and 470 + 30 > mouse[1] > 470:
            pygame.draw.rect(gameDisplay, green, (350, 470, 100, 30))

            if click[0] == 1:
                clicked = 1
        else:
            pygame.draw.rect(gameDisplay, dark_green, (350, 470, 100, 30))

        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = text_objects("Compare!", smallText)
        textRect.center = ((350 + (100 / 2)), (470 + (30 / 2)))
        gameDisplay.blit(textSurf, textRect)

        if clicked:
            createTextCenter((display_width / 2), 300, str(aliceBits), 20)
            createTextCenter((display_width / 2), 430, str(bobBits), 20)
            button("Generate Private Key!", 250, 520, 300, 50, dark_green, green, final)

        pygame.display.update()
        clock.tick(15)

def final():
    final = False

    while not final:
        events = pygame.event.get()
        for event in events:
            # print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(background)
        compare()
        createTextCenter((display_width / 2), (display_height / 20), "Shared Secret Key", 40)
        createTextCenter((display_width / 2), (display_height / 3 ), "Bingo!", 20)
        createTextCenter((display_width / 2), (display_height / 3 + 30), "The private key for this message is:", 20)
        createTextCenter((display_width / 2), (display_height / 3 + 60), str(key), 20)
        button("Play Again!", 250, (display_height / 3 + 150), 300, 50, dark_green, green, game_intro)

        pygame.display.update()
        clock.tick(15)

def sender_help():
    pass


game_intro()
