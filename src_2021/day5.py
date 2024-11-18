import utils
# checking every pair of lines is O(n^2m). where m = max line length 

# input: [s1x, s1y, t1x, t1y], [s2x, s2y, t2x, t2y]
def get_parallel_int_points(line1, line2):
    (s1x, s1y), (t1x, t1y) = line1
    (s2x, s2y), (t2x, t2y) = line2

    l1_length = abs(s1x - t1x) + abs(s1y - t1y)
    l2_length = abs(s2x - t2x) + abs(s2y - t2y)
    if l1_length > l2_length:
        return get_parallel_int_points(line2, line1)
    
    # l1_length <= l2_length. iterate over l1
    xrange = utils.range_inclusive(s1x, t1x)
    yrange = utils.range_inclusive(s1y, t1y)
    if utils.slope(*line1) == 0:
        l1_points = [(x, s1y) for x in xrange]
    elif utils.slope(*line1) == float("inf"):
        l1_points = [(s1x, y) for y in yrange]
    else:
        l1_points = [(x, y) for x, y in zip(xrange, yrange)]

    intersections = []
    for point in l1_points:
        if utils.pt_on_line(point, *line2):
            intersections.append(point)
    return set(intersections)

# any chance of intersection?
def ischance(line1, line2):
    # this method makes a box with line1 and checks endpoints. 
    (s1x, s1y), (t1x, t1y) = line1
    (s2x, s2y), (t2x, t2y) = line2
    l1_box = min(s1x, t1x), max(s1x, t1x), min(s1y, t1y), max(s1y, t1y)
    l2_box = min(s2x, t2x), max(s2x, t2x), min(s2y, t2y), max(s2y, t2y)
    # https://stackoverflow.com/questions/40795709/checking-whether-two-rectangles-overlap-in-python-using-two-bottom-left-corners
    return not (l1_box[1] < l2_box[0] or \
                l1_box[0] > l2_box[1] or \
                l1_box[3] < l2_box[2] or \
                l1_box[2] > l2_box[3])

def parse_input(input):
    input = utils.split_and_strip(input)
    
    lines = []
    for line in input:
        s, t = line.split(" -> ")
        s = tuple(map(int, s.split(",")))
        t = tuple(map(int, t.split(",")))
        lines.append([s, t])

    return lines

def main(input):
    # approach 2: keep a list of the points
    import numpy as np
    p1, p2 = 0, 0
    lines = parse_input(input)
    min_x = min([min(s[0], t[0]) for s, t in lines])
    min_y = min([min(s[1], t[1]) for s, t in lines])
    max_x = max([max(s[0], t[0]) for s, t in lines])
    max_y = max([max(s[1], t[1]) for s, t in lines])

    # get the bounding box
    xrange = max_x - min_x + 1
    yrange = max_y - min_y + 1
    grid = np.zeros((xrange, yrange), dtype=int)
    s_grid = np.zeros((xrange, yrange), dtype=int)

    for line in lines:
        (sx, sy), (tx, ty) = line
        if sx == tx:
            s_grid[sx - min_x, min(sy, ty) - min_y: max(sy, ty) - min_y + 1] += 1
        elif sy == ty:
            s_grid[min(sx, tx) - min_x: max(sx, tx) - min_x + 1, sy - min_y] += 1
        else:
            xs = utils.range_inclusive(sx - min_x, tx - min_x)
            ys = utils.range_inclusive(sy - min_y, ty - min_y)
            grid[xs, ys] += 1

    grid += s_grid
    
    p1 = np.sum(s_grid > 1)
    p2 = np.sum(grid > 1)
    return p1, p2
    # whoa that was soo much easier... 


    # approach 1: iterate through the lines
    p1, p2 = 0, 0

    lines = parse_input(input)
    straights = []
    diags = []
    for line in lines:
        (sx, sy), (tx, ty) = line
        if sx == tx or sy == ty:
            straights.append(line)
        else:
            diags.append(line)

    # do just the straights intersect straights
    ss_intersect = set()
    all_intersects = set()
    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            # if not ischance(lines[i], lines[j]):
            #     continue
            l1 = lines[i]
            l2 = lines[j]
            if utils.slope(*l1) == utils.slope(*l2):
                intersects = get_parallel_int_points(l1, l2)
            else:
                intersects = set([utils.get_line_intersection(*l1, *l2)])

            # print(i,j, l1, l2, intersects)
            all_intersects = all_intersects.union(intersects)
            if l1 in straights and l2 in straights:
                ss_intersect = ss_intersect.union(intersects)

    if None in ss_intersect:
        ss_intersect.remove(None)
    if None in all_intersects:
        all_intersects.remove(None)

    p1, p2 = len(ss_intersect), len(all_intersects)

    return p1, p2


