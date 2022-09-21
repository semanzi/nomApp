import pandas as pd
import networkx as nx
import dash_cytoscape as cyto
from datetime import date, timedelta
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
            angle = angle_count * (360 / (num_of_nodes - 1))
            position = (radius * math.cos(math.radians(angle)), radius * math.sin(math.radians(angle)))
            nodes += [{'data': {'id': str(nodes_[i]['data']['id']), 'label': str(nodes_[i]['data']['id'])}, 'position': {'x': position[0] + centre[0], 'y': position[1] + centre[1]}, 'classes': 'non-selected'}]
            angle_count += 1

    return nodes


class Network:
    __dataset = None
    __services = None
    __cytoscape_nodes = None
    __cytoscape_edges = None
    __networkx_graph = None
    __adjacency_matrix = None
    __selected_node = None

    def __init__(self):
        pass

    # Creates the graph, argument is a clean dataset
    def initialise(self, dataset: pd.DataFrame):
        self.__dataset = dataset
        self.__services = self.__get_services()
        self.__create_adjacency_matrix()
        self.create_cytoscape_nodes_and_edges(all_nodes_and_edges=True,
                                              start_date=date(day=1, month=1, year=2000),
                                              end_date=date(day=1, month=1, year=2000))
        self.__create_networkx_nodes_and_edges()

    def __get_services(self):
        return self.__dataset['service'].drop_duplicates().tolist()

    def __create_adjacency_matrix(self):
        services = self.__services

        # Create an empty 2x2 matrix containing lists of tuples
        # Tuple layout is (datetime.date(day, month, year), datetime.date(day, month, year))
        self.__adjacency_matrix = [[[] for i in range(len(services))] for j in range(len(services))]
        num_of_rows = len(self.__dataset)
        prev_row = 0
        next_row = 1
        for i in range(num_of_rows - 1):
            prev_row_id = self.__dataset.loc[prev_row]['id']
            next_row_id = self.__dataset.loc[next_row]['id']
            prev_row_service = self.__dataset.loc[prev_row]['service']
            next_row_service = self.__dataset.loc[next_row]['service']
            prev_row_start_time = str(self.__dataset.loc[prev_row]['referraldate'])
            next_row_end_time = str(self.__dataset.loc[next_row]['dischargedate'])
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

                time_data = (date(day=day_start,
                                  month=month_start,
                                  year=year_start),
                             date(day=day_end,
                                  month=month_end,
                                  year=year_end))
                self.__adjacency_matrix[index[0]][index[1]].append(time_data)

            prev_row += 1
            next_row += 1

    def create_cytoscape_nodes_and_edges(self, all_nodes_and_edges: bool, start_date: date, end_date: date):
        nodes = []
        edges = []
        active_services = [False for i in range(len(self.__services))]

        services = self.__services

        # Add necessary nodes
        if all_nodes_and_edges:
            # Add all nodes
            for i in range(len(services)):
                nodes += [{'data': {'id': str(services[i]), 'label': str(services[i])}}]

        for i in range(len(services)):
            for j in range(len(services)):
                if all_nodes_and_edges:
                    weight = len(self.__adjacency_matrix[i][j])
                    if weight > 0:
                        edge = [{'data': {'source': services[i], 'target': services[j],
                                          'weight': weight}}]
                        edges += edge

                else:
                    instances = self.__adjacency_matrix[i][j]
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

        self.__cytoscape_nodes = nodes
        self.__cytoscape_edges = edges
        self.__create_networkx_nodes_and_edges()

    def get_cytoscape_nodes(self):
        return self.__cytoscape_nodes

    def get_cytoscape_edges(self):
        return self.__cytoscape_edges

    def get_cytoscape_graph(self, graph_name: str):

        return cyto.Cytoscape(id=graph_name,
                              elements=self.__cytoscape_nodes + self.__cytoscape_edges,
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
                              style={'position': 'absolute', 'left': '1%', 'width': '50%', 'height': '90%', 'margin-top': '20px', 'background-color': 'white', 'border': 'solid', }
                              )

    def set_selected_node(self, selected_node: str):
        self.__selected_node = selected_node

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
                                  'left': '52%',
                                  'width': '33%',
                                  'height': '90%',
                                  'margin-top': '20px',
                                  'background-color': 'white',
                                  'border': 'solid',
                                  'position': 'absolute'
                              }
                              )

    def get_specific_node_elements(self, in_or_out: str):
        node_id = self.__selected_node
        if node_id is None:
            return []

        edges = self.__cytoscape_edges

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

