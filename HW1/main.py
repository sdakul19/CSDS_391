import random
import sys

puzzle_config = [
    " ", 1, 2,
    3, 4, 5,
    6, 7, 8,
]
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
                    puzzle_config[i-1] = parsed_command[i]
                    
            
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
        commands = ["move up", "move down", "move left", "move right"]
        try:
            for i in range(int(parsed_command[1])):
                if empty_pos == 0:
                    commands.remove("move up")
                    commands.remove("move left")
                elif empty_pos == 2:
                    commands.remove("move up")
                    commands.remove("move right")
                elif empty_pos == 6:
                    commands.remove("move down")
                    commands.remove("move left")
                elif empty_pos == 8:
                    commands.remove("move down")
                    commands.remove("move right")
                elif empty_pos == 1:
                    commands.remove("move up")
                elif empty_pos == 7:
                    commands.remove("move down")
                elif empty_pos == 3:
                    commands.remove("move left")
                elif empty_pos == 5:
                    commands.remove("move right")
                
                cmd(random.choice(commands))
                commands = ["move up", "move down", "move left", "move right"]
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

    else:
        print(" Error: invalid command: " + command)
        message = " Error: invalid command: " + command

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
    

if __name__ == "__main__":
    try:
        filename = sys.argv[1]
        cmdfile(filename)
    except IndexError:
        print("Error: No file listed or doesn't exist")
       
    

