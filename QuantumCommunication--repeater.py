import pygame
import pygame_textinput
import time
import random
import qkd
import numpy as np
import math
import binascii

import pop_up
pop_up.popUpWindow("warning", "if this isnt here everything crashes")

#import TextBox
#Colors
background = (173,216,230)
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,200)
dark_green = (0,255,0)
dark_red = (255,0,0)
grey = (220,220,220)
purple = (128,0,128)
light_red = (255, 102, 102)
yellow = (255,255,0)

#QC initials
nt = 0
qlist = []
aliceBases = []
bobBases = []
bobBits = []
aliceBits = []
key = []

clicked = 0


x0 = pygame.image.load('imgs/0x.png')
x1 = pygame.image.load('imgs/1x.png')
z1 = pygame.image.load('imgs/1z.png')
z0 = pygame.image.load('imgs/0z.png')
axisx = pygame.image.load('imgs/x.png')
axisz = pygame.image.load('imgs/y.png')
P = pygame.image.load('imgs/Capture.PNG')
tip = pygame.image.load('imgs/tooltip.png')


#repeater initials
computers = {}
repeaters = {}

connections = {}

sent_messages = {}

n = ""
msg = ""

LOSS = 0.10

#Game Initials
pygame.init()
textinput = pygame_textinput.TextInput()
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Quantum Communication')
pygame.display.set_icon(pygame.image.load('imgs/icon.png'))
clock = pygame.time.Clock()

####################### repeaters #####################
def text_objects(text, font, colour=black):
	textSurface = font.render(text, True, colour)
	return textSurface, textSurface.get_rect()

def clearUI():
  gameDisplay.fill(background, (0, display_height*2/3 + 50, display_width, display_height))
  help_button = button("?", display_width-100, display_height*2/3 + 50, 50, 50, background, grey, action=show_help, text_size=30)

def show_help():
    pop_up.popUpWindow('Help?', 'In this level you must first create a secure connection between yourself and Bob.\n Since the distance is too great for a qubit to be sent without loss, you must set up a chain of repeaters which take in a qubit, and output it with greater signal.\n\nOnce a repeater has been placed, the bb84 protocol which you saw in the introduction is run, with green lines representing the successfully transmitted qubits and the red lines representing the lost ones. \nRemember that the further apart your repeaters are, the greater the loss.\n\nOnce you have a complete chain of repeaters, you will be able to send messages completely securely across any number of repeaters, only needing faith in the laws of quantum mechanics to trust its security.')



def show_message(message):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()

        gameDisplay.fill(background)

        close = button("X", display_width - 40, 20, 20, 20, dark_red, red, action=main_loop)

        smallText = pygame.font.Font("freesansbold.ttf", 12)
        textSurf, textRect = text_objects(message, smallText)
        textRect.center = ((display_width / 2), (display_height / 3))
        gameDisplay.blit(textSurf, textRect)

        pygame.display.update()
        clock.tick(15)

def show_tutorial():
    show_message("In this level you will learn about chaining quantum repeaters to create a secure connection between any user. Qubits can be sent over lossy channels to create private keys. Your first step will be to create a network of repeaters.")


def draw_grid(top_left=(0, 0), width=display_width, height=int(display_height * 2 / 3)):  # 0 gamewidth 2/3 gamewidth
    #gameDisplay.fill(background)

    # print(top_left, width, height)
    # print(repeaters)
    blockSize = 50  # Set the size of the grid block
    for x in range(height):
        for y in range(width):
            if x * blockSize <= width and y * blockSize <= height:
                rect = pygame.Rect(top_left[0] + x * blockSize, top_left[1] + y * blockSize,
                                   blockSize, blockSize)
                if rect.topleft in repeaters and rect.topleft not in computers:
                    # print(rect.topleft , "in repeaters")
                    pygame.draw.rect(gameDisplay, repeaters[rect.topleft], rect, 0)  # 0 fill
                else:
                    pygame.draw.rect(gameDisplay, grey, rect, 1)  # 1 dont fill


