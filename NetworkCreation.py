import pandas as pd
import networkx as nx
import dash_cytoscape as cyto
import datetime
import math


# node_id: string
# nodes_: list of nodes in format [{'data': {'id': '', 'label': ''}}]
# centre: tuple in form (x, y) to specify centre
# radius: radius of circle
# RETURN: list of nodes in radial layout, in format {'data': {'id': '', 'label': ''}, 'position': {'x': '', 'y': ''}}
def get_radial_layout(node_id, nodes_, centre, radius):
    nodes = [{'data': {'id': str(node_id), 'label': str(node_id)}, 'position': {'x': centre[0], 'y': centre[1]}, 'classes': 'selected'}]

    num_of_nodes = len(nodes_)
    angle_count = 0
    for i in range(num_of_nodes):
        if str(nodes_[i]['data']['id']) != str(node_id):
            # Orbiting
            angle = angle_count * (360 / num_of_nodes)
            position = (radius * math.cos(math.radians(angle)), radius * math.sin(math.radians(angle)))
            nodes += [{'data': {'id': str(nodes_[i]['data']['id']), 'label': str(nodes_[i]['data']['id'])}, 'position': {'x': position[0] + centre[0], 'y': position[1] + centre[1]}}]
            angle_count += 1

    return nodes


class NetworkCreator:
    dataset = None
    services = None
    full_cytoscape_nodes = None
    full_cytoscape_edges = None
    cytoscape_nodes = None
    cytoscape_edges = None
    networkx_nodes = None
    networkx_edges = None
    networkx_graph = None
    adjacency_matrix = None
    selected_node = None

    def __init__(self):
        pass

    # Creates the graph, argument is a clean dataset
    def initialise(self, dataset: pd.DataFrame):
        self.dataset = dataset
        self.services = self.get_services()
        self.create_adjacency_matrix()
        self.create_cytoscape_nodes_and_edges(all_nodes_and_edges=True, start_date=datetime.date(day=1, month=1, year=2017),
                                              end_date=datetime.date(day=1, month=1, year=2022))
        self.full_cytoscape_nodes = self.cytoscape_nodes
        self.full_cytoscape_edges = self.cytoscape_edges

        self.create_networkx_nodes_and_edges()

    def get_services(self):
        return self.dataset['service'].drop_duplicates().tolist()

    def create_adjacency_matrix(self):
        services = self.services

        # Create an empty 2x2 matrix containing lists of tuples
        # Tuple layout is (datetime.date(day, month, year), datetime.date(day, month, year))
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

                time_data = (datetime.date(day=day_start,
                                           month=month_start,
                                           year=year_start),
                             datetime.date(day=day_end,
                                           month=month_end,
                                           year=year_end))
                self.adjacency_matrix[index[0]][index[1]].append(time_data)

            prev_row += 1
            next_row += 1

    def create_cytoscape_nodes_and_edges(self, all_nodes_and_edges: bool, start_date: datetime.date, end_date: datetime.date):
        nodes = []
        edges = []
        active_services = [False for i in range(len(self.services))]

        services = self.services

        # Add necessary nodes
        if all_nodes_and_edges:
            # Add all nodes
            for i in range(len(services)):
                nodes += [{'data': {'id': str(services[i]), 'label': str(services[i])}}]

        for i in range(len(services)):
            for j in range(len(services)):
                if all_nodes_and_edges:
                    weight = len(self.adjacency_matrix[i][j])
                    if weight > 0:
                        edge = [{'data': {'source': services[i], 'target': services[j],
                                          'weight': weight}}]
                        edges += edge

                else:
                    instances = self.adjacency_matrix[i][j]
                    if len(instances) > 0:
                        num_of_edges = 0
                        for k in range(len(instances)):
                            instance = instances[k]
                            instance_start_date = instance[0]
                            instance_end_date = instance[1]

                            if start_date <= instance_start_date <= end_date or start_date <= instance_end_date <= end_date:
                                num_of_edges += 1

                        if num_of_edges > 0:
                            active_services[i] = True
                            active_services[j] = True

                            edge = [{'data': {'source': services[i], 'target': services[j],
                                              'weight': num_of_edges}}]
                            edges += edge

        if not all_nodes_and_edges:
            for a in range(len(active_services)):
                if active_services[a]:
                    nodes += [{'data': {'id': str(services[a]), 'label': str(services[a])}}]

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
                              style={'width': '25vw', 'height': '25vw', 'background-color': 'white', 'border': 'solid'}
                              )

    def set_selected_node(self, selected_node):
        self.selected_node = selected_node

    def get_specific_node_cytoscape_graph(self, graph_name: str, in_or_out: str):
        elements = self.get_specific_node_elements(in_or_out)

        return cyto.Cytoscape(id=graph_name,
                              elements=elements,
                              layout={
                                  'name': 'preset'
                              },
                              stylesheet=[
                                  {
                                      'selector': 'node',
                                      'style': {
                                          'label': 'data(label)'
                                      }
                                  },
                                  {
                                      'selector': 'edge',
                                      'style': {
                                          'label': 'data(weight)',
                                          'target-arrow-shape': 'triangle',
                                          'target-arrow-color': 'red',
                                          'curve-style': 'bezier'
                                      }

                                  },
                                  {
                                      'selector': '.selected',
                                      'style': {
                                          'background-color': 'green'
                                      }


                                  },


                              ],
                              style={
                                  'width': '25vw',
                                  'height': '25vw',
                                  'background-color': 'white',
                                  'border': 'solid'
                              }
                              )

    def get_specific_node_elements(self, in_or_out: str):
        node_id = self.selected_node
        if node_id is None:
            return []

        nodes = self.cytoscape_nodes
        edges = self.cytoscape_edges

        selected_nodes = [{'data': {'id': str(node_id), 'label': str(node_id)}}]
        selected_edges = []

        for i in range(len(edges)):
            if edges[i]['data']['source'] == node_id and in_or_out == 'out':
                selected_edges += [edges[i]]
                selected_nodes += [{'data': {'id': edges[i]['data']['target'], 'label': edges[i]['data']['target']}}]
            if edges[i]['data']['target'] == node_id and in_or_out == 'in':
                selected_edges += [edges[i]]
                selected_nodes += [{'data': {'id': edges[i]['data']['source'], 'label': edges[i]['data']['source']}}]

        return get_radial_layout(node_id, selected_nodes, (0, 0), 250) + selected_edges





    def create_networkx_nodes_and_edges(self):
        self.networkx_graph = nx.Graph()
        nodes = []
        edges = []

    def get_graphs(self, start_date, end_date):
        pass
