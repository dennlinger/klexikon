"""
Spacy interprets years with a period as a section heading (i.e., new sentence), instead of correctly assigning them
to the previous sentence. This script fixes this bug.
"""

import regex
import os

if __name__ == '__main__':
    source_dir = "./data/gold"

    for fn in os.listdir(source_dir):
        fp = os.path.join(source_dir, fn)

        with open(fp) as f:
            lines = f.readlines()

        new_lines = []
        for idx, line in enumerate(lines):
            clean_line = line.strip("\n ")
            if regex.match("[0-9]{1,6}.*Koordinaten:", clean_line):
                print("Found coordinates")
                print(fp)
                print(line)
            elif regex.match("[0-9]{1,6}\.", clean_line):
                # print(fp)
                # print(lines[idx-1].strip("\n"))
                # print(line)
                prev_line = new_lines[-1].replace('\n', ' ')
                new_lines[-1] = f"{prev_line}{line}"
            else:
                new_lines.append(line)

        with open(fp, "w") as f:
            f.write("".join(new_lines))