def draw_connections():
    for key in connections:
        a = int(connections[key][0][0]), int(connections[key][0][1] + 50 / 2)
        b = int(connections[key][1][0]), int(connections[key][1][1] + 50 / 2)
        pygame.draw.line(gameDisplay, green, a, b, 5)
        text = "key: (secret)"
        if connections[key][0] in computers and a[0] < display_width / 2 or connections[key][1] in computers and b[
            0] < display_width / 2:  # is you
            text = "key: " + str(key)

        smallText = pygame.font.Font("freesansbold.ttf", 12)
        textSurf, textRect = text_objects(text, smallText, colour=blue)
        textRect.center = (a[0] / 2 + b[0] / 2, a[1] / 2 + b[1] / 2 + 25)
        gameDisplay.blit(textSurf, textRect)


def main_loop():
    textinput.clear_text()
    qubits = 0
    intro = True



    while intro:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                quitgame()
        gameDisplay.fill(white)
        clearUI()
        draw_grid((0, 0), display_width, int(display_height * 2 / 3))
        draw_connections()

        h, w = (100, 100)
        a_c = pygame.Rect((50, int(display_height / 3 - h / 2)), (w, h))
        pygame.draw.rect(gameDisplay, blue, a_c)
        for d1 in [0, 50]:
            for d2 in [0, 50]:
                computers[a_c.left + d1, a_c.top + d2] = blue

        smallText = pygame.font.Font("freesansbold.ttf", 12)
        textSurf, textRect = text_objects("Your computer", smallText, colour=blue)
        textRect.center = (100, 0)
        textRect.top = a_c.bottom + 10
        gameDisplay.blit(textSurf, textRect)

        b_c = pygame.Rect((display_width - w - 50, int(display_height / 3 - h / 2)), (w, h))
        pygame.draw.rect(gameDisplay, purple, b_c)
        for d1 in [0, 50]:
            for d2 in [0, 50]:
                computers[b_c.left + d1, b_c.top + d2] = purple

        textSurf, textRect = text_objects("Bob's computer", smallText, colour=purple)
        textRect.center = (display_width - 100, 0)
        textRect.top = b_c.bottom + 10
        gameDisplay.blit(textSurf, textRect)

        add_button = button("add repeater", 50, 480, 150, 50, green, dark_green, action=add)
        hover(50, 530, "Use this button to add a repeater to your network. Since",  "cloning a quantum state is impossible, a quantum repeater", "works by purifying and switching entaglements")


        if complete_path():
            send_button = button("send message", 250, 480, 150, 50, green, dark_green, action=send)
            hover(250, 530, "Use this button to send a classical string to Bob. This could either be done",  "by encoding the message onto a qubit and sending it to him through the network or by distributing", " entangled qubits through the network and teleporting the string")

        if len(sent_messages) > 0:
            next_button = button("what's next?", 450, 480, 150, 50, blue, purple, action=show_future)

        pygame.display.update()
        clock.tick(15)

def show_future():
    pop_up.popUpWindow("future levels", "In the future, as qubit loss decreases and error correction improves, more complicated networks may be simulated in this game. \nOnce qubits can sent deterministically, people may securely send large amounts of data to be computed else and returned to be measured.\n Eventually a quantum internet may be built which promises to revolutionize the spread of information on a scale akin to the development of the classical internet.")

def add():
    pygame.mouse.set_cursor(*pygame.cursors.tri_left)
    from_grid = choice_selection("Where do you want the connection to come from",
                                 (display_width * 2 / 3, display_height * 5 / 6))
    hover(display_width*2/3, display_height * 5/6, "You must choose an existing repeater or the",  "bottom right of your computer")

    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
    nearest_grid = choice_selection("Choose a grid to place your new connection",
                                    (display_width * 2 / 3, display_height * 5 / 6), measure_distance_from=from_grid, is_repeater=False)

    # smallText = pygame.font.Font("freesansbold.ttf", 12)
    # textSurf, textRect = text_objects("Choose a grid to place your new repeater", smallText)
    # textRect.center = (display_width*2/3, display_height*5/6)
    # gameDisplay.blit(textSurf, textRect)

    pygame.mouse.set_cursor(*pygame.cursors.arrow)
    pygame.display.update()

    create_key(from_grid, nearest_grid)

    # main_loop()


