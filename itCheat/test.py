import getopt
import sys

if __name__ == "__main__":
    argv = sys.argv[1:]
    short_options = "f:p:"
    long_options = ["force=","pin="]
    # Get the options and the arguments
    arguments, values = getopt.getopt(argv, short_options, long_options)
    # Check each option
    print(arguments)
    recArgs = {}
    for opt, arg in arguments:
        if opt in ("-f", "--force"):
            if "force" not in recArgs:
                print("Force mode: %s" % arg)
                recArgs["force"] = arg
        elif opt in ("-p", "--pin"):
            if "pin" not in recArgs:
                print("Pin mode: %s" % arg)
                recArgs["pin"] = arg
        else:
            print(opt, arg)
            print("Invalid argument")
    print("Done")