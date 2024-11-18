import utils
'''  
8:     
 aaaa  
b    c 
b    c 
 dddd  
e    f 
e    f 
 gggg  
'''

def main(input):
    input = utils.split_and_strip(input)

    p1 = 0
    p2 = 0
    for line in input:

        all_ten = line.split("|")[0].split(" ")
        one =   [i for i in all_ten if len(i) == 2][0]
        seven = [i for i in all_ten if len(i) == 3][0]
        four =  [i for i in all_ten if len(i) == 4][0]
        eight = [i for i in all_ten if len(i) == 7][0]
        a = [k for k in seven if k not in one]
        bd = [k for k in four if k not in one]

        # 5-char number which overlaps with 1 is 3. 
        three = [k for k in all_ten if set(one) <= set(k) and len(k) == 5][0]

        # 6-char number which overlaps with 3 is 9. 
        nine = [k for k in all_ten if set(three) <= set(k) and len(k) == 6][0]
        b = [k for k in nine if k not in three][0]

        remaining = [k for k in all_ten if k not in [one, seven, four, eight, three, nine]]
        # 0, 2, 5, 6, left
        # 5-char with b is 5        
        five = [k for k in remaining if b in k and len(k) == 5][0]
        remaining.remove(five)
        two = [k for k in remaining if len(k) == 5][0]
        remaining.remove(two)

        # if overlap w 1, then is 0
        zero = [k for k in remaining if set(one) <= set(k)][0]
        remaining.remove(zero)
        six = remaining[0]

        numbers = [zero, one, two, three, four, five, six, seven, eight, nine]
        numbers = [set(n) for n in numbers]

        # now, decode

        nums = line.split("|")[-1].strip().split(" ")
        full_num = 0
        for n in nums:
            # part 1
            if len(n) in [2, 3, 4, 7]:
                p1 += 1
            # part 2
            full_num *= 10
            n = set(n)
            num = [k for k in numbers if n <= k and k <= n][0]
            full_num += numbers.index(num)       
        p2 += full_num

    return p1, p2