def send():
    i = 0
    global msg
    textinput.clear_text()
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quitgame()
        clearUI()


        smallText = pygame.font.Font("freesansbold.ttf", 16)
        textSurf, textRect = text_objects("What message would you like to send to Bob?", smallText)
        textRect.center = (display_width * 1 / 2, display_height * 4.5 / 6 + 25)
        gameDisplay.blit(textSurf, textRect)

        textinput.update(events)
        gameDisplay.blit(textinput.get_surface(), (textRect.left, 500))

        add_button = button("OK", display_width/2, 525, 50, 50, green, dark_green, action=update_msg)

        if len(msg) > 0:
            clearUI()
            createTextCenter(display_width*1/2, display_height*5/6, "Encoding '" + msg + "' ...", 24)

            binary_msg = ' '.join(format(ord(x), 'b') for x in msg)
            createTextCenter(display_width*1/2, display_height*5/6 + 25, binary_msg[:i], 16)
            i += 1
            if i == len(binary_msg): break

        pygame.display.update()
        clock.tick(15)

    pygame.time.wait(1000)
    update_msg(val="")
    send_to_bob(binary_msg.split())


def send_to_bob(message):
    clearUI()
    a=(100, 200) 
    b=(650, 200)
    path = get_path(a,b)
    print("path: ", path)

    createTextLeft(0, display_height*4.5/6 + 10, "Message: '" + " ".join(message) + "'             (=" + "".join([chr(int(x,2)) for x in message]) + ")", 20)

    createTextLeft(0, display_height*5/6, "Sending: ", 18)

    createTextLeft(0, display_height*5.5/6, "Status: ", 18) 

    for j, letter in enumerate(message):
        #col = random.choice([green, purple, yellow, blue, ])
        col = [random.random() * 255, random.random() * 150, random.random() * 255]
        while sum([abs(background[k] - col[k]) for k in range(3)]) < 30: 
            col = [random.random() * 255, random.random() * 150, random.random() * 255]

        createTextLeft(55 + j * 50, display_height*5/6, letter, 16, colour=col)
        #createTextLeft(55 + j * 50, display_height*5.5/6, "success", 16, colour=green)
        for i in range(len(path)-1):
            a = path[i][0] + 50, path[i][1] + 20
            b = path[i+1][0], path[i][1] + 20
            loss = LOSS * get_dist(a, b)
            red = int(loss * len(letter) + random.random())
            draw_lines(red, len(letter)-red, a, b, block_size=10, green_col=col)

            pygame.time.wait(500)
        createTextLeft(55 + j * 50, display_height*5.5/6, "success", 16, colour=green)
    pygame.display.update()
    pygame.time.wait(1000)
    pop_up.popUpWindow("Success", "You successfully sent the message '" + "".join([chr(int(x,2)) for x in message]) + "' to Bob")
    
    sent_messages[("a","b")] = message
        #print("here", j==len(message) -1 and 1/0)

    main_loop()
        


def get_path(a, b):
    if a == b: return [a]
    path = [a]
    for key in connections:
        if connections[key][0] == path[-1]: return path + get_path(connections[key][1], b)
        if path[-1] == b: return path


def get_message():
    global msg
    msg = textinput.get_text()


