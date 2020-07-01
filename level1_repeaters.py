import pygame
import time
import random
import math

import qkd
import pygame_textinput


pygame.init()
textinput = pygame_textinput.TextInput()
display_width = 800
display_height = 600

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

computers = {}
repeaters = {}

connections = {}

n = ""
msg = ""

LOSS = 0.05

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Level 1')
clock = pygame.time.Clock()


def text_objects(text, font, colour=black):
	textSurface = font.render(text, True, colour)
	return textSurface, textSurface.get_rect()

def button(text,x,y,w,h,dark,light, action=None):
	mouse = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()

	if x+w > mouse[0] > x and y+h > mouse[1] > y:
		pygame.draw.rect(gameDisplay, light,(x,y,w,h))

		if click[0] == 1 and action != None:
			action()
	else:
		pygame.draw.rect(gameDisplay, dark,(x,y,w,h))

	smallText = pygame.font.Font("freesansbold.ttf",20)
	textSurf, textRect = text_objects(text, smallText)
	textRect.center = ( int(x+(w/2)), int(y+(h/2)) )
	gameDisplay.blit(textSurf, textRect)


def quitgame():
	pygame.quit()
	quit()

def clearUI():
  gameDisplay.fill(pygame.Color("white"), (0, display_height*2/3, display_width, display_height))

def show_message(message):
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quitgame()


		gameDisplay.fill(white)

		close = button("X", display_width-40, 20, 20, 20, dark_red, red, action=main_loop)
		

		smallText = pygame.font.Font("freesansbold.ttf", 12)
		textSurf, textRect = text_objects(message, smallText)
		textRect.center = ((display_width / 2), (display_height / 3))
		gameDisplay.blit(textSurf, textRect)

		pygame.display.update()
		clock.tick(15)

def draw_grid(top_left=(0,0), width=display_width, height=int(display_height * 2/3)): # 0 gamewidth 2/3 gamewidth 
	#print(top_left, width, height)
	#print(repeaters)
	blockSize = 50 #Set the size of the grid block
	for x in range(height):
		for y in range(width):
			if x*blockSize <= width and y * blockSize <= height:
				rect = pygame.Rect(top_left[0] + x*blockSize, top_left[1] + y*blockSize,
								   blockSize, blockSize)
				if rect.topleft in repeaters and rect.topleft not in computers:
					#print(rect.topleft , "in repeaters")
					pygame.draw.rect(gameDisplay, repeaters[rect.topleft], rect, 0) #0 fill
				else:
					pygame.draw.rect(gameDisplay, grey, rect, 1)#1 dont fill

def draw_connections():
  for key in connections:
    a = int(connections[key][0][0]), int(connections[key][0][1] + 50/2)
    b = int(connections[key][1][0]), int(connections[key][1][1] + 50/2)
    pygame.draw.line(gameDisplay, green, a, b, 5)
    text = "key: (secret)"
    if connections[key][0] in computers and a[0] < display_width/2 or connections[key][1] in computers and b[0] < display_width/2: #is you
      text = "key: " + str(key)

    smallText = pygame.font.Font("freesansbold.ttf", 12)
    textSurf, textRect = text_objects(text, smallText, colour=blue)
    textRect.center = (a[0]/2 + b[0]/2, a[1]/2 + b[1]/2 + 25)
    gameDisplay.blit(textSurf, textRect)


def main_loop():
  qubits = 0
  intro = True

  while intro:
    for event in pygame.event.get():
      #print(event)
      if event.type == pygame.QUIT:
        quitgame()
    gameDisplay.fill(white)

    draw_grid((0,0), display_width, int(display_height * 2/3))
    draw_connections()

    h, w = (100,100)
    a_c = pygame.Rect((50, int(display_height/3-h/2)), (w,h))
    pygame.draw.rect( gameDisplay, blue, a_c)
    for d1 in [0,50]:
      for d2 in [0,50]:
        computers[a_c.left + d1, a_c.top + d2] = blue

    smallText = pygame.font.Font("freesansbold.ttf", 12)
    textSurf, textRect = text_objects("Your computer", smallText, colour=blue)
    textRect.center = (100, 0)
    textRect.top = a_c.bottom + 10
    gameDisplay.blit(textSurf, textRect)

    b_c = pygame.Rect((display_width-w-50, int(display_height/3-h/2)), (w,h))
    pygame.draw.rect( gameDisplay, purple, b_c)
    for d1 in [0,50]:
      for d2 in [0,50]:
        computers[b_c.left + d1, b_c.top + d2] = purple

    textSurf, textRect = text_objects("Bob's computer", smallText, colour=purple)
    textRect.center = (display_width - 100, 0)
    textRect.top = b_c.bottom + 10
    gameDisplay.blit(textSurf, textRect)


    add_button = button("add repeater", 50, 480, 150, 50, green, dark_green, action=add)

    if complete_path():
      send_button = button("send message", 250, 480, 150, 50, green, dark_green, action=send)



    pygame.display.update()
    clock.tick(15)

