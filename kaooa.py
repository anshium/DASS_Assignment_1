

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

for i in range(10):
    Entity(model = 'platform',
           position = Vec3(positions[i][0], positions[i][1], 0),
           rotation = Vec3(0, 0, 0),
           texture = 'grass',
           scale = 0.1
           )
    
objects = []
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

occupied = dict()
for i in range(0, 10):
    occupied[i] = 0

class Vulture:
    global occupied
    global positions
    global adjacent_positions
    def __init__(self, index):
        self.index = index
        self.initial_position = Vec3(positions[index][0], positions[index][1], -1)
        self.current_position = self.initial_position
        self.entity = Entity(model = 'vulture_prototype', 
               position = self.initial_position,
               rotation = Vec3(0, 0, 0),
               scale = 0.5)
    def updatePosition(self, index):
        self.position = positions[index]
        self.entity.position = self.position

    # Moves the vulture to a spot that does not have a crow. 
    def moveToBlockNoCrow(self, block_index:int):
        if block_index in adjacent_positions[self.index]:
            if occupied[block_index] == 0:
                occupied[self.index] = 0
                self.index = block_index
                self.updatePosition(block_index)
                occupied[self.index] = 1
                
                return 0
        return 1
    
    # Tries to jump over some crow in any of the blocks adjacent to it. If it fails, it returns 1, otherwise returns 0 
    # Assuming only one vulture, rest all crows. This code will break if that is not the case. However, we can change occupied    
    def moveToBlockOverCrow(self, block_index:int) -> bool:
        for i in adjacent_positions[self.index + 1]:
            if block_index in adjacent_positions[i + 1]:
                if occupied[block_index] == 0 and occupied[i] == 1:
                    occupied[self.index] = 0
                    occupied[i] = 0             # Use the return statement somehow to remove the crow from the board
                    self.index = block_index
                    self.updatePosition(block_index)
                    occupied[self.index] = 1
                
                    return 0
        
        return 1

move = 0

def incrementMove():
    global move
    move+=1


abc = 1

newVulture = Vulture(0)
newVulture.entity.color = color.green

def update():
    global move
    global abc
    if held_keys['m']:
        if(move == 1):
            val = newVulture.moveToBlockNoCrow(8)
        elif(move == 2):
            val = newVulture.moveToBlockNoCrow(9)
        elif(move == 3):
            val = newVulture.moveToBlockNoCrow(5)  
        if(abc == 1):
            move+=1
            abc = 0
        
    if held_keys['k']:
        abc = 1

Sky(texture = 'stars2')
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
