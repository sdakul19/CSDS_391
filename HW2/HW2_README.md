# Intro
This folder contains files for CSDS 391 Assignment 2. This assignment revolves around
an 8 piece puzzle configuration

# Contents
This folder contains a main.py file and a testBFS.txt file that generates an output.txt file

The main.py file contains a cmd() and cmdfile() function that are able to control the puzzle.
The cmd() function can take the commands
- setState {puzzle state}
- printState
- move {direction}
- scrambleState {n}
- comment
- reset
- solve BFS maxnodes=1000

# Running Code
To run the code run 
```
python main.py {testfile.txt}
```
You can either run main.py and in __main__ declare the commands using cmd
ex. 
```
if __name__ == "__main__":
    cmd("scrambleState 10")
    cmd("solve BFS")
    cmd(printState)
```
Or you can fill out a text file and use it in as an argument with main.py
testcmds.txt shows an example test file
```
if __name__ "__main__":
    try:
        filename = sys.argv[1]
        cmdfile(filename)
    except IndexError:
        print("Error: No file listed or doesn't exist")
```

# Running BFS Test File
The current code shouldn't need to be changed and can just be run with the following:
```
python main.py testBFS.txt
```
