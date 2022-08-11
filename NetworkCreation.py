import pandas as pd
import networkx as nx
import dash_cytoscape as cyto


class NetworkCreator:
    dataset = None
    services = None
    cytoscape_nodes = None
    cytoscape_edges = None
    networkx_nodes = None
    networkx_edges = None
    networkx_graph = None
    matrix = None

    def __init__(self):
        pass

    # Creates the graph, argument is a clean dataset
    def initialise(self, dataset: pd.DataFrame):
        self.dataset = dataset
        self.services = self.get_services()
        self.create_cytoscape_nodes_and_edges()
        self.create_networkx_nodes_and_edges()

    def get_services(self):
        return self.dataset['service'].drop_duplicates().tolist()

    def create_cytoscape_nodes_and_edges(self):
        nodes = []
        edges = []
        # Add the nodes
        services = self.services
        for i in range(len(services)):
            node = {'data': {'id': str(services[i]), 'label': str(services[i])}}
            nodes.append(node)

        # Add the edges
        # Create an empty 2x2 matrix
        self.matrix = [[0 for i in range(len(services))] for j in range(len(services))]
        num_of_rows = len(self.dataset)
        prev_row = 0
        next_row = 1
        for i in range(num_of_rows - 1):
            prev_row_id = self.dataset.loc[prev_row]['id']
            next_row_id = self.dataset.loc[next_row]['id']
            prev_row_service = self.dataset.loc[prev_row]['service']
            next_row_service = self.dataset.loc[next_row]['service']
            if next_row_id == prev_row_id:
             # same patient
                index = [0, 0]
                for j in range(len(services)):
                    if services[j] == prev_row_service:
                        index[0] = j
                    if services[j] == next_row_service:
                        index[1] = j
                self.matrix[index[0]][index[1]] += 1

            prev_row += 1
            next_row += 1

        for i in range(len(services)):
            for j in range(len(services)):
                if self.matrix[i][j] > 0:
                    edge = {'data': {'source': services[i], 'target': services[j], 'weight': self.matrix[i][j]}}
                    edges.append(edge)

        self.cytoscape_nodes = nodes
        self.cytoscape_edges = edges

    def get_cytoscape_nodes(self):
        return self.cytoscape_nodes

    def get_cytoscape_edges(self):
        return self.cytoscape_edges

    def get_cytoscape_graph(self, graph_name: str):
        return cyto.Cytoscape(id=graph_name,
                              elements=self.cytoscape_nodes + self.cytoscape_edges,
                              layout={
                                'name': 'cose',
                                'gravity': '0.1',
                                'idealEdgeLength': '100',
                                'nodeRepulsion': '400'
                              },
                              stylesheet=[
                               {
                                   'selector': 'edge',
                                   'style': {
                                       'target-arrow-shape': 'triangle',
                                       'target-arrow-color': 'black',
                                       'curve-style': 'bezier'
                                   }
                               },
                               {
                                   'selector': 'node',
                                   'style': {
                                       'label': 'data(label)'
                                   }

                               }
                              ],
                              style={'width': '50vw', 'height': '50vw', 'background-color': 'white'}
                              )

    def create_networkx_nodes_and_edges(self):
        self.networkx_graph = nx.Graph()
        nodes = []
        edges = []



