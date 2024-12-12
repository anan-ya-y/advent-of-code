import utils
c = complex

space = {}
NEIGHBORS = [c(0, 1), c(0, -1), c(1, 0), c(-1, 0)]

def get_area(plot):
    return len(plot)

def get_perimeter(plot):
    perimeter = 0
    for pos in plot:
        for n in NEIGHBORS:
            if pos + n not in plot:
                perimeter += 1
    return perimeter

def get_nedges(plot):
    # get the horizontal and vertical edges of all exterior points
    # use a sweeping line.. but weird bc we're going in the gaps between coords.
    edge_lines = []

    for line in range(int(min([plot.real for plot in plot])-1), \
                   int(max([plot.real for plot in plot])+2)):
        plot_items_in_l = set([plot.imag for plot in plot if plot.real == line])
        plot_items_in_next = set([plot.imag for plot in plot if plot.real == line+1])
        edge_lines.append(list(plot_items_in_l.difference(plot_items_in_next)))
        edge_lines.append(list(plot_items_in_next.difference(plot_items_in_l)))

    for r in range(int(min([plot.imag for plot in plot])-1), \
                   int(max([plot.imag for plot in plot])+2)):
        plot_items_in_r = set([plot.real for plot in plot if plot.imag == r])
        plot_items_in_next = set([plot.real for plot in plot if plot.imag == r+1])
        edge_lines.append(list(plot_items_in_r.difference(plot_items_in_next)))
        edge_lines.append(list(plot_items_in_next.difference(plot_items_in_r)))
   
    nedges = 0
    for line in edge_lines:
        n = 0

        line = list(set(line)) # remove dupes
        line.sort()
        prev = float("-inf")
        for l in line:
            if l - prev != 1:
                n += 1
            prev = l
        nedges += n


    return nedges  

def main(input):
    global space
    space = utils.get_complex_space(input, "positions")
    # neighbor_generator: function that takes input (vertex, path to vertex) outputs list of all possible neighbors
    def space_neighbors(pos):
        v, _ = pos
        all_neighbors = [v + n for n in NEIGHBORS]
        return [n for n in all_neighbors if n in space and space[n] == space[v]]

    p1 = 0
    p2 = 0
    space_copy = space.copy()
    while len(space_copy) > 0:
        # pick a letter that's in space
        start_pos = list(space_copy.keys())[0]

        # find its reachable set
        garden_plot = utils.reachability_with_neighbor_generator(start_pos, space_neighbors)

        # get area
        area = get_area(garden_plot)

        # get perim
        perimeter = get_perimeter(garden_plot)

        # get nedges
        nedges = get_nedges(garden_plot)

        p1 += (area * perimeter)
        p2 += (area * nedges)

        # remove the whole set from space_copy
        for pos in garden_plot:
            del space_copy[pos]

    return p1, p2
