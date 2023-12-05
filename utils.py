def get_file_stripped_lines(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    return [l.strip() for l in lines]

def get_file_content(filename):
    with open(filename, 'r') as f:
        return f.read().strip()