def add():

  pygame.mouse.set_cursor(*pygame.cursors.tri_left)
  from_grid = choice_selection("Where do you want the connection to come from", (display_width*2/3, display_height*5/6))


  pygame.mouse.set_cursor(*pygame.cursors.broken_x)
  nearest_grid = choice_selection("Choose a grid to place your new connection", (display_width*2/3, display_height*5/6), measure_distance_from=from_grid)


	#smallText = pygame.font.Font("freesansbold.ttf", 12)
	#textSurf, textRect = text_objects("Choose a grid to place your new repeater", smallText)
	#textRect.center = (display_width*2/3, display_height*5/6)
	#gameDisplay.blit(textSurf, textRect)


	

  pygame.mouse.set_cursor(*pygame.cursors.arrow)
  pygame.display.update()

  create_key(from_grid, nearest_grid)

  #main_loop()

def send():
  textinput.clear_text()
  while True:
    global msg
    events = pygame.event.get()
    for event in events:
      if event.type == pygame.QUIT:
        quitgame()
    clearUI()
    smallText = pygame.font.Font("freesansbold.ttf", 16)
    textSurf, textRect = text_objects("What message would you like to send to Bob?", smallText)
    textRect.center = (display_width*1/2, display_height*4.5/6)
    gameDisplay.blit(textSurf, textRect)

    textinput.update(events)
    gameDisplay.blit(textinput.get_surface(), (textRect.left,500))

    add_button = button("OK", textRect.left + 50, 600, 50, 50, green, dark_green, action=get_message)

    if len(msg) > 0:
      clearUI()
      binary_msg = ' '.join(format(ord(x), 'b') for x in msg)
      smallText = pygame.font.Font("freesansbold.ttf", 16)
      textSurf, textRect = text_objects("Encoding '" + msg + "' ...", smallText)
      textRect.center = (display_width*1/2, display_height*4.5/6)
      gameDisplay.blit(textSurf, textRect)


    pygame.display.update()
    clock.tick(30)

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
      #print(event)
      if event.type == pygame.QUIT:
        quitgame()
      if event.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()
        if pos[1] < display_height * 2/3:
          grid_block = (pos[0] - (pos[0]% 50), pos[1] - (pos[1] % 50))
          if is_repeater:
            if grid_block in repeaters:
              #del repeaters[grid_block]
              print("TODO: implement deletion")
            else:
              if measure_distance_from and qkd.calc_loss(LOSS, get_dist(grid_block, measure_distance_from)) == 1:
                smallText = pygame.font.Font("freesansbold.ttf", 12)
                textSurf, textRect = text_objects("Range is too great, try again", smallText, colour=red)
                textRect.center = display_width*3/4, display_height*4.5/6
                gameDisplay.blit(textSurf, textRect)
                continue
              else:
                repeaters[grid_block] = red
                draw_grid((0,0), display_width, int(display_height * 2/3))
          else:
            if grid_block not in computers: print("choice must be in a computer", 1/0)
          return grid_block

    if measure_distance_from:
      gameDisplay.fill(pygame.Color("white"), (position[0]-100, position[1] + 25, 200, 50))
      pos = pygame.mouse.get_pos()
      nearest = (pos[0] - (pos[0]% 50), pos[1] - (pos[1] % 50))
      dist =  get_dist(nearest, measure_distance_from)
      loss = qkd.calc_loss(LOSS, dist)
      label = "Distance: " + str(round(dist, 3)) + "=> loss: " + str(round(loss,3))
      colour = [(1-loss) * green[j] + loss * red[j] for j in range(3)]
      textSurf, textRect = text_objects(label, smallText, colour=colour)
      textRect.center = (position[0], position[1] + 50)
      gameDisplay.blit(textSurf, textRect)

      if remove_next and nearest != remove_next:#and nearest not in repeaters and nearest not in computers and nearest[1] * 50 < display_height * 2/3:
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
  q = None
  while True:
    global n
    #print("n=", n)

    events = pygame.event.get()
    for event in events:
      if event.type == pygame.QUIT:
        quitgame()

    clearUI()
    smallText = pygame.font.Font("freesansbold.ttf", 16)
    textSurf, textRect = text_objects("How many qubits do you want to send to the repeater to create the key?", smallText)
    textRect.center = (display_width*1/2, display_height*4.5/6)
    gameDisplay.blit(textSurf, textRect)

    textinput.update(events)
    #gameDisplay.blit(textinput.get_surface(), (display_width*1/2, display_width * 10/12))
    gameDisplay.blit(textinput.get_surface(), (textRect.left,500))

    add_button = button("OK", textRect.left + 50, 500, 50, 50, green, dark_green, action=update_n)

    try:
      n = int(n)

    except:
      if len(n) > 0:
        textSurf, textRect = text_objects("Invalid input", smallText, colour=red)
        textRect.center = (textRect.left+50, display_height*5.5/6)
        gameDisplay.blit(textSurf, textRect)

    if type(n) == int and n > 0:
      q = qkd.bb84(n, p=LOSS)
      dist = get_dist(a,b)
      q.run_protocol(dist)
      draw_lines(q.n_sent-q.n_received, q.n_received, (a[0] + 50, a[1]), b)
      
      draw_grid()
    
    if q and (not q.get_key() or q.get_key() == "error" or q.get_key() in connections):
      textSurf, textRect = text_objects("An empty or identical key has been generated, try sending more qubits", smallText, colour=red)
      textRect.topleft = (textRect.left+150, display_height*5.75/6)
      gameDisplay.blit(textSurf, textRect)
      update_n(val="")

      
    elif q:
      clearUI()

      print("great success")
  
      repeaters[b] = green
      connections[q.get_key()] = (a, b)
      print("connections: ", connections)
      if complete_path():
        show_message("Congratulations! You have created a completely secure path between you and Bob, you may now send and encrypt messages to each other")
      n = ""
      main_loop()

    pygame.display.update()
    clock.tick(30)

