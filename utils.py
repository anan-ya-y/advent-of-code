def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    return [l.strip() for l in lines]


def split_lines(filecontents):
    return filecontents.split("\n")

def split_and_strip(filecontents):
    lines = [l.strip() for l in filecontents.split("\n")]
    if lines[-1] == "":
        lines.pop()
    return lines