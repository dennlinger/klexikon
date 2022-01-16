"""
Use heuristics that no sentence should end with a semicolon, which we assume for simplicity.
"""
import os

if __name__ == "__main__":
    fd = "./data/raw/wiki/"
    for fn in sorted(os.listdir(fd)):
        fp = os.path.join(fd, fn)
        with open(fp) as f:
            lines = f.readlines()

        new_line_split = []

        prev_colon = False
        curr = ""
        for line in lines:
            # Note that several rows in a row might end in semicolons, this is why we first check for that.
            if line.rstrip("\n").endswith(";"):
                curr += line.rstrip("\n") + " "
                prev_colon = True
            # Similarly, proceed with the same pattern for other forms of lines that don't end in a "period-like".
            # Inconvenient notation because at this point we could be dealing with single-character lines ("\n"),
            # which does not allow for check of line [-2]
            elif not line.startswith("==") and line.strip("\n ") and \
                    not (line.rstrip("\n").endswith(":") or line.rstrip("\n").endswith(".")
                         or line.rstrip("\n").endswith("?") or line.rstrip("\n").endswith("!")):
                curr += line.rstrip("\n") + " "
                prev_colon = True
            # Actually add the previous groupings with the current line together.
            elif prev_colon:
                # if there is an empty line after, just keep the current formatting
                if not line.strip("\n"):
                    new_line_split.append(curr.rstrip(" ") + "\n")
                    new_line_split.append(line)
                # If there is still content in the current line, add it to the fixed split.
                else:
                    curr += line
                    new_line_split.append(curr)
                curr = ""
                prev_colon = False
            # Otherwise, keep the existing split.
            else:
                # Exclude the notorious "f/ff" lines, which appear to be some horizontal separator.
                if line.strip("\n ") == "ff" or line.strip("\n ") == "f":
                    continue
                else:
                    new_line_split.append(line)

        for i, line in enumerate(new_line_split[:3]):
            # Fixed all of these mistakes.
            if len(line) < 10 and line.strip("\n ") and not line.startswith("=="):
                print(fp)
                print(line)
                print("----------")
            # Fixed all of these mistakes
            elif "Koordinaten" in line:
                print(fp)
                print(line)
                print("----------")
            # Fixed all of these automatically in the full document.
            # Remaining cases usually are succeeded by lists (ignored in this data set).
            elif line.strip("\n"):
                if line[-2] not in ".?!:" and not line.startswith("=="):
                    print(fp)
                    print(line)
                    print("----------")

            if not line.strip("\n") and i == 0:
                print(fp)
                print("Starts with empty line")
                print("----------")
            elif line[0] in "0123456789" and i == 0:
                print(fp)
                print(line)
                print("Starts with a number")
                print("----------")

        with open(fp, "w") as f:
            f.write("".join(new_line_split))



