

from hmac import new
from ursina import *
from ursina import texture
import time
# import vulture

import PIL

import math

app = Ursina()

size = 20
s = 20
small_size = 10

positions = [[0, s]]

angle = 72
ar = math.radians(72)

# I just need to do it like 4 times, one point is already there
for i in range(1, 5):
    x = positions[i - 1][0]
    y = positions[i - 1][1]
        
    X = x * math.cos(ar) + y * math.sin(ar)
    Y = - x * math.sin(ar) + y * math.cos(ar)

    positions.append([X, Y])
    
positions.append([0, -small_size])
for i in range(6, 10):
    x = positions[i - 1][0]
    y = positions[i - 1][1]
    
    X = x * math.cos(ar) + y * math.sin(ar)
    Y = - x * math.sin(ar) + y * math.cos(ar)    

    positions.append([X, Y])

platforms = dict()
for i in range(10):
     platforms[i] = Entity(model = 'platform',
           position = Vec3(positions[i][0], positions[i][1], 0),
           rotation = Vec3(0, 0, 0),
           texture = 'texture1',
           scale = 0.1,
           collider='box'
           )
    
adjacent_positions = {
        0:  [7, 8],
        1:  [8, 9],
        2:  [5, 9],
        3:  [5, 6],
        4:  [6, 7],
        5:  [2, 3, 6, 9],
        6:  [3, 4, 5, 7],
        7:  [0, 4, 6, 8],
        8:  [0, 1, 7, 9],
        9:  [1, 2, 5, 8]
}

two_jump_moves = {
        0:  [6, 9],
        1:  [7, 5],
        2:  [8, 6],
        3:  [7, 9],
        4:  [5, 8],
        5:  [1, 4],
        6:  [0, 2],
        7:  [1, 3],
        8:  [2, 4],
        9:  [0, 3]
}

occupied = dict()
for i in range(0, 10):
    occupied[i] = 0
    
# This would be of the format {number: [position_index, Entity Object], ...}
crows_and_their_position_indices = dict()
for i in range(7):
    crows_and_their_position_indices[i + 1] = [-1, 0]

class Vulture:
    global occupied
    global positions
    global adjacent_positions
    global platforms
    global crows_and_their_position_indices
    def __init__(self, index):
        self.index = index
        self.initial_position = Vec3(positions[index][0], positions[index][1], -1)
        self.current_position = self.initial_position
        self.entity = Entity(model = 'vulture_prototype', 
               position = self.initial_position,
               rotation = Vec3(0, 0, 0),
               scale = 0.5)
        occupied[self.index] = 1
    def updatePosition(self, index):
        self.position = positions[index]
        self.entity.position = self.position

    # Moves the vulture to a spot that does not have a crow. 
    def moveToBlockNoCrow(self, block_index:int):
        if block_index in adjacent_positions[self.index]:
            if occupied[block_index] == 0 or 1:
                occupied[self.index] = 0
                self.index = block_index
                self.updatePosition(block_index)
                occupied[self.index] = 1
                
                return 0
        return 1
    def highlightAdjacent(self)->list:
        possibilities = []
        for i in range(0, 10):
            platforms[i].color = color.red
        for i in range(0, 10):
            if(i in adjacent_positions[self.index]):
                if(i == 8):
                    print("heya")
                if(occupied[i]):
                    print("Here")
                    for j in adjacent_positions[i]:
                        if(j == 9):
                            print("Hola")
                        if j in two_jump_moves[self.index]:
                            platforms[i].color = color.red
                            platforms[j].color = color.green
                            possibilities.append(j)
                else:
                    platforms[i].color = color.green
                    possibilities.append(i)
        return possibilities
          
    # Tries to jump over some crow in any of the blocks adjacent to it. If it fails, it returns 1, otherwise returns 0 
    # Assuming only one vulture, rest all crows. This code will break if that is not the case. However, we can change occupied    
    def moveToBlockOverCrow(self, block_index:int) -> bool:
        for i in adjacent_positions[self.index]:
            if block_index in adjacent_positions[i]:
                print("Here")
                if occupied[block_index] == 0 and occupied[i] == 1:
                    occupied[self.index] = 0
                    occupied[i] = 0             # Use the return statement somehow to remove the crow from the board
                    self.index = block_index
                    self.updatePosition(block_index)
                    occupied[self.index] = 1
                    
                    for key, value in crows_and_their_position_indices.items():
                        print(key, value)
                        if(value[0] == i):
                            destroy(value[1])

                    return 0
        return 1

