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
