
from ursina import *

# indices are 1-indexed

class Vulture:
    global occupied
    global positions
    global adjacent_positions
    def __init__(self, position:list):
        Entity(model = 'vulture_prototype', 
               position = position,
               rotation = Vec3(0, 0, 0),
               scale = 0.1);
        self.initial_position = position
        self.current_position = position
        self.index = 1
        for i in range(len(positions)):
            if(positions[i][0] == position[0] and positions[i][1] == position[1]):
                self.index = i + 1
                break

        self.entity = Entity(model = 'vulture',
           position = Vec3(position[0], position[1], position[2]),
           rotation = Vec3(0, 0, 0),
           texture = 'cobblestone',
           scale = 0.1
           )
    def updatePosition(self, index):
        self.position = positions[index]

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
        for i in adjacent_positions[self.index]:
            if block_index in adjacent_positions[i]:
                if occupied[block_index] == 0 and occupied[i] == 1:
                    occupied[self.index] = 0
                    occupied[i] = 0             # Use the return statement somehow to remove the crow from the board
                    self.index = block_index
                    self.updatePosition(block_index)
                    occupied[self.index] = 1
                
                    return 0
        
        return 1