import os
import re

try:
    with open('rubric-03.md', 'r') as rubric:
        lines = rubric.readlines()
        mark = float(re.search(r'\d+(\.[0-9])?', lines[-3]).group(0))
        lines.insert(-4, "%.1f/100 final grade\n\n Marked by Ryan\n\n" % mark)

    with open("rubric-03.md", 'w') as rubric:
        rubric.writelines(lines)


except FileNotFoundError:
    print("Can not find the file")
