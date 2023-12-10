# author: Devyash Saini
from ALPHA import User
import sys

args = sys.argv
if len(args) > 1:
    if args[1] == "--train":
        if len(args) > 2:
            res = User.train(args[2])
        else:
            print("Error: User.Name required to train\nUsage: python3 main.py --train <User.Name>")
    elif args[1] == "--detect":
        res = User.verify(False)
        if res:
            print("Program Exited with 0 errors.")
        else:
            print("Exit - err!")
    else:
        print(f"Error: Invalid argument ({args[1]})")
else: 
    res = User.verify(True)
    if res:
        print("Welcome")
    else:
        print("Get lost")