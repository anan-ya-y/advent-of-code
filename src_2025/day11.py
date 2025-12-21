import utils

def main(inp):
    inp = utils.split_and_strip(inp)
    directions = {}

    for line in inp:
        parts = line.split(":")
        prefix = parts[0].strip()
        suffix = parts[1].strip().split(" ")
        directions[prefix] = suffix

    def neighbors(v):
        vertex, _ = v
        neighbors = []
        if vertex not in directions:
            return []
        for n in directions[vertex]:
            neighbors.append(n)
        return neighbors
    
    p1 = utils.dfs_npaths(neighbors, "you", "out")



    backward_directions = {}
    for k, v in directions.items():
        for i in v:
            if i not in backward_directions:
                backward_directions[i] = []
            backward_directions[i].append(k)

    def backward_neighbors(v):
        vertex, _ = v
        neighbors = []
        if vertex not in backward_directions:
            return []
        for n in backward_directions[vertex]:
            neighbors.append(n)
        return neighbors

    out_to_fft = utils.dfs_npaths(backward_neighbors, "out", "fft")
    fft_to_dac = utils.dfs_npaths(backward_neighbors, "fft", "dac")
    dac_to_svr = utils.dfs_npaths(backward_neighbors, "dac", "svr")

    out_to_dac = utils.dfs_npaths(backward_neighbors, "out", "dac")
    dac_to_fft = utils.dfs_npaths(backward_neighbors, "dac", "fft")
    fft_to_svr = utils.dfs_npaths(backward_neighbors, "fft", "svr")

    p2 = (out_to_fft * fft_to_dac * dac_to_svr) +\
         (out_to_dac * dac_to_fft * fft_to_svr) 

    return p1, p2
            


