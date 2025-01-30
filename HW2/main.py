import random
import sys
import re
from collections import deque
# import puzzle_state


puzzle_config = [
    " ", 1, 2,
    3, 4, 5,
    6, 7, 8
]

goal_state = tuple([
    " ", 1, 2,
    3, 4, 5,
    6, 7, 8
])

empty_pos = 0
seed = 0
def cmd(command: str):
    """
    This function takes a command string as input and performs the corresponding action.
    """

    global empty_pos
    global puzzle_config
    global seed
    message = ""

    parsed_command = command.split(" ")
    if parsed_command[0] == "setState":
        expected_numbers = set(str(i) for i in range(0, 9))
        if len(parsed_command[1:]) != 9 or expected_numbers.issubset(set(parsed_command[1:])) == False:
            print("Error: Invalid Puzzle State")
            message = "Error: Invalid Puzzle State"
        else:
            for i in range(1, len(parsed_command)):
                if parsed_command[i] == '0':
                    puzzle_config[i-1] = " "
                    empty_pos = i-1
                else:
                    puzzle_config[i-1] = int(parsed_command[i])
            
    elif parsed_command[0] == "printState":
        print("|" + str(puzzle_config[0]) + "|" + str(puzzle_config[1]) + "|" + str(puzzle_config[2]) + "|")
        print("|" + str(puzzle_config[3]) + "|" + str(puzzle_config[4]) + "|" + str(puzzle_config[5]) + "|")
        print("|" + str(puzzle_config[6]) + "|" + str(puzzle_config[7]) + "|" + str(puzzle_config[8]) + "|")
        message = ("|" + str(puzzle_config[0]) + "|" + str(puzzle_config[1]) + "|" + str(puzzle_config[2]) + "|\n" + 
        "|" + str(puzzle_config[3]) + "|" + str(puzzle_config[4]) + "|" + str(puzzle_config[5]) + "|\n" + 
        "|" + str(puzzle_config[6]) + "|" + str(puzzle_config[7]) + "|" + str(puzzle_config[8]) + "|" )

    elif parsed_command[0] == "move":
        direction = parsed_command[1]
        if direction.lower() == "up":

            if empty_pos < 3:
                print("Error: Invalid Move")
                message = "Error: Invalid Move"
            else:
                puzzle_config[empty_pos] = puzzle_config[empty_pos - 3]
                puzzle_config[empty_pos - 3] = " "
                empty_pos -=3
        
        elif direction.lower() == "down":
            if empty_pos > 5:
                print("Error: Invalid Move")
                message = "Error: Invalid Move"
            else:
                puzzle_config[empty_pos] = puzzle_config[empty_pos + 3]
                puzzle_config[empty_pos + 3] = " "
                empty_pos +=3

        elif direction.lower() == "left":
            if empty_pos % 3 == 0:
                print("Error: Invalid Move")
                message = "Error: Invalid Move"
            else:
                puzzle_config[empty_pos] = puzzle_config[empty_pos - 1]
                puzzle_config[empty_pos - 1] = " "
                empty_pos -=1

        elif direction.lower() == "right":
            if empty_pos % 3 == 2:
                print("Error: Invalid Move")
                message = "Error: Invalid Move"
            else:
                puzzle_config[empty_pos] = puzzle_config[empty_pos + 1]
                puzzle_config[empty_pos + 1] = " "
                empty_pos +=1
    elif parsed_command[0] == 'setSeed':
        seed = random.seed(int(parsed_command[1]))
        message = ""

    elif parsed_command[0] == "scrambleState":
        cmd("reset")
        commands = ["move left", "move right", "move up", "move down"]
        try:
            for i in range(int(parsed_command[1])):
                commands = optimize_commands(commands, empty_pos)
                
                cmd(random.choice(commands))
                commands = ["move left", "move right", "move up", "move down"]
        except IndexError:
            print("Error: No Scramble Occurred")
            message = "Error: No Scramble Occurred"
        

    elif parsed_command[0] == "#" or parsed_command[0] == "//":
        print(command)
        messsage = command
        
    elif parsed_command[0] == "reset":
        puzzle_config = [
            " ", 1, 2,
            3, 4, 5,
            6, 7, 8,
        ]
        empty_pos = 0
    elif parsed_command[0] == "":
        pass
    
    elif parsed_command[0] == "solve":
        
        # Frontier a queue to store the nodes that are to be expanded
        # Explored a set to store the nodes that have been expanded
        try:
            match = re.search(r"maxnodes=(\d+)", parsed_command[2])
            if match:
                maxNodes = int(match.group(1))

            else:
                print("Error: Incorrectly declared maxnodes")
                return "Error: Incorrectly declared maxnodes: " + command
        except:
            maxNodes = 1000
            
        frontier = deque([(puzzle_config, [])])
        explored = set()
        explored.add(tuple(puzzle_config))
        nodeCount = 0
        
        if tuple(puzzle_config) == goal_state:
            frontier.clear()
            print("Puzzle already in goal state!")
            message = "Puzzle already in goal state!"

        while frontier:
            current_state, path = frontier.popleft()

            if nodeCount > maxNodes:
                print(f"Error: Max Nodes Exceeded {maxNodes}")
                message = "Error: Max Nodes Exceeded " + str(maxNodes) 
                break

            empty_pos = current_state.index(" ")

            commands = optimize_commands(["move left", "move right", "move up", "move down"], empty_pos)  
            
            for command in commands:

                empty_pos = current_state.index(" ")
                puzzle_config = list(current_state)
                
                cmd(command)

                nxt_state = tuple(puzzle_config)

                if nxt_state == goal_state:
                    
                    message = ("Solution found!\nNodes created during search: " + 
                            str(nodeCount) + "\nSolution length: " + str(len(path) + 1) + "\nMove sequence:\n")

                    for step in path + [command]:
                        message += step + "\n"
    
                    print(message)
                    return message


                if nxt_state not in explored:
                    explored.add(nxt_state)
                    frontier.append((nxt_state, path + [command]))
                    nodeCount += 1
                    
    else:
        print("Error: invalid command: " + command)
        message = "Error: invalid command: " + command

    return message + "\n" if message != "" else ""
        
def cmdfile(filename:str):
    """
    This function reads a file and calls the cmd function for each line in the file.
    """
    try:
        with open(filename, 'r') as Readfile:
            with open("output.txt", 'w') as Writefile:
                for line in Readfile:
                    command = line.strip().split(" ")
                    print(line.strip())
                    Writefile.write(line.strip() + "\n")
                    if(not(command[0] == "#" or command[0] == "//" or command[0] == "" or command[0] == "printState")):
                        Writefile.write(cmd(line.strip()))
                        Writefile.write(cmd("printState") + "\n")
                    elif(command[0] == "printState"):
                        Writefile.write(cmd(line.strip()))
    except Exception:
        print("This file doesn't exist or can't be read from")
        Writefile.write("This file doesn't exist or can't be read from" + "\n")
    
def optimize_commands(commands: list[str], empty_pos):
    """
    Optimizes valid moves based on the empty position.
    """
    try:
        if empty_pos < 3:
            commands.remove("move up")
        if empty_pos > 5:
            commands.remove("move down")
        if empty_pos % 3 == 0:
            commands.remove("move left")
        if empty_pos % 3 == 2:
            commands.remove("move right")
    except:
        print("Error: Incorrect set of commands")
    
    return commands
        

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        cmdfile(filename)
    except IndexError:
        print("Error: No file listed or doesn't exist")

    # cmd("setState 1 2 0 3 4 5 6 7 8")
    # cmd("printState")
    # cmd("solve BFS")
    
    
       
    

