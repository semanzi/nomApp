import pandas as pd
import networkx as nx
import dash_cytoscape as cyto
import datetime


class NetworkCreator:
    dataset = None
    services = None
    cytoscape_nodes = None
    cytoscape_edges = None
    networkx_nodes = None
    networkx_edges = None
    networkx_graph = None
    adjacency_matrix = None

    def __init__(self):
        pass

    # Creates the graph, argument is a clean dataset
    def initialise(self, dataset: pd.DataFrame):
        self.dataset = dataset
        self.services = self.get_services()
        self.create_adjacency_matrix()
        self.create_cytoscape_edges(all_edges=True, start_date=datetime.date(day=1, month=1, year=2017), end_date=datetime.date(day=1, month=1, year=2022))
        self.create_networkx_nodes_and_edges()

    def get_services(self):
        return self.dataset['service'].drop_duplicates().tolist()

    def create_adjacency_matrix(self):
        nodes = []
        # Add the nodes
        services = self.services
        for i in range(len(services)):
            node = {'data': {'id': str(services[i]), 'label': str(services[i])}}
            nodes.append(node)

        self.cytoscape_nodes = nodes

        # Create an empty 2x2 matrix
        # (day_start, month_start, year_start, day_end, month_end, year_end)

        self.adjacency_matrix = [[[] for i in range(len(services))] for j in range(len(services))]
        num_of_rows = len(self.dataset)
        prev_row = 0
        next_row = 1
        for i in range(num_of_rows - 1):
            prev_row_id = self.dataset.loc[prev_row]['id']
            next_row_id = self.dataset.loc[next_row]['id']
            prev_row_service = self.dataset.loc[prev_row]['service']
            next_row_service = self.dataset.loc[next_row]['service']
            prev_row_start_time = str(self.dataset.loc[prev_row]['referraldate'])
            next_row_end_time = str(self.dataset.loc[next_row]['dischargedate'])
            if next_row_id == prev_row_id:
                # same patient
                index = [0, 0]
                for j in range(len(services)):
                    if services[j] == prev_row_service:
                        index[0] = j
                    if services[j] == next_row_service:
                        index[1] = j

                day_start = int(prev_row_start_time.split('/')[0])
                month_start = int(prev_row_start_time.split('/')[1])
                year_start = int(prev_row_start_time.split('/')[2])
                if next_row_end_time != "nan":
                    day_end = int(next_row_end_time.split('/')[0])
                    month_end = int(next_row_end_time.split('/')[1])
                    year_end = int(next_row_end_time.split('/')[2])
                else:
                    day_end = 1
                    month_end = 1
                    year_end = 9999

                time_data = (day_start, month_start, year_start, day_end, month_end, year_end)
                self.adjacency_matrix[index[0]][index[1]].append(time_data)

            prev_row += 1
            next_row += 1

    def create_cytoscape_edges(self, all_edges: bool, start_date: datetime.date, end_date: datetime.date):
        edges = []
        services = self.services

        for i in range(len(services)):
            for j in range(len(services)):
                if all_edges:
                    weight = len(self.adjacency_matrix[i][j])
                    if weight > 0:
                        edge = {'data': {'source': services[i], 'target': services[j],
                                         'weight': weight}}
                        edges.append(edge)
                else:
                    instances = self.adjacency_matrix[i][j]
                    if len(instances) > 0:
                        num_of_edges = 0
                        for k in range(len(instances)):
                            instance = instances[k]
                            instance_start_date = datetime.date(day=instance[0], month=instance[1], year=instance[2])
                            instance_end_date = datetime.date(day=instance[3], month=instance[4], year=instance[5])
                            if start_date <= instance_start_date <= end_date or start_date <= instance_end_date <= end_date:
                                num_of_edges += 1

                        if num_of_edges > 0:
                            edge = {'data': {'source': services[i], 'target': services[j],
                                             'weight': num_of_edges}}
                            edges.append(edge)

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
                                'gravity': '0.01',
                                'idealEdgeLength': '100',
                                'nodeRepulsion': '800'
                              },
                              stylesheet=[
                               {
                                   'selector': 'edge',
                                   'style': {
                                       'target-arrow-shape': 'triangle',
                                       'curve-style': 'bezier',
                                       'line-color': 'red',
                                       'width': 'data(weight)'
                                   }
                               },
                               {
                                   'selector': 'node',
                                   'style': {
                                       'label': 'data(label)'
                                   }

                               },
                               {
                                   'selector': '[weight < 3]',
                                   'style': {
                                       'line-color': 'green'
                                   }


                               }

                              ],
                              style={'width': '25vw', 'height': '25vw', 'background-color': 'white'}
                              )

    def create_networkx_nodes_and_edges(self):
        self.networkx_graph = nx.Graph()
        nodes = []
        edges = []


    def get_graphs(self, start_date, end_date):
        pass