def choice_selection(message, position, is_repeater=True, measure_distance_from=None):
    clearUI()
    smallText = pygame.font.Font("freesansbold.ttf", 12)
    textSurf, textRect = text_objects(message, smallText)
    textRect.center = position
    gameDisplay.blit(textSurf, textRect)
 
    remove_next = None
 
    while True:
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.QUIT:
                quitgame()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if pos[1] < display_height * 2 / 3:
                    grid_block = (pos[0] - (pos[0] % 50), pos[1] - (pos[1] % 50))
                    if is_repeater:
                       
                        #Make sure the first link is in a computer
                        if len(repeaters) == 0 and grid_block not in computers:
                            createTextLeft(display_width * 2 / 3, display_height * 5.5 / 6, "The first repeater must be in the computer", 16, colour=red)
                            print("The fist repeater must be in the computer")
                            continue
                           
                        else:
 
                        #Make sure that you don't click the same grid as another repeater
                            if len(repeaters)%2 == 0 and len(repeaters) != 0 and grid_block not in repeaters:
                                createTextLeft(display_width * 2/3, display_height*5.5/6, "The link must start in an existing repeater", 16, colour=red)
                                print("The link must start in an existing repeater")
                                continue
 
                            elif grid_block in repeaters:
                                # del repeaters[grid_block]
                                print("TODO: implement deletion")
                           
                            #Adds the repeater to the list
                            else:
                                if measure_distance_from and qkd.calc_loss(LOSS, get_dist(grid_block,
                                                                                        measure_distance_from)) == 1:
                                    smallText = pygame.font.Font("freesansbold.ttf", 12)
                                    textSurf, textRect = text_objects("Range is too great, try again", smallText,
                                                                    colour=red)
                                    textRect.center = display_width * 2/3, display_height * 4.75 / 6
                                    gameDisplay.blit(textSurf, textRect)
                                    continue
                                else:
                                    repeaters[grid_block] = red
                                    draw_grid((0, 0), display_width, int(display_height * 2 / 3))
                    elif measure_distance_from and qkd.calc_loss(LOSS, get_dist(grid_block,
                                                                                        measure_distance_from)) == 1:
                                    smallText = pygame.font.Font("freesansbold.ttf", 12)
                                    textSurf, textRect = text_objects("Range is too great, try again", smallText,
                                                                    colour=red)
                                    textRect.center = display_width * 2 / 3, display_height * 4.75 / 6
                                    gameDisplay.blit(textSurf, textRect)
                                    continue
 
                    return grid_block
 
        if measure_distance_from:
            gameDisplay.fill(pygame.Color("white"), (position[0] - 100, position[1] + 25, 200, 50))
            pos = pygame.mouse.get_pos()
            nearest = (pos[0] - (pos[0] % 50), pos[1] - (pos[1] % 50))
            dist = get_dist(nearest, measure_distance_from)
            loss = qkd.calc_loss(LOSS, dist)
            label = "Distance: " + str(round(dist, 3)) + "=> loss: " + str(round(loss, 3))
            colour = [(1 - loss) * green[j] + loss * red[j] for j in range(3)]
            textSurf, textRect = text_objects(label, smallText, colour=colour)
            textRect.center = (position[0], position[1] + 50)
            gameDisplay.blit(textSurf, textRect)
 
            if remove_next and nearest != remove_next:  # and nearest not in repeaters and nearest not in computers and nearest[1] * 50 < display_height * 2/3:
                rect = pygame.Rect(remove_next[0], remove_next[1], 50, 50)
                pygame.draw.rect(gameDisplay, white, rect, 0)
                pygame.draw.rect(gameDisplay, grey, rect, 1)
                remove_next = None
 
            if nearest not in computers and nearest not in repeaters:
                rect = pygame.Rect(nearest[0], nearest[1], 50, 50)
                pygame.draw.rect(gameDisplay, light_red, rect, 0)
                remove_next = nearest
 
        pygame.display.update()
        clock.tick(30)


