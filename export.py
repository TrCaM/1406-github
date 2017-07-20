#!/usr/bin/python3
''' This script to export feedback file from submissions
'''

import sys
import os
import argparse
def main():

    args = args_handle()

    if os.path.isdir(args.input[1]) or os.path.isdir("./" +args.input[1]):
        print("Will get ", args.input[0],"  from here")
    else:
        print("The folder doesn't exist")



def args_handle():
    ''' Handle input options via command line arguments
    '''
    parser = argparse.ArgumentParser(prog='export.py')
    parser.add_argument("input", nargs=2, help="input path for the directory",
                        default= "./")

    args = parser.parse_args()
    return args

if __name__ == "__main__":
    main()
