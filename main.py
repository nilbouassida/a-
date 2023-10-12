import pygame
import sys
import random
import math
pygame.init()

w, h, scl = 900, 900, 65
font = pygame.font.SysFont(None, int((scl/10)*9))
font2 = pygame.font.SysFont(None, int((scl/2)))
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("astar")

fps = 120
a = None
b = None
walls = []
terrain = []
current = None
children = []
parents = []
newParents = []
nodes = []
opened = []
closed = []
fcost = []
gcost = []
hcost = []
path = []
parents = []
closed_parents = []

state = "a"
start = False
first = True

def find_min(l, l2):
    m = l[0]
    ind = 0
    for i, j in enumerate(l):
        if j < m:
            m = j
            ind = i
        if a == m and l2 != []:
            m2 = l2[0]
            for i2, j2 in enumerate(l2):
                if j2 < m2:
                    m2 = j2
                    ind = i2
    return ind

def distance(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def round_down(num, divisor):
    return num - (num%divisor)

def write(text, x, y, color="Black"):
    text = font.render(text, 1, pygame.Color(color))
    text_rect = text.get_rect(center=(int(x), int(y)))
    screen.blit(text, text_rect)
    return text

def write2(text, x, y, color="Black"):
    text = font2.render(text, 1, pygame.Color(color))
    text_rect = text.get_rect(center=(int(x), int(y)))
    screen.blit(text, text_rect)
    return text

def find_children(current, a, walls, closed):
    x, y = current[0], current[1]
    children = []
    parents = []
    if (x, y-1) != a and (x, y-1) not in walls and (x, y-1) not in closed:
        children.append((x, y-1))
        parents.append("v")
    if (x-1, y) != a and (x-1, y) not in walls and (x-1, y) not in closed:
        children.append((x-1, y))
        parents.append(">")
    if (x+1, y) != a and (x+1, y) not in walls and (x+1, y) not in closed:
        children.append((x+1, y))
        parents.append("<")
    if (x, y+1) != a and (x, y+1) not in walls and (x, y+1) not in closed:
        children.append((x, y+1))
        parents.append("^")


    return children, parents

def find_current(opened, a, b, terrain):
    fcost = []
    gcost = []
    hcost = []
    for i, j in enumerate(opened):
        if j not in terrain:
            gcost.append(distance(j, a))
            hcost.append(distance(j, b))
            fcost.append(distance(j, a) + distance(j, b))
        else:
            gcost.append(distance(j, a))
            hcost.append(distance(j, b))
            fcost.append((distance(j, a) + distance(j, b))/2)
    return opened[find_min(fcost, hcost)], fcost, gcost, hcost

def find_fcost(closed, a, b, terrain):
    fcost = []
    gcost = []
    hcost = []
    for i, j in enumerate(closed):
        if j not in terrain:
            gcost.append(distance(j, a))
            hcost.append(distance(j, b))
            fcost.append(distance(j, a) + distance(j, b))
        else:
            gcost.append(distance(j, a))
            hcost.append(distance(j, b))
            fcost.append((distance(j, a) + distance(j, b))/2)
    return fcost

def localize_path(current, nodes, parents, a, b):
    path = []
    while current != a:
        ind = nodes.index(current)
        
        if parents[ind] == "<": 
            path.append(current)
            current = (current[0] + -1, current[1] + 0)
        if parents[ind] == ">": 
            path.append(current)
            current = (current[0] + 1, current[1] + 0)
        if parents[ind] == "^": 
            path.append(current)
            current = (current[0] + 0, current[1] + -1)
        if parents[ind] == "v": 
            path.append(current)
            current = (current[0] + 0, current[1] + 1)

    return path


clock = pygame.time.Clock()
while True:
    #####################################################################################
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                scl-=1
                font = pygame.font.SysFont(None, int((scl/10)*9))
                font2 = pygame.font.SysFont(None, int((scl/2)))
            if event.button == 5:
                scl+=1
                font = pygame.font.SysFont(None, int((scl/10)*9))
                font2 = pygame.font.SysFont(None, int((scl/2)))
    screen.fill((255, 255, 255))

    pos = (round_down(pygame.mouse.get_pos()[0], scl), round_down(pygame.mouse.get_pos()[1], scl))

    pressed = pygame.mouse.get_pressed()
    if state == "a" and pressed[0]:
        a = pygame.mouse.get_pos()
        a = (round_down(a[0], scl)/scl, round_down(a[1], scl)/scl)
        state = "na"
    if state == "b" and pressed[0]:
        b = pygame.mouse.get_pos()
        b = (round_down(b[0], scl)/scl, round_down(b[1], scl)/scl)
        state = "nb"
    if state == "w" and pressed[0]:
        wall = (round_down(pygame.mouse.get_pos()[0], scl)/scl, round_down(pygame.mouse.get_pos()[1], scl)/scl)
        if wall not in walls:
            walls.append(wall)
        state = "w"
    if state == "t" and pressed[0]:
        terr = (round_down(pygame.mouse.get_pos()[0], scl)/scl, round_down(pygame.mouse.get_pos()[1], scl)/scl)
        if terr not in terrain:
            terrain.append(terr)
        state = "t"

    if state == "na" and not(pressed[0]):
        state = "b"
    if state == "nb" and not(pressed[0]):
        state = "w"
    if state == "nw" and not(pressed[0]):
        state = "w"

    if pygame.key.get_pressed()[pygame.K_a]:
        state = "a"
    if pygame.key.get_pressed()[pygame.K_b]:
        state = "b"
    if pygame.key.get_pressed()[pygame.K_t]:
        state = "t"
    if pygame.key.get_pressed()[pygame.K_w]:
        state = "w"

    # if pos == a:
    #     state = "nw"
    #     if pressed[0]:
    #         print("a")
    #         a = pos
    # if pos == b:
    #     state = "nw"
    #     if pressed[0]:
    #         print("b")
    #         b = pos
    

    for i in range(len(walls)):
        pos = (round_down(pygame.mouse.get_pos()[0], scl), round_down(pygame.mouse.get_pos()[1], scl))
        if pressed[2] and pos == walls[i]:
            del walls[i]
            break
    

    key = pygame.key.get_pressed()
    if key[pygame.K_RETURN] and start == False:
        current = a
        start = True
    #####################################################################################


    if start:
        fps = 130
        if current == b:
            print("path found!")
            path = localize_path(current, nodes, parents, a, b)
            start = False
            key = pygame.key.get_pressed()
            if key[pygame.K_RETURN]:
                start = False
                w = []
                terrain = []
                a = None
                b = None
            
        


        children, newParents = find_children(current, a, walls, closed)
        for i, j in enumerate(children):
            if j not in opened:
                opened.append(j)
                nodes.append(j)
                parents.append(newParents[i])

        if current in opened:
            opened.remove(current)
        closed.append(current)
        

        current, fcost, gcost, hcost = find_current(opened, a, b, terrain)

        closed_fcost = find_fcost(closed, a, b, terrain)

    #pygame.draw.rect(screen, (255, 255, 255), (w, 0, 200, h))
    for i in range(len(terrain)):
        pygame.draw.rect(screen, (139, 69, 19), (terrain[i][0]*scl, terrain[i][1]*scl, scl, scl))
    for i in range(len(walls)):
        pygame.draw.rect(screen, (0, 0, 0), (walls[i][0]*scl, walls[i][1]*scl, scl, scl))
    for i in range(len(opened)):
        pygame.draw.rect(screen, (0, 255, 0), (opened[i][0]*scl, opened[i][1]*scl, scl, scl))
        # write2(str(math.floor(fcost[i])), opened[i][0]*scl+scl/2, opened[i][1]*scl+scl/2)
    for i in range(len(closed)):
        pygame.draw.rect(screen, (255, 0, 0), (closed[i][0]*scl, closed[i][1]*scl, scl, scl))
        # write2(str(math.floor(closed_fcost[i])), closed[i][0]*scl+scl/2, closed[i][1]*scl+scl/2)
    for i in range(len(path)):
        pygame.draw.rect(screen, (136, 0, 255), (path[i][0]*scl, path[i][1]*scl, scl, scl))
    for i in range(len(nodes)):
        write2(str(parents[i]), nodes[i][0]*scl+scl/2, nodes[i][1]*scl+scl/2)
    if a != None:
        pygame.draw.rect(screen, (0, 200, 255), (a[0]*scl, a[1]*scl, scl, scl))
        write("A", a[0]*scl+scl/2, a[1]*scl+scl/2)
    if b != None:
        pygame.draw.rect(screen, (0, 200, 255), (b[0]*scl, b[1]*scl, scl, scl))
        write("B", b[0]*scl+scl/2, b[1]*scl+scl/2)
    if current != None and start:
        pygame.draw.rect(screen, (255, 255, 0), (current[0]*scl, current[1]*scl, scl, scl))
    for i in range(1, int(w/scl)+1):
        pygame.draw.line(screen, (0, 0, 0), (0, i*scl), (w, i*scl), 2)
        pygame.draw.line(screen, (0, 0, 0), (i*scl, 0), (i*scl, h), 2)
    pygame.display.update()
