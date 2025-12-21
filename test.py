import matplotlib.pyplot as plt

edge_vertices = [(7, 1), (11, 1), (11, 7), (9, 7), (9, 5), (2, 5), (2, 3), (7, 3)]

plt.figure()
for i in range(len(edge_vertices)):
    start = edge_vertices[i]
    end = edge_vertices[(i + 1) % len(edge_vertices)]
    plt.plot([start[0], end[0]], [start[1], end[1]], 'b-')

red_line = [(2, 7), (12, 0)]
plt.plot([red_line[0][0], red_line[1][0]], [red_line[0][1], red_line[1][1]], 'r-')

plt.show()