def create_key(a, b):
    t = 0
    run = True
    q = None
    while True:
        global n
        # print("n=", n)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quitgame()

        clearUI()
        smallText = pygame.font.Font("freesansbold.ttf", 16)
        textSurf, textRect = text_objects("How many qubits do you want to send to the repeater to create the key?",
                                          smallText)
        textRect.center = (display_width * 1 / 2, display_height * 4.5 / 6 + 25)
        gameDisplay.blit(textSurf, textRect)

        textinput.update(events)
        # gameDisplay.blit(textinput.get_surface(), (display_width*1/2, display_width * 10/12))
        gameDisplay.blit(textinput.get_surface(), (textRect.left, 500))

        add_button = button("OK", textRect.left + 50, 500, 50, 50, green, dark_green, action=update_n)

        try:
            n = int(n)

        except:
            if len(n) > 0:
                textSurf, textRect = text_objects("Invalid input", smallText, colour=red)
                textRect.center = (textRect.left + 50, display_height * 5.5 / 6)
                gameDisplay.blit(textSurf, textRect)

        if run and type(n) == int and n > 0:
            q = qkd.bb84(n, p=LOSS)
            dist = get_dist(a, b)
            q.run_protocol(dist)
            draw_lines(q.n_sent - q.n_received, q.n_received, (a[0] + 50, a[1]), b)

            draw_grid()
            t = time.time()


        if run and q and (not q.get_key() or q.get_key() == "error" or q.get_key() in connections):
            textSurf, textRect = text_objects("An empty or identical key has been generated, try sending more qubits",
                                              smallText, colour=red)
            textRect.topleft = (textRect.left + 150, display_height * 5.75 / 6)
            gameDisplay.blit(textSurf, textRect)
            update_n(val="")


        elif q:
            run = False
            createTextCenter(a[0], a[1] + 100, "My bases were: " + " ".join(q.alice_bases[:5]) + "..." * int(len(q.alice_bases) > 5), 15)

            if 0.9 < time.time() - t < 1:
                b_filt = [z for z in q.bob_bases if z != -1]
                createTextCenter(b[0], b[1] - 50, "My bases were: " + " ".join(b_filt[:5]) + "..." * int(len(b_filt) > 5), 15)
    

            if 3.9 < time.time() - t < 4:

                clearUI()

                print("great success")

                repeaters[b] = green
                connections[q.get_key()] = (a, b)
                if complete_path():
                    draw_grid()
                    pygame.display.update()

                    pop_up.popUpWindow("Path complete", "Congratulations! You have created a completely secure path between you and Bob, you may now send and encrypt messages to each other")
                n = ""
                main_loop()

        pygame.display.update()
        clock.tick(30)


def update_n(val=None):
    global n
    if type(val) == str:
        n = val
    else:
        n = textinput.get_text()

def update_msg(val=None):
    global msg
    if type(val) == str:
        msg = val
    else:
        msg = textinput.get_text()


def get_dist(p0, p1):
    return math.sqrt(((p0[0] - p1[0]) / 50) ** 2 + ((p0[1] - p1[1]) / 50) ** 2)
    # return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)


def complete_path(a=(100, 200), b=(650, 200)):
    if a == b: return True
    for key in connections:
        if connections[key] == (a, b): return True
        if connections[key][0] == a: return complete_path(a=connections[key][1], b=b)
    return False


