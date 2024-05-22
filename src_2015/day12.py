import re, json

def p1(input):
    nums = map(int, re.findall(r'-?\d+', input))
    return sum(nums)

def get_sum(json_obj):
    if type(json_obj) == dict:
        if "red" in json_obj.values():
            return 0
        return sum(get_sum(v) for v in json_obj.values())
    elif type(json_obj) == list:
        return sum(get_sum(v) for v in json_obj)
    elif type(json_obj) == int:
        return json_obj
    return 0


def p2(input):
    input = json.loads(input)
    return get_sum(input)