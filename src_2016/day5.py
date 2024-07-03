import utils
# TODAY IS SLOW. 
# Nothing I can do about it except parallelize; this is dependent on md5 speed. 

def p1(input):
    password = ""

    i = 0
    while len(password) != 8:
        md5hash = utils.get_md5(input + str(i))
        if md5hash[:5] == "00000":
            password += md5hash[5]
        i += 1
    return password 


def p2(input):
    password = ["" for _ in range(8)]

    i = 0
    while "" in password:
        md5hash = utils.get_md5(input + str(i))
        if md5hash[:5] == "00000" and md5hash[5].isdigit():
            position = int(md5hash[5])
            if position < 8 and password[position] == "":
                password[position] = md5hash[6]
        i += 1
    return "".join(password)