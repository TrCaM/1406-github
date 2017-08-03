''' This script copy given file to all sub folders in this folder
'''
import shutil
import os
import stat
import sys

for dir_name in os.listdir():
    if os.path.isdir(dir_name):
        os.chmod(dir_name, stat.S_IWRITE)
        for name in sys.argv[1:]:
            shutil.copyfile(name, os.path.join(dir_name, name))