##### NETWORK X #####


    def __create_networkx_nodes_and_edges(self):
        self.__networkx_graph = nx.DiGraph()

        # Add nodes and edges from cytoscape
        for i in range(len(self.__cytoscape_nodes)):
            self.__networkx_graph.add_node(self.__cytoscape_nodes[i]['data']['id'])
        for i in range(len(self.__cytoscape_edges)):
            self.__networkx_graph.add_edge(self.__cytoscape_edges[i]['data']['source'],
                                           self.__cytoscape_edges[i]['data']['target'],
                                           weight=int(self.__cytoscape_edges[i]['data']['weight'])
                                           )


##### GRAPH ITERATION #####

    # start_date -> The first date within range of time to view
    # end_date -> The final date within range of time to view
    # slice_resolution -> Year(1), Month(2) or Day(3)
    # slice_size -> The size of the period of time to view as 1 piece
    # metric_scope -> Whether to focus on the graph as a whole, or a specific node (value 1 is whole graph, value 2 is selected node)
    # metric -> The metric to view
    # Whole graph metrics: Num of nodes(1), Num of edges(2), Average degree(3), Graph density(4), Network modularity(5)
    # Specific node metrics: Degree(1), Betweenness(2), Modularity(3), Eigenvector(4)

    def iterate(self, start_date: date, end_date: date, slice_resolution: int, slice_size: int, metric_scope: int, metric: int):
        # Need to iterate through adjacency matrix
        # Create networkX graph for each time slice
        # Graph networkX stats

        matrix = self.__adjacency_matrix

        node_number = None

        for i in range(len(self.__services)):
            if self.__services[i] == self.__selected_node:
                node_number = i

        data = []

        if slice_resolution == 1:
            start_year = start_date.year
            end_year = end_date.year
            num_of_years = end_year - start_year + 1

            # Iterate over years
            for y in range(num_of_years):
                current_year = start_year + y
                temp_graph = nx.Graph()

                # Iterate over adjacency matrix
                for i in range(len(self.__services)):
                    for j in range(len(self.__services)):
                        instances_of_edge = matrix[i][j]
                        # Iterate through instances of edges
                        num_of_active_patients = 0
                        for k in range(len(instances_of_edge)):
                            # Is current year within two dates
                            is_between = instances_of_edge[k][0].year <= current_year <= instances_of_edge[k][1].year
                            if is_between:
                                temp_graph.add_node(i)
                                temp_graph.add_node(j)
                                num_of_active_patients += 1
                        if num_of_active_patients > 0:
                            temp_graph.add_edge(i, j, weight=num_of_active_patients)

                # find metrics
                centrality = None
                if metric_scope == 1:
                    # Whole graph
                    if metric == 1:
                        data += [nx.number_of_nodes(temp_graph)]
                    if metric == 2:
                        data += [nx.number_of_edges(temp_graph)]
                    if metric == 3:
                        data += [nx.average_degree_connectivity(temp_graph)]
                    if metric == 4:
                        data += [nx.density(temp_graph)]
                    if metric == 5:
                        pass

                elif metric_scope == 2:
                    # Specific node
                    if metric == 1:
                        centrality = nx.degree_centrality(temp_graph)
                    if metric == 2:
                        centrality = nx.betweenness_centrality(temp_graph)
                    if metric == 3:
                        pass
                    if metric == 4:
                        centrality = nx.eigenvector_centrality(temp_graph)

                    if centrality.__contains__(node_number):
                        data += [centrality[node_number]]
                    else:
                        data += [0]
                else:
                    print("INVALID VALUE FOR metric_scope IN ITERATE METHOD, VALUE SHOULD BE 1 OR 2")

            return data

        if slice_resolution == 2:
            current_year = start_date.year
            current_month = start_date.month

            # Iterate over months
            while not (current_year == end_date.year and current_month == end_date.month + 1):
                temp_graph = nx.Graph()

                # Iterate over adjacency matrix
                for i in range(len(self.__services)):
                    for j in range(len(self.__services)):
                        instances_of_edge = matrix[i][j]
                        # Iterate through instances of edges
                        num_of_active_patients = 0
                        for k in range(len(instances_of_edge)):
                            # Is current month within two dates
                            is_between1 = date(day=15, month=current_month, year=current_year) >= date(day=1, month=instances_of_edge[k][0].month, year=instances_of_edge[k][0].year)
                            is_between2 = date(day=15, month=current_month, year=current_year) <= date(day=28, month=instances_of_edge[k][1].month, year=instances_of_edge[k][1].year)
                            if is_between1 and is_between2:
                                temp_graph.add_node(i)
                                temp_graph.add_node(j)
                                num_of_active_patients += 1
                        if num_of_active_patients > 0:
                            temp_graph.add_edge(i, j, weight=num_of_active_patients)

                # find metrics
                centrality = None
                if metric_scope == 1:
                    # Whole graph
                    if metric == 1:
                        data += [nx.number_of_nodes(temp_graph)]
                    if metric == 2:
                        data += [nx.number_of_edges(temp_graph)]
                    if metric == 3:
                        data += [nx.average_degree_connectivity(temp_graph)]
                    if metric == 4:
                        data += [nx.density(temp_graph)]
                    if metric == 5:
                        pass

                elif metric_scope == 2:
                    # Specific node
                    if metric == 1:
                        centrality = nx.degree_centrality(temp_graph)
                    if metric == 2:
                        centrality = nx.betweenness_centrality(temp_graph)
                    if metric == 3:
                        pass
                    if metric == 4:
                        centrality = nx.eigenvector_centrality(temp_graph)

                    if centrality.__contains__(node_number):
                        data += [centrality[node_number]]
                    else:
                        data += [0]
                else:
                    print("INVALID VALUE FOR metric_scope IN ITERATE METHOD, VALUE SHOULD BE 1 OR 2")

                current_month += 1
                if current_month > 12:
                    current_month = 1
                    current_year += 1

            return data

        if slice_resolution == 3:
            num_of_days = (end_date - start_date).days

            # Iterate through days
            for d in range(num_of_days):
                current_day = start_date + timedelta(days=d)

                temp_graph = nx.Graph()

                # Iterate over adjacency matrix
                for i in range(len(self.__services)):
                    for j in range(len(self.__services)):
                        instances_of_edge = matrix[i][j]
                        num_of_active_patients = 0

                        for k in range(len(instances_of_edge)):
                            is_between = instances_of_edge[k][0] <= current_day <= instances_of_edge[k][1]
                            if is_between:
                                temp_graph.add_node(i)
                                temp_graph.add_node(j)
                                num_of_active_patients += 1
                        if num_of_active_patients > 0:
                            temp_graph.add_edge(i, j, weight=num_of_active_patients)

                # find metrics
                centrality = None
                if metric_scope == 1:
                    # Whole graph
                    if metric == 1:
                        data += [nx.number_of_nodes(temp_graph)]
                    if metric == 2:
                        data += [nx.number_of_edges(temp_graph)]
                    if metric == 3:
                        data += [nx.average_degree_connectivity(temp_graph)]
                    if metric == 4:
                        data += [nx.density(temp_graph)]
                    if metric == 5:
                        pass

                elif metric_scope == 2:
                    # Specific node
                    if metric == 1:
                        centrality = nx.degree_centrality(temp_graph)
                    if metric == 2:
                        centrality = nx.betweenness_centrality(temp_graph)
                    if metric == 3:
                        pass
                    if metric == 4:
                        centrality = nx.eigenvector_centrality(temp_graph)

                    if centrality.__contains__(node_number):
                        data += [centrality[node_number]]
                    else:
                        data += [0]
                else:
                    print("INVALID VALUE FOR metric_scope IN ITERATE METHOD, VALUE SHOULD BE 1 OR 2")





            return data