def update_n(val=None):
  global n
  if type(val) == str: n = val
  else: n = textinput.get_text()
  #print("n now", n, len(n))

def get_dist(p0, p1):
    return math.sqrt( ((p0[0] - p1[0])/50)**2 +((p0[1] - p1[1])/50)**2)
    #return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

def complete_path(a=(100,200), b=(650, 200)):
  if a == b: return True
  for key in connections:
    if connections[key] == (a,b): return True
    if connections[key][0] == a: return complete_path(a=connections[key][1], b=b)
    if connections[key][1] == b: return complete_path(a=a, b=connections[key][0])
  return False


def draw_lines(red_lines, green_lines, a, b):
  red_remaining = red_lines
  green_remaining = green_lines

  n_drawn = 0

  drawn_lines = {"red": [((0,0),(0,0))]*(red_lines + green_lines), "green":[]}

  while red_remaining + green_remaining > 0 or max(drawn_lines["red"]) != ((0,0),(0,0)):
    events = pygame.event.get()
    for event in events:
      if event.type == pygame.QUIT:
        quitgame()


    gameDisplay.fill(pygame.Color("white"), (a[0], a[1], b[0]-a[0], b[1]-a[1] + 50))
    if green_remaining > 0 and random.random() > red_remaining/green_remaining:
      #draw a green line
      sep = n_drawn/green_lines * 50
      coords = ((a[0], a[1] + sep), (b[0], b[1] + sep))
      #pygame.draw.line(gameDisplay, green, (a[0], a[1] + sep), (b[0], b[1] + sep)))
      drawn_lines["green"].append(coords)
      n_drawn += 1
      green_remaining -= 1
    elif red_remaining > 0:
      sep1 = random.random() * 50
      sep2 = random.random() * 50
      coords = ((a[0], a[1] + sep1), (b[0], b[1] + sep2))
      drawn_lines["red"].insert(0, coords)
      red_remaining -= 1
    
    drawn_lines["red"].insert(0, ((0,0),(0,0)))
    
    drawn_lines["red"] = drawn_lines["red"][:red_lines + green_lines]
    
    #print("drawing ", len(drawn_lines["green"]), " green lines")
    for fr, to in drawn_lines["green"]:
      pygame.draw.line(gameDisplay, green, fr, to, 2)
    for i, (fr, to) in enumerate(drawn_lines["red"]):
      if (fr, to) != (0,0): 
        c = (i+1)/len(drawn_lines["red"]) * 255
        new_col = [min(j + c, 255) for j in red]
        #print("drawing red with colour", new_col)
        pygame.draw.line(gameDisplay, red + (i/len(drawn_lines["red"]), ), fr, to)
      
    pygame.display.update()
    clock.tick(30)
    #print(drawn_lines["red"])
    
#show_message("In this level you will learn about chaining quantum repeaters to create a secure connection between any user")
main_loop()
