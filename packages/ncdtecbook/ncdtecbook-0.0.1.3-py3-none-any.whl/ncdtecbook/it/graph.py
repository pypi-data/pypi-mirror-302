from IPython.display import display, clear_output
import ipywidgets as widgets
import matplotlib.pyplot as plt
import networkx as nx
from collections import deque  # Import deque for efficient queue operations



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
    """Graph implementation using adjacency matrix"""
    
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
    """Graph implementation using adjacency list"""

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

    # Use the neighbors_of method to get the neighbors
    for neighbor, _ in graph.neighbors_of(start_vertex):
        if neighbor not in visited:
            dfs(graph, neighbor, visited)

    return visited



def bfs(graph, start_vertex):
    visited = []  # Initialize the visited list
    queue = deque([start_vertex])  # Use deque for efficient queue operations

    while queue:
        current_vertex = queue.popleft()  # Get the vertex at the front of the queue
        
        if current_vertex not in visited:  # If not visited
            visited.append(current_vertex)  # Mark as visited
            print(f"Visited: {current_vertex}")  # Display the visited vertex

            # Use the neighbors_of method to get the neighbors
            for neighbor, _ in graph.neighbors_of(current_vertex):
                if neighbor not in visited and neighbor not in queue:  # Avoid revisiting
                    queue.append(neighbor)  # Add to the queue for future exploration

    return visited  # Return the list of visited vertices


def example_dfs(graph, start_vertex):
    traversal_list = dfs(graph, start_vertex)
    interactive_traverse(graph, traversal_list)


def example_bfs(graph, start_vertex):
    traversal_list = bfs(graph, start_vertex)
    interactive_traverse(graph, traversal_list)

def interactive_traverse(graph, traversal_list):
    # Create an integer slider with a range from 0 to the length of the traversal list
    slider = widgets.IntSlider(
        value=0,  # Initial value
        min=0,  # Minimum value
        max=len(traversal_list),  # Maximum value, corresponding to the traversal steps
        step=1,  # Step size
        description='Step:',
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




if __name__ == '__main__':

    pass