def draw_lines(red_lines, green_lines, a, b, block_size=50, green_col=green):
    red_remaining = red_lines
    green_remaining = green_lines

    n_drawn = 0

    drawn_lines = {"red": [((0, 0), (0, 0))] * (red_lines + green_lines), "green": []}

    while red_remaining + green_remaining > 0 or max(drawn_lines["red"]) != ((0, 0), (0, 0)):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quitgame()

        gameDisplay.fill(pygame.Color("white"), (a[0], a[1], b[0] - a[0], b[1] - a[1] + block_size))
        if green_remaining > 0 and random.random() > red_remaining / green_remaining:
            # draw a green line
            sep = n_drawn / green_lines * block_size
            coords = ((a[0], a[1] + sep), (b[0], b[1] + sep))
            # pygame.draw.line(gameDisplay, green, (a[0], a[1] + sep), (b[0], b[1] + sep)))
            drawn_lines["green"].append(coords)
            n_drawn += 1
            green_remaining -= 1
        elif red_remaining > 0:
            sep1 = random.random() * block_size
            sep2 = random.random() * block_size
            coords = ((a[0], a[1] + sep1), (b[0], b[1] + sep2))
            drawn_lines["red"].insert(0, coords)
            red_remaining -= 1

        drawn_lines["red"].insert(0, ((0, 0), (0, 0)))

        drawn_lines["red"] = drawn_lines["red"][:red_lines + green_lines]

        # print("drawing ", len(drawn_lines["green"]), " green lines")
        if block_size == 100: 
            print(red_lines, green_lines)
            print(drawn_lines["red"])
        for fr, to in drawn_lines["green"]:
            pygame.draw.line(gameDisplay, green_col, fr, to, 2)
        for i, (fr, to) in enumerate(drawn_lines["red"]):
            if (fr, to) != (0, 0):
                c = (i + 1) / len(drawn_lines["red"]) * 255
                new_col = [min(j + c, 255) for j in red]
                # print("drawing red with colour", new_col)
                #pygame.draw.line(gameDisplay, red + (i / len(drawn_lines["red"]),), fr, to)
                pygame.draw.line(gameDisplay, new_col, fr, to)

        pygame.display.update()
        clock.tick(30)
####################### repeaters #####################

