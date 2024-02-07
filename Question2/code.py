import matplotlib.pyplot as plt

starting_position = [0, 0]

# This will give the direction like 30* from North in NW direction
def direction_calculator(degrees)->list:
    degree = degrees % 360

    return_value = ['', 0]
    
    if(degree >= 0 and degree < 90):
        return_value[0] = 'NE'
        return_value[1] = degree
    elif(degree >= 90 and degree < 180):
        return_value[0] = 'SE'
        return_value[1] = degree % 90
    elif(degree >= 180 and degree < 270):
        return_value[0] = 'SW'
        return_value[1] = degree % 180
    elif(degree >= 270 and degree < 360):
        return_value[0] = 'NW'
        return_value[1] = degree % 270

    return return_value

def getInput()->list:
    print('''
        At how many degrees from the North do you want to go?
        ''')
    try:
        degrees = float(input())
    except:
        print("Please enter valid float degrees: ")
    direction = direction_calculator(degrees)
    

    print('''
        And by how much?
        ''')

    try:
        distance = float(input())
    except:
        print("Please enter valid float distance (cm): ")
    
    print(direction)
    print(distance)

def repeat_input()->list:
    a = 1
    sequence = []
    while(a != 0):
        sequence.append(getInput())

        answer = input("Do you want to travel more? (enter = Yes, 'N' = No): ")
        if(answer.lower() == 'n'):
            a = 0
            print('Ok')

    return sequence

def plot_sequence(sequence:list[list])->int:

    return 1
        
def main():
    sequence = repeat_input()

    X = []
    Y = []

if __name__ == "__main__":
    main()
