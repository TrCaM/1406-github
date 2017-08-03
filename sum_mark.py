''' This script helps to quickly import the mark
'''

import os
import re

try:
    with open("rubric-01.md", 'r') as rubric:
        mark = 0
        pattern = r"^\d+(\.?\d+)?"
        lines = rubric.readlines()
        for idx, line in enumerate(lines):
            if re.search("final grade", line):
                lines[idx] = "%.1f/100 final grade\n" % (mark)
            elif idx == (len(lines)-3):
                lines[idx] = "<!-- %.1f -->\n" % mark
            else:
                match = re.search(pattern, line)
                mark += float(match.group(0)) if match else 0

        print("Mark is: ", mark)

    with open("rubric-01.md", 'w') as rubric:
        rubric.writelines(lines)


except FileNotFoundError:
    print("Can not find the file")