class Crow:
    global occupied
    global positions
    global adjacent_positions
    global crows_and_their_position_indices
    def __init__(self, number, index):
        self.index = index
        self.initial_position = Vec3(positions[index][0], positions[index][1], -1)
        self.current_position = self.initial_position
        self.entity = Entity(model = 'crow_prototype', 
               position = self.initial_position,
               rotation = Vec3(0, 0, 0),
               scale = 0.5)
        occupied[self.index] = 1
        self.number = number
        crows_and_their_position_indices[self.number] = [index, self.entity]
    def updatePosition(self, index):
        self.position = positions[index]
        self.entity.position = self.position
        crows_and_their_position_indices[self.number] = [index, self.entity]

    # Moves the vulture to a spot that does not have a crow. 
    def moveToBlock(self, block_index:int):
        if block_index in adjacent_positions[self.index]:
            if occupied[block_index] == 0:
                occupied[self.index] = 0
                self.index = block_index
                self.updatePosition(block_index)
                occupied[self.index] = 1
                
                return 0
        return 1

move = 0

def incrementMove():
    global move
    move+=1

def changeTurnText(turn, textBox:Entity):
    if turn == 0:
        textBox.text = 'Turn: Vulture'
    elif turn == 1:
        textBox.text = 'Turn: Crow, Drop phase'


text_box = Text(text = 'Turn: Vulture')
text_box.origin = (0, 15)

abc = 1

initial_vulture_index = 0

newVulture = Vulture(initial_vulture_index)
newVulture.entity.color = color.green

possibilities = newVulture.highlightAdjacent()

def clear_highlighting():
    global platforms
    i = 0
    for i in range(10):
        platforms[i].color = color.white

i = 0
xyz = 0
selected_index = 0
turn = 0        # 0: Vulture, 1: Crows
allowed_to_change_turns = 0

new_crow_position = 0

fgh = 0

p = -1

crow_index = 1
allowed = 0

phase = 0   # 0: drop phase, 1: move phase

current_moving_crow = 1 # Identified by a 0-indexed number that user crows_and_their_position_indices

