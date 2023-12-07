import utils
import re

# https://www.dataquest.io/wp-content/uploads/2019/03/python-regular-expressions-cheat-sheet.pdf

DAY=1

word2num = {'one':1, 
            'two':2, 
            'three':3, 
            'four':4, 
            'five':5, 
            'six':6,
            'seven':7, 
            'eight':8, 
            'nine':9
}

def p1(input):
    
    input = utils.split_and_strip(input)
    sum = 0
    for line in input:
        numbers = re.findall(r'\d+?', line)
        # print(numbers)
        sum += 10*int(numbers[0]) + int(numbers[-1])

    return sum

def p2(input):
    regexstr = "one|two|three|four|five|six|seven|eight|nine"
    forward = re.compile(regexstr + "|\d+?")
    backward = re.compile(regexstr[::-1] + "|\d+?")

    input = utils.split_and_strip(input)
    sum = 0
    for line in input:
        numbers = re.findall(forward, line)
        lastnumbers = re.findall(backward, line[::-1])
        firstNum = numbers[0]    if numbers[0].isdigit() \
                                else word2num[numbers[0]]
        lastNum = lastnumbers[0] if lastnumbers[0].isdigit() \
                                else word2num[lastnumbers[0][::-1]]
        sum += 10*int(firstNum) + int(lastNum)

    return sum