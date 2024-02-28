import utils

class GraphNode:
    def __init__(self, label):
        self.label = label
        self.children = [] # list of children objects
        self.parent = ""
        self.filesize = -1

    def print(self):
        print("node", self.label, [c.label for c in self.children], self.parent, self.filesize)

def parse_filetree(input):
    all_nodes = {}
    root = GraphNode("/")
    currentNode = root.label
    all_nodes[currentNode] = root

    linenum = 1
    while linenum < len(input):
        line = input[linenum]
        l = line.split(" ")

        if "cd" in l:
            label = l[-1]
            if label == "..":
                currentNode = all_nodes[currentNode].parent
                linenum += 1
                continue
            label = currentNode+"_"+label
            if label not in all_nodes:
                all_nodes[label] = GraphNode(label)
            currentNode = label
            linenum += 1
        if "ls" in l:
            linenum += 1
            while linenum < len(input) and "$" not in input[linenum]:
                line = input[linenum]
                l = line.split(" ")
                if "dir" in l:
                    label = l[-1]
                    label = currentNode+"_"+label
                    if label not in all_nodes:
                        all_nodes[label] = GraphNode(label)
                    all_nodes[currentNode].children.append(all_nodes[label])
                    all_nodes[label].parent = currentNode
                else:
                    fs, label = l
                    label = currentNode+"_"+label
                    if label not in all_nodes:
                        all_nodes[label] = GraphNode(label)
                    all_nodes[currentNode].children.append(all_nodes[label])
                    all_nodes[label].parent = currentNode
                    all_nodes[label].filesize = int(fs)
                linenum += 1
    return root, all_nodes

def set_directory_filesizes(root):
    if len(root.children) == 0:
        # print("leaf", root.label, root.filesize)
        return root.filesize
    else:
        # print("not leaf", root.label, root.filesize)
        total = 0
        for child in root.children:
            total += set_directory_filesizes(child)
        root.filesize = total
        return total

def p1(input):
    lines = utils.split_and_strip(input)

    root, all_nodes = parse_filetree(lines)
    # for n in all_nodes:
    #     all_nodes[n].print()
    set_directory_filesizes(root)
    directories = []
    for label in all_nodes:
        if len(all_nodes[label].children) > 0:
            directories.append(label)

    
    sum = 0
    for dir in directories:
        if all_nodes[dir].filesize < 100000:
            sum += all_nodes[dir].filesize

    return sum
    

def p2(input):
    lines = utils.split_and_strip(input)

    root, all_nodes = parse_filetree(lines)
    # for n in all_nodes:
    #     all_nodes[n].print()
    set_directory_filesizes(root)
    directories = []
    for label in all_nodes:
        if len(all_nodes[label].children) > 0:
            directories.append(label)

    space_needed = 30000000 - (70000000 - root.filesize)
    min_space = 70000000
    for dir in directories:
        if all_nodes[dir].filesize < min_space and \
             all_nodes[dir].filesize >= space_needed:
            min_space = all_nodes[dir].filesize
    return min_space