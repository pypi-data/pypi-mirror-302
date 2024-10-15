import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx


def _validate_edges(edges):
    result = []
    for u, v, *r in edges:
        w = r[0] if len(r) > 0 else 1
        edge = (u, v, w)
        result.append(edge)
    return result


def _extract_vertices(edges):
    s = set()
    for u, v, *r in edges:
        s.add(u)
        s.add(v)
    return list(s)



class GraphM:
    
    def __init__(self, edges, is_directed=False, vertices = None):
        self.edges = _validate_edges(edges)
        self.vertices = list(vertices) if vertices else _extract_vertices(edges)
        self.n = len(self.vertices)
        self.is_directed= is_directed

        # Create an adjacency matrix initialized with zeros
        self.adj_matrix = [[0] * self.n for _ in range(self.n)]

        # Add edges
        for edge in self.edges:
            vertex1, vertex2, weight = edge
            self.add_edge(vertex1, vertex2, weight)
        
            self.visited = set()


    def visit(self,vertex):
        if vertex in self.vertices:
            self.visited.add(vertex)
    

    def add_edge(self, vertex1, vertex2, weight):
        i = self.vertices.index(vertex1)
        j = self.vertices.index(vertex2)
        self.adj_matrix[i][j] = weight
        if not self.is_directed:
          self.adj_matrix[j][i] = weight 
    

    def neighbors_of(self, vertex):
        """ Returns the list of neighbors of the given vertex. """
        if vertex not in self.vertices:
            raise ValueError(f"Vertex '{vertex}' not found in the graph.")
        
        i = self.vertices.index(vertex)
        neighbors = []
        for j in range(self.n):
            if self.adj_matrix[i][j] != 0:  # If there's an edge
                neighbors.append((self.vertices[j], self.adj_matrix[i][j]))
        
        return neighbors
    
    def __repr__(self):
        result = f'\t   {"  ".join(self.vertices)}'
        for i, row in enumerate(self.adj_matrix):
            result+= f'\n\t{self.vertices[i]} {row}'
        return result + '\n'
    
    def __str__(self):
        return self.__repr__()
    

class GraphL:
    
    def __init__(self, edges, is_directed=False, vertices = None):

        self.edges = _validate_edges(edges)
        self.vertices = list(vertices) if vertices else _extract_vertices(edges)
        self.n = len(self.vertices)
        self.is_directed= is_directed

        self.adj_list = {vertex: [] for vertex in self.vertices}  # empty adjacency list for each vertex

        # Add edges
        for edge in self.edges:
            vertex1, vertex2, weight = edge
            self.add_edge(vertex1, vertex2, weight)

        self.visited = set()


    def visit(self,vertex):
        if vertex in self.vertices:
            self.visited.add(vertex)
            
    def add_edge(self, vertex1, vertex2, weight):

        self.adj_list[vertex1].append((vertex2, weight))
        if not self.is_directed:
          self.adj_list[vertex2].append((vertex1, weight))  # For undirected graph; remove for directed graph

    def __repr__(self):
        result = ""
        for vertex, edges in self.adj_list.items():
            result+= f"{vertex}: {edges}\n"
        return result
    
    def __str__(self):
        return self.__repr__()
    
    
    def neighbors_of(self, vertex):
        """ Returns the list of neighbors of the given vertex. """
        if vertex not in self.adj_list:
            raise ValueError(f"Vertex '{vertex}' not found in the graph.")
        return self.adj_list[vertex]        


    

def display_graph(g):
    t = g.__class__.__name__ 
    print(f'type = {t}')
    if t == 'GraphM':
        display_graphM(g)
    elif    t == 'GraphL':
        display_graphL(g)
    else:
        print(f'g is not of graph types')

def display_graphL(graph):

    G = nx.DiGraph() if graph.is_directed else nx.Graph()

    # Add nodes and edges
    for vertex in graph.adj_list:
        G.add_node(vertex)
        
    for vertex, neighbors in graph.adj_list.items():
        for neighbor, weight in neighbors:
            G.add_edge(vertex, neighbor, weight=weight)

    # Use spring layout with a fixed seed to ensure consistent layout
    pos = nx.spring_layout(G, seed=42)

    # Determine colors for each node based on whether it's visited
    node_colors = []
    for vertex in graph.vertices:
        if vertex in graph.visited:
            node_colors.append('orange')  # Visited nodes in orange
        else:
            node_colors.append('lightblue')  # Not visited nodes in light blue

    # Plot the graph
    nx.draw(G, pos, with_labels=True, node_color=node_colors, font_weight='bold', node_size=700)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.show()  # Display the graph
    
