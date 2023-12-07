import utils

def n_unique_chars(line, n):
    for i in range(len(line)-n-1):
        if len(set(line[i:i+n])) == n:
            return line[i:i+n], i+n

def get_packet_start(line, n):
    return n_unique_chars(line, n)[1]


def p1(line):
    packet_start = get_packet_start(line, 4)
    return (packet_start)
def p2(line):
    packet_start = get_packet_start(line, 14)
    return (packet_start)


# p1("mjqjpqmgbljsphdztnvjfqwrcgsmlb")
# with open('inputs/6.real.txt', 'r') as f:
#     line = f.readlines()[0]
# p1(line)
# # part 2
# print(get_packet_start(line, 14))