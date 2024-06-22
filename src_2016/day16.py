import utils


def transform(a):
    b = a
    b = b[::-1]
    b = b.replace('0', 'x')
    b = b.replace('1', '0')
    b = b.replace('x', '1')
    a = a + '0' + b
    return a

def once_checksum(a):
    b = ''
    for i in range(0, len(a), 2):
        s = a[i:i+2]
        if s == '00' or s == '11':
            b += '1'
        else:
            b += '0'
    return b

def checksum(a):
    while len(a) % 2 == 0:
        a = once_checksum(a)
    return a

def p1(input):
    disk_size = 272

    while len(input) < disk_size:
        input = transform(input)
    input = input[:disk_size]

    return checksum(input)

def p2(input):
    disk_size = 35651584

    while len(input) < disk_size:
        input = transform(input)
    input = input[:disk_size]

    return checksum(input)