####################### QC #####################
def button(text, x, y, w, h, dark, light, action=None, text_size=20):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, light, (x, y, w, h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, dark, (x, y, w, h))

    smallText = pygame.font.SysFont("comicsansms", text_size)
    textSurf, textRect = text_objects(text, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    gameDisplay.blit(textSurf, textRect)


def hover(x, y, hover_text, line2='',line3=''):
    mouse = pygame.mouse.get_pos()
    showImg(x,y, tip)
    if x + 16 > mouse[0] > x and y + 16 > mouse[1] > y:
        createTextLeft(x + 20, y + 8, hover_text, 15)
        createTextLeft(x + 20, y + 23, line2, 15)
        createTextLeft(x + 20, y + 38, line3, 15)

def createTextLeft(x, y, text, fontsize, colour=black):
    smallText = pygame.font.SysFont("comicsansms", fontsize)
    textSurf, textRect = text_objects(text, smallText, colour=colour)
    textRect.midleft = (x, y)
    gameDisplay.blit(textSurf, textRect)

def createTextCenter(x, y, text, fontsize, colour=black):
    smallText = pygame.font.SysFont("comicsansms", fontsize)
    textSurf, textRect = text_objects(text, smallText, colour=colour)
    textRect.center = (x, y)
    gameDisplay.blit(textSurf, textRect)

def Qubit():
    global qlist, aliceBases, aliceBits
    qlist = []
    aliceBases = []
    aliceBits = []

    if textinput.get_text() != "":
        nt = int(textinput.get_text())

        for i in range(nt):
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
        nt = int(textinput.get_text())

        for i in range(nt):
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
    nt = 0
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

        createTextCenter((display_width / 2), (display_height / 7),
                         "In Quantum Communication, one way to encrypy the message", 20)
        createTextCenter((display_width / 2), (display_height / 7 + 30),
                         "is to use the method called Quantum Key Distribution.", 20)
        createTextCenter((display_width / 2), (display_height / 7 + 60),
                       "It's not using Qubits to carry messages but is using Qubits to", 20)
        createTextCenter((display_width / 2), (display_height / 7 + 90),
                         "generate a unique key for the message that known only to", 20)
        createTextCenter((display_width / 2), (display_height / 7 + 120),
                         "the sender and receiver.", 20)

        createTextCenter((display_width / 2), (display_height / 7 + 170),
                         "The method is very safe as Qubits will change their states after", 20)
        createTextCenter((display_width / 2), (display_height / 7 + 200),
                         "first observation. Thus, if hackers observed the Qubits before", 20)
        createTextCenter((display_width / 2), (display_height / 7 + 230),
                         "the receiver, the result will be different when users comparing", 20)
        createTextCenter((display_width / 2), (display_height / 7 + 260),
                         "the key sequence and users will know the key is not safe.", 20)

        createTextCenter((display_width / 2), (display_height / 7 + 310),
                         "In this game, We are going to simulate the process of generating", 20)
        createTextCenter((display_width / 2), (display_height / 7 + 340),
                         "a random secret key shared between the sender and receiver", 20)
        createTextCenter((display_width / 2), (display_height / 7 + 370),
                         "by using BB84 protocol(the first quantum cryptography protocol).", 20)

        button("Continue!", 250, 500, 300, 50, dark_green, green, game_Sender)
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
        hover(120, 60, "The sender is sending a random sequence of Qubits that based on Z or X axis", "each bit has a value of 0 or 1 for key generation")

        createTextCenter(display_width / 2, 120, "Please choose the number of Qubits you want to send to generate the key:", 20)

        textinput.update(events)
        pygame.draw.rect(gameDisplay, pygame.Color("white"), (display_width / 2-50, 145, 120, 40))
        gameDisplay.blit(textinput.get_surface(), (display_width / 2, 150))
        hover(display_width / 2 - 50, 185, "Please no more than 16!")

        button("OK", 600, 150, 30, 30, green, dark_green, Qubit)

        createTextLeft(50, 220, "Random qubits in Random bases are:", 20)

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
        createTextLeft(100, 450, str(aliceBits), 20)

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
        hover(120, 60, "After receiving the Qubits, the receiver will generate a sequence of random bases",
              "with the same amount of Qubits, and send the bases back to sender for key comparing")

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
        if bobBits != []:
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
        hover(270, 60, "The method will analyze the Qubits using both sequence of bases.",
              "If a bit is analyzed by a different base, the result will be an ",
              "uncertain value, which is represented by '-'")

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
        createTextCenter((display_width / 2), 200, "The Base Sequence of Sender is:",20)
        #createTextCenter((display_width / 2), 230, str(aliceBases), 20)
        k = 0
        while k < len(aliceBases):
            if aliceBases[k] == 'x':
                showImg((100 + k * 40), 230, axisx)
            else:
                showImg((100 + k * 40), 230, axisz)
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

        if 350 + 100 > mouse[0] > 350 and 300 + 30 > mouse[1] > 300:
            pygame.draw.rect(gameDisplay, green, (350, 300, 100, 30))

            if click[0] == 1:
                clicked = 1
        else:
            pygame.draw.rect(gameDisplay, dark_green, (350, 300, 100, 30))

        smallText = pygame.font.SysFont("comicsansms", 20)
        textSurf, textRect = text_objects("Compare!", smallText)
        textRect.center = ((350 + (100 / 2)), (300 + (30 / 2)))
        gameDisplay.blit(textSurf, textRect)

        hover(450, 310, "After comparing the result", "The uncertain values will be discarded", "and the remain values will be the key")

        if clicked:
            createTextLeft(100, 270, str(aliceBits), 20)
            createTextLeft(100, 430, str(bobBits), 20)
            button("Generate Private Key!", 250, 480, 300, 50, dark_green, green, final)

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
        if key != []:
            createTextCenter((display_width / 2), (display_height / 3 ), "Bingo!", 20)
            createTextCenter((display_width / 2), (display_height / 3 + 30), "The private key for this message is:", 20)
            createTextCenter((display_width / 2), (display_height / 3 + 60), str(key), 20)
        else:
            createTextCenter((display_width / 2), (display_height / 3), "Ops, sorry!", 20)
            createTextCenter((display_width / 2), (display_height / 3 + 30), "It seems you don't have enough sequence to generate a key.", 20)
            createTextCenter((display_width / 2), (display_height / 3 + 60), "Please play again and try sending more Qubits!", 20)
        button("Play Again!", 250, (display_height / 3 + 150), 300, 50, dark_green, green, game_intro)

        button("Next Level!", 250, (display_height / 3 + 250), 300, 50, dark_red, red, show_tutorial)

        pygame.display.update()
        clock.tick(15)

def sender_help():
    pass


game_intro()
#main_loop()
