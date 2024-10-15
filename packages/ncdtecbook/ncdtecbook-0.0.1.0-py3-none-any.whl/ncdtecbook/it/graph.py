import matplotlib.pyplot as plt
import networkx as nx


def display_graph(graph):
    G = nx.DiGraph() if graph.is_directed else nx.Graph()

    # Add nodes and edges
    for i, vertex in enumerate(graph.vertices):
        G.add_node(vertex)
    
    for i, row in enumerate(graph.adj_matrix):
        for j, weight in enumerate(row):
            if weight != 0:
                G.add_edge(graph.vertices[i], graph.vertices[j], weight=weight)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=700)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    
    plt.show()


def p():
    print('version 01')


if __name__ == '__main__':
    display_graph([])