def display_graphM(graph):
    G = nx.DiGraph() if graph.is_directed else nx.Graph()

    # Add nodes and edges
    for i, vertex in enumerate(graph.vertices):
        G.add_node(vertex)
    
    for i, row in enumerate(graph.adj_matrix):
        for j, weight in enumerate(row):
            if weight != 0:
                G.add_edge(graph.vertices[i], graph.vertices[j], weight=weight)

    # Determine colors for each node based on whether it's visited
    node_colors = []
    for vertex in graph.vertices:
        if vertex in graph.visited:
            node_colors.append('orange')  # Visited nodes in orange
        else:
            node_colors.append('lightblue')  # Not visited nodes in light blue

    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color=node_colors, font_weight='bold', node_size=700)

    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
  
    plt.show()  # Display the graph
    

def dfs(graph, start_vertex, visited=None):
    if visited is None:
        visited = []  # Initialize the visited set if it's the first call

    # Mark the start vertex as visited and display it
    visited.append(start_vertex)
    print(f"Visited: {start_vertex}")

    # Use the neighbors_of method to get the neighbors
    for neighbor, _ in graph.neighbors_of(start_vertex):
        if neighbor not in visited:
            dfs(graph, neighbor, visited)

    return visited


import ipywidgets as widgets
from IPython.display import display, clear_output



def example_dfs(graph, start_vertex):


    traversal_list = dfs(graph, start_vertex)
    interactive_dfs(graph, traversal_list)



def interactive_dfs(graph, traversal_list):
    # Create an integer slider with a range from 0 to the length of the traversal list
    slider = widgets.IntSlider(
        value=0,  # Initial value
        min=0,  # Minimum value
        max=len(traversal_list),  # Maximum value, corresponding to the traversal steps
        step=1,  # Step size
        description='Traversal Step:',
        continuous_update=False  # Update only when the user releases the slider
    )

    def update_graph(change):
        # Clear the visited set before updating
        graph.visited = set()

        # Add vertices up to the current step
        for i in range(slider.value):
            graph.visited.add(traversal_list[i])

        clear_output(wait=True)

        # Display the updated graph
        display(slider)
        display_graph(graph)

    # Attach the slider update to the graph visualization
    slider.observe(update_graph, names='value')

    # Display the slider and initial graph
    display(slider)
    update_graph(None)  # Display the initial state of the graph



def display_graphM2(graph):

    G = nx.DiGraph() if graph.is_directed else nx.Graph()

    # Add nodes and edges
    for i, vertex in enumerate(graph.vertices):
        G.add_node(vertex)
    
    for i, row in enumerate(graph.adj_matrix):
        for j, weight in enumerate(row):
            if weight != 0:
                G.add_edge(graph.vertices[i], graph.vertices[j], weight=weight)

    # Determine colors for each node based on whether it's visited
    node_colors = []
    for vertex in graph.vertices:
        if vertex in graph.visited:
            node_colors.append('orange')  # Visited nodes in orange
        else:
            node_colors.append('lightblue')  # Not visited nodes in light blue

    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=True, node_color=node_colors, font_weight='bold', node_size=700)

    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

    plt.ion()  # Enable interactive mode
    fig = plt.gcf()  # Get current figure
    plt.show()  # Display the graph
    return fig  # Return the figure referenc

def interactive_dfs2(graph, traversal_list):
    # Create an integer slider with a range from 0 to the length of the traversal list
    slider = widgets.IntSlider(
        value=0,  # Initial value
        min=0,  # Minimum value
        max=len(traversal_list),  # Maximum value, corresponding to the traversal steps
        step=1,  # Step size
        description='Traversal Step:',
        continuous_update=False  # Update only when the user releases the slider
    )

    fig = None  # Initialize figure reference

    def update_graph(change):
        nonlocal fig  # Reference the outer fig variable

        # Clear the previous plot if it exists
        if fig is not None:
            plt.clf(fig)

        # Clear the visited set before updating
        graph.visited = set()

        # Add vertices up to the current step
        for i in range(slider.value):
            graph.visited.add(traversal_list[i])

        # Display the slider and updated graph
        display(slider)
        fig = display_graph(graph)  # Store the new figure reference

    # Attach the slider update to the graph visualization
    slider.observe(update_graph, names='value')

    # Display the slider and initial graph
    display(slider)
    update_graph(None)  # Display the initial state of the graph


if __name__ == '__main__':
    edges = [("A", "B",4), ("D", "A", 5), ("B", "D", 1), ("B", "C", 2), ("E", "D", 10), ("C", "E", 8)]
    g = GraphL(edges, is_directed=False)    
    print(g.neighbors_of('A'))
    print(dfs(g, 'A'))


        # Example usage
    edges = [('A', 'B', 2), ('A', 'C', 1), ('B', 'C', 3), ('C', 'D', 2)]
    g = GraphM(edges, is_directed=False)

    # Perform DFS and get the traversal list
    traversal_list = dfs(g, 'A')

    # Create an interactive slider to update the visited nodes and display the graph
    interactive_dfs(g, traversal_list)