def update():
    global turn
    global move
    global abc
    global platforms
    global i
    global xyz
    global selected_index
    global allowed_to_change_turns
    global text_box
    global possibilities
    global fgh
    global p
    global new_crow_position
    global crow_index
    global allowed
    global crows_and_their_position_indices
    global phase
    global current_moving_crow
    if(turn == 0):
        if held_keys['m']:
            '''if(move == 1):
                val = newVulture.moveToBlockOverCrow(9)
                newVulture.highlightAdjacent()
                print(val)
            elif(move == 2):
                val = newVulture.moveToBlockNoCrow(2)
                newVulture.highlightAdjacent()
                print(val)
            elif(move == 3):
                val = newVulture.moveToBlockNoCrow(5) 
                newVulture.highlightAdjacent()
                highlight_particular(newVulture)
                print(val)'''
            if(abc == 1):
                platforms[selected_index].color = color.white

                for i in adjacent_positions[newVulture.index]:
                    if(occupied[i]):
                        for j in adjacent_positions[i]:
                            if j in two_jump_moves[newVulture.index]:
                                newVulture.moveToBlockOverCrow(j)
                newVulture.moveToBlockNoCrow(selected_index)
        
                possibilities = newVulture.highlightAdjacent()    
                move+=1
                abc = 0
                newVulture.entity.color = color.yellow
    
        if held_keys['k']:    
            newVulture.entity.color = color.green
            abc = 1


        if held_keys['o']:
            if(xyz == 0):
                platforms[possibilities[i % len(possibilities)]].color = color.green
                i += 1
                xyz = 1
                platforms[possibilities[i % len(possibilities)]].color = color.yellow
                selected_index = possibilities[i % len(possibilities)]
                print(selected_index)
        
        if held_keys['p']:
            xyz = 0
    
    if(turn == 1):
        if(phase == 0):
            if held_keys['o']:
                if(fgh == 1):
                    platforms[p % 10].color = color.white
                    p += 1
                    print("ye")
                    while(occupied[p % 10] == 1):
                        p += 1
                    platforms[p % 10].color = color.green
                    new_crow_position = p % 10

                    fgh = 0
            if held_keys['p']:
                fgh = 1
        
            if held_keys['space'] and allowed:
                if(not occupied[new_crow_position]):
                    if(crow_index <= 7):
                        new_crow = Crow(crow_index, new_crow_position)
                        crow_index += 1
                        allowed = 0
                    if(crow_index == 8):
                        phase = 1
                        fgh = 0
                        p = 0
                        allowed = 0
            if held_keys['g']:
                allowed = 1
        elif(phase == 1):
            if held_keys['r']:
                if(fgh == 1): 
                    crows_and_their_position_indices[p % len(crows_and_their_position_indices) + 1][1].color = color.white
                    p += 1
                    crows_and_their_position_indices[p % len(crows_and_their_position_indices) + 1][1].color = color.salmon
                    current_moving_crow = p
                    fgh = 0
            if held_keys['b']:
                fgh = 1
                
            if held_keys['space'] and allowed:
               crows_and_their_position_indices[p % len(crows_and_their_position_indices) + 1][1].color = color.green

            if held_keys['g']:
                allowed = 1

    if held_keys['u']:
        if(allowed_to_change_turns == 1):
            turn = (turn + 1) % 2
            allowed_to_change_turns = 0
            changeTurnText(turn, text_box)
            clear_highlighting()
            if(turn == 0):
                possibilities = newVulture.highlightAdjacent()    
    if held_keys['t']:
        allowed_to_change_turns = 1
     
    if held_keys['d']:
        camera.position += Vec3(0.5, 0, 0)
    if held_keys['a']:
        camera.position += Vec3(-0.5, 0, 0)
    if held_keys['w']:
        camera.rotation += Vec3(0.5, 0, 0)
    if held_keys['s']:
        camera.rotation += Vec3(-0.5, 0, 0)
        
    if held_keys['l']:
        print(crows_and_their_position_indices)
Sky(texture = 'background6')
'''
platformOne = Entity(model = 'platform',
                     color = color.rgb(255, 0, 0),
                     position = Vec3(0, 0, 0),
                     rotation = Vec3(0, 10, 0), 
                     texture = 'brick',
                     scale = 2
                     )
platformTwo = Entity(model = 'platform',
                     color = color.rgb(255, 0, 0),
                     position = Vec3(0, 0, 0),
                     rotation = Vec3(0, 10, 0),
                     texture = 'brick',
                     scale = 2
                     )
platformThree = Entity(model = 'platform',
                     color = color.rgb(255, 0, 0),
                     position = Vec3(0, 0, 0),
                     rotation = Vec3(0, 10, 0),
                     texture = 'brick',
                     scale = 2
                     )
platformFour = Entity(model = 'platform',
                     color = color.rgb(255, 0, 0),
                     position = Vec3(0, 0, 0),
                     rotation = Vec3(0, 10, 0),
                     texture = 'brick',
                     scale = 2
                     )
platformFive = Entity(model = 'platform',
                     color = color.rgb(255, 0, 0),
                     position = Vec3(0, 0, 0),
                     rotation = Vec3(0, 10, 0),
                     texture = 'brick',
                     scale = 2
                     )
platformSix = Entity(model = 'platform',
                     color = color.rgb(255, 0, 0),
                     position = Vec3(0, 0, 0),
                     rotation = Vec3(0, 10, 0),
                     texture = 'brick',
                     scale = 2
                     )
platformSeven = Entity(model = 'platform',
                     color = color.rgb(255, 0, 0),
                     position = Vec3(0, 0, 0),
                     rotation = Vec3(0, 10, 0),
                     texture = 'brick',
                     scale = 2
                     )
platformEight = Entity(model = 'platform',
                     color = color.rgb(255, 0, 0),
                     position = Vec3(0, 0, 0),
                     rotation = Vec3(0, 10, 0),
                     texture = 'brick',
                     scale = 2
                     )
platformNine = Entity(model = 'platform',
                     color = color.rgb(255, 0, 0),
                     position = Vec3(0, 0, 0),
                     rotation = Vec3(0, 10, 0),
                     texture = 'brick',
                     scale = 2
                     )
platformTen = Entity(model = 'platform',
                     color = color.rgb(255, 0, 0),
                     position = Vec3(0, 0, 0),
                     rotation = Vec3(0, 10, 0),
                     texture = 'brick',
                     scale = 2
                     )
'''
camera = EditorCamera()
camera.position = Vec3(0, -70, -40)
camera.rotation = Vec3(-60, 0, 0)
app.run()

'''
import pygame
import time
import math
# pygame setup
pygame.init()
Width = 1280
Height = 720
screen = pygame.display.set_mode((Width, Height))
clock = pygame.time.Clock()
running = True

class Vulture:
    pass

def playable_positions(x, y, size):
    points = []
    
    angle = math.radians(36)
    
    x_original = x
    y_original = y

    points.append([x, y])                   # Point 1
    x = x + size
    y = y
    points.append([x, y])                   # Point 2
    x = x - math.cos(angle) * size
    y = y + math.sin(angle) * size
    points.append([x, y])                   # Point 3
    x = x + math.cos(2 * angle) * size
    y_low_keep = y
    y = y - size * math.sin(2 * angle)
    points.append([x, y])                   # Point 4
    x = x + math.cos(2 * angle) * size;
    y = y_low_keep
    points.append([x, y])                   # Point 5
    
    points.append([x_original, y_original])

    points_copy = [[0, 0]] * len(points)

    for i in range(len(points)):
        points_copy[i] = points[i]

    for i in range(len(points_copy) - 1):
        # print((points_copy[i] + points_copy[i + 1]))
        L1 = points_copy[i] 
        L2 = points_copy[i + 1]
        L3 = [0, 0]
        L4 = [0, 0]
        L3[0] = (L1[0] + L2[0]) * (1 / 3)
        L3[1] = (L1[1] + L2[1]) * (1 / 3)
        L4[0] = (L1[0] + L2[0]) * (2 / 3)
        L4[1] = (L1[1] + L2[1]) * (2 / 3)

        points.insert(points.index(L1) + 1, L4)
        points.insert(points.index(L1) + 1, L3)

    return points 

def draw_star(surface, x, y, size):
    # I am going for a polygon approach for this
    points = []
    
    angle = math.radians(36)
    
    x_original = x
    y_original = y

    points.append([x, y])                   # Point 1
    x = x + size
    y = y
    points.append([x, y])                   # Point 2
    x = x - math.cos(angle) * size
    y = y + math.sin(angle) * size
    points.append([x, y])                   # Point 3
    x = x + math.cos(2 * angle) * size
    y_low_keep = y
    y = y - size * math.sin(2 * angle)
    points.append([x, y])                   # Point 4
    x = x + math.cos(2 * angle) * size;
    y = y_low_keep
    points.append([x, y])                   # Point 5
    
    points.append([x_original, y_original])

    pygame.draw.polygon(surface, 'black', points, 2)
    
    return points

def baseboard(x=0, y=0):
    size = 500
    points = draw_star(screen, Width / 2 - size / 2, Height / 2, 500)
    
    # Draw the points
    for i in range(len(points)):
        pygame.draw.circle(screen, 'black', points[i], 20, width = 2)
    
positions = playable_positions(Width / 2, Height / 2, 10)
points = draw_star(screen, Width / 2 - 10 / 2, Height / 2, 500)
print(positions)
print(points)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # fill the screen with a color to wipe away anything from last frame
    screen.fill(pygame.Color(235, 210, 52))
    # +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
    
    # Find playable position

    # Rendering the game // Not sure if this is the right thing to say
    baseboard(1280 / 2, 720 / 2)
    
    pygame.draw.polygon(screen, 'black', positions, 2) 

    # +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=
    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(60)# limits FPS to 60
pygame.quit()           
'''
