def read_lines(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    return [l.strip() for l in lines]

def get_file_content(filename):
    with open(filename, 'r') as f:
        return f.read().strip()
    
def get_file_content_raw(filename):
    with open(filename, 'r') as f:
        return f.read()
    
def split_lines(filecontents):
    return filecontents.split("\n")

def split_and_strip(filecontents):
    lines = [l.strip() for l in filecontents.split("\n")]
    if lines[-1] == "":
        lines.pop()
    return lines