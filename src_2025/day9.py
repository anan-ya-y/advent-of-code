import utils

def main(inp):
    inp = utils.split_and_strip(inp)
    inp = [tuple(map(int, x.split(','))) for x in inp]
    all_edges = utils.construct_edges(inp)
    
    p1 = 0
    shapes = []
    for i in range(len(inp)):
        for j in range(i + 1, len(inp)):
            xdiff = abs(inp[i][0] - inp[j][0]) + 1
            ydiff = abs(inp[i][1] - inp[j][1]) + 1
            
            p1 = max(p1, xdiff * ydiff)
            shapes.append((xdiff*ydiff, (inp[i], inp[j])))

    shapes = sorted(shapes, reverse=True, key=lambda x: x[0])
    
    p2 = 0
    for shape in shapes:
        area, (pt1, pt2) = shape
        corners = [(pt1[0], pt1[1]), (pt1[0], pt2[1]), (pt2[0], pt1[1]), (pt2[0], pt2[1])]
        valid = all([utils.point_in_shape(c, inp, all_edges) for c in corners])
        if valid:
            p2 = area
            break        

    return p1, p2

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