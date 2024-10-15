import networkx as nx
import matplotlib.pyplot as plt

def createGraph(txt):
    g = nx.Graph()
    nodeIndex = 0
    with open(txt, 'r') as file:
        lines = file.readlines()
        metadata = lines[0].strip().split()
        x = int(metadata[0])
        y = int(metadata[1])

        z = int(metadata[2]) if len(metadata) > 2 else 1

        for depth in range(z):
            for row in range(y):
                line = lines[1 + depth * y + row].strip().split()
                for col in range(x):
                    currentColor = 'white'
                    if line[col] == '0':
                        currentColor = 'black'
                    g.add_node(nodeIndex, color=currentColor)

                    if row > 0:
                        g.add_edge(nodeIndex, nodeIndex - x, weight=1)  # Vertical edge (up)
                    if col > 0:
                        g.add_edge(nodeIndex, nodeIndex - 1, weight=1)  # Horizontal edge (left)

                    # Diagonal edges
                    if row > 0 and col > 0:  # Top-left diagonal
                        g.add_edge(nodeIndex, nodeIndex - x - 1, weight=1)
                    if row > 0 and col < x - 1:  # Top-right diagonal
                        g.add_edge(nodeIndex, nodeIndex - x + 1, weight=1)

                    # Diagonal edges for bottom-right diagonal if working on multiple layers (optional)
                    if depth > 0:
                        g.add_edge(nodeIndex, nodeIndex - (x * y), weight=1)  # Between layers

                    nodeIndex += 1

    blueNode = nodeIndex
    g.add_node(blueNode, color='blue')
    nodeIndex += 1
    redNode = nodeIndex
    g.add_node(redNode, color='red')

    # **Connect blue node to all black nodes in the bottom row of each layer (y = last row)**
    for depth in range(z):
        bottomRowStart = (depth * x * y) + (y - 1) * x
        for i in range(bottomRowStart, bottomRowStart + x):
            if g.nodes[i]['color'] == 'white':
                g.add_edge(redNode, i, weight=1)

    # **Connect red node to all white nodes in the top row of each layer (y = first row)**
    for depth in range(z):
        topRowStart = depth * x * y
        for i in range(topRowStart, topRowStart + x):
            if g.nodes[i]['color'] == 'black':
                g.add_edge(blueNode, i, weight=1)

    return g


def filterGraph(inputG):
    filtered_edges = []

    # Include connections between black-black, white-white, blue-black, and red-white nodes
    for u, v, d in inputG.edges(data=True):
        u_color = inputG.nodes[u]['color']
        v_color = inputG.nodes[v]['color']

        # Filter the edges based on colors
        if (u_color == 'black' and v_color == 'black') or \
           (u_color == 'white' and v_color == 'white') or \
           (u_color == 'blue' and v_color == 'black') or \
            (u_color == 'black' and v_color == 'blue') or \
            (u_color == 'red' and v_color == 'white') or \
           (u_color == 'black' and v_color == 'red'):  # Check reverse for red-black
            filtered_edges.append((u, v))

    # Create the filtered graph
    H = nx.Graph()
    H.add_nodes_from(inputG.nodes(data=True))
    H.add_edges_from(filtered_edges)

    return H



def bfs(filteredGraph, blue_node):
    bfs_results = {}
    shortest_paths = nx.single_source_shortest_path(filteredGraph, blue_node)

    for node in shortest_paths:
        if filteredGraph.nodes[node]['color'] == 'black':
            bfs_results[node] = shortest_paths[node]

    return bfs_results


def plotGraph(g):
    pos = nx.spring_layout(g)

    node_colors = [g.nodes[node]['color'] for node in g.nodes()]

    nx.draw(g, pos, with_labels=False, node_color=node_colors, node_size=500, font_size=10)

    labels = {node: str(node) for node in g.nodes()}

    for node, label in labels.items():
        # If the node is black, set the font color to white; otherwise, black
        font_color = 'white' if g.nodes[node]['color'] == 'black' else 'black'
        nx.draw_networkx_labels(g, pos, labels={node: label}, font_color=font_color)

    plt.show()
