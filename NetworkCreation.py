import pandas as pd


def get_services(dataset: pd.DataFrame):
    return dataset['service'].drop_duplicates().tolist()


def create_nodes_and_edges(dataset: pd.DataFrame):
    elements = []
    # Add the nodes
    services = get_services(dataset=dataset)
    for i in range(len(services)):
        node = {'data': {'id': str(services[i]), 'label': str(services[i])}}
        elements.append(node)

    # Add the edges
    # Create an empty 2x2 matrix
    matrix = [[0 for i in range(len(services))] for j in range(len(services))]
    num_of_rows = len(dataset)
    prev_row = 0
    next_row = 1
    for i in range(num_of_rows - 1):
        prev_row_id = dataset.loc[prev_row]['id']
        next_row_id = dataset.loc[next_row]['id']
        prev_row_service = dataset.loc[prev_row]['service']
        next_row_service = dataset.loc[next_row]['service']
        if next_row_id == prev_row_id:
            # same patient
            index = [0, 0]
            for j in range(len(services)):
                if services[j] == prev_row_service:
                    index[0] = j
                if services[j] == next_row_service:
                    index[1] = j
            matrix[index[0]][index[1]] += 1

        prev_row += 1
        next_row += 1

    for i in range(len(services)):
        for j in range(len(services)):
            if matrix[i][j] > 0:
                edge = {'data': {'source': services[i], 'target': services[j], 'weight': matrix[i][j]}}
                elements.append(edge)

    return elements




# Creates the graph, argument is a clean dataset
def initialise_graph(dataset: pd.DataFrame):
    pass
