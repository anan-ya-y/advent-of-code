import utils

# 1568849600


all_shapes = []
def p1(inp):
    global all_shapes
    inp = utils.split_and_strip(inp)
    inp = [tuple(map(int, x.split(','))) for x in inp]
    
    p1 = 0
    all_shapes = []
    for i in range(len(inp)):
        for j in range(i + 1, len(inp)):
            xdiff = abs(inp[i][0] - inp[j][0]) + 1
            ydiff = abs(inp[i][1] - inp[j][1]) + 1
            
            p1 = max(p1, xdiff * ydiff)
            all_shapes.append((xdiff*ydiff, (inp[i], inp[j])))

    return p1

    
def p2(inp):
    global all_shapes
    inp = utils.split_and_strip(inp)
    inp = [tuple(map(int, x.split(','))) for x in inp]
    all_edges = utils.construct_edges(inp)
    sorted_x = sorted(x for x, y in inp)
    sorted_y = sorted(y for x, y in inp)

    all_shapes.sort(reverse=True, key=lambda x: x[0])
    
    p2 = 0
    for shape in all_shapes:
        area, (pt1, pt2) = shape
        valid = rectangle_in_shape(pt1, pt2, sorted_x, sorted_y, all_edges)
        if valid:
            p2 = area
            break        

    return p2


# this function is based off of the one in utils. But cache because speeed.
validity = {}
def optimized_point_in_shape(pt, max_x, min_y, edges):
    if pt in validity:
        return validity[pt] 
    
    ray_end = (max_x + 1, min_y - 1)
    ray = (pt, ray_end)

    intersection_points = set()
    for edge in edges:
        if pt == edge[0] or pt == edge[1]:
            return True
        intersection_point = utils.get_line_intersection(*ray, *edge)
        if intersection_point is not None:
            intersection_points.add(intersection_point)
        if intersection_point == pt: # edge point. 
            return True

    validity[pt] = (len(intersection_points) % 2) == 1
    return (len(intersection_points) % 2) == 1


def rectangle_in_shape(pt1, pt2, sorted_x, sorted_y, edges):
    # corners first
    corners = [(pt1[0], pt1[1]), (pt1[0], pt2[1]), (pt2[0], pt1[1]), (pt2[0], pt2[1])]
    for c in corners:
        if not optimized_point_in_shape(c, sorted_x[0], sorted_y[0], edges):
            return False
                
    # check the horizontal edges first
    ymin = min(pt1[1], pt2[1])
    ymax = max(pt1[1], pt2[1])
    xmin = min(pt1[0], pt2[0])
    xmax = max(pt1[0], pt2[0])

    horizontal_x_verts = sorted_x[sorted_x.index(xmin):sorted_x.index(xmax)+1]
    vertical_y_verts = sorted_y[sorted_y.index(ymin):sorted_y.index(ymax)+1]
    edge_1 = [(x, ymin) for x in horizontal_x_verts]
    edge_2 = [(x, ymax) for x in horizontal_x_verts]
    edge_3 = [(xmin, y) for y in vertical_y_verts]
    edge_4 = [(xmax, y) for y in vertical_y_verts]

    all_points = edge_1 + edge_2 + edge_3 + edge_4

    # random shuffle for serendipity
    import random
    random.seed(2025)
    random.shuffle(all_points)
    # ^ I mean really we should be doing this binary style but ehhh

    for pt in all_points:
        if not optimized_point_in_shape(pt, sorted_x[0], sorted_y[0], edges):
            return False
    return True