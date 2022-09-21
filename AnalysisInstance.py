import pandas as pd
from dash import html, dcc
from datetime import date, datetime
from DateSlider import DateSlider
from NetworkCreation import Network
import plotly.express as px


# An AnalysisInstance object contains all the necessary pieces to analyse a range of data
# Callbacks for AnalysisInstance objects are dealt with in main.py
class AnalysisInstance:
    __instance_id = ""
    __dataset = None
    __date_slider = None
    __network = None
    __toggle_value = "out"
    __selected_node = ""
    __slider_start_pos = None
    __slider_end_pos = None
    __selected_metric_scope = 1
    __selected_metric = 1

    # Empty __init__(self) -> Just creates a new object
    def __init__(self):
        pass

    # Initialises the AnalysisInstance object
    def initialise(self, instance_id: str, dataset: pd.DataFrame):
        self.__instance_id = instance_id
        self.__dataset = dataset
        self.__date_slider = DateSlider(id="instance" + str(instance_id) + "date_slider",
                                        start_date=date(day=1, month=1, year=2000),
                                        end_date=datetime.today().date(),
                                        slice_size=1,
                                        slice_resolution=1
                                        )
        self.__slider_start_pos = 0
        self.__slider_end_pos = self.__date_slider.get_length() - 1
        self.__network = Network()
        self.__network.initialise(dataset)

    # MUTATORS
    # Sets the date range of the Date Slider
    def set_date_range(self, start_date: date, end_date: date):
        self.__date_slider.update_slider(start_date,
                                         end_date,
                                         self.__date_slider.get_slice_size(),
                                         self.__date_slider.get_slice_resolution()
                                         )

    # Sets the date resolution of the Date Slider
    def set_date_resolution(self, slice_resolution: int):
        self.__date_slider.update_slider(self.__date_slider.get_start_date(),
                                         self.__date_slider.get_end_date(),
                                         self.__date_slider.get_slice_size(),
                                         slice_resolution
                                         )

    # Sets the slice size of the Date Slider
    def set_slice_size(self, slice_size: int):
        self.__date_slider.update_slider(self.__date_slider.get_start_date(),
                                         self.__date_slider.get_end_date(),
                                         slice_size,
                                         self.__date_slider.get_slice_resolution(),
                                         )

    #
    def set_start_pos(self, pos: int):
        self.__slider_start_pos = pos

    #
    def set_end_pos(self, pos: int):
        self.__slider_end_pos = pos

    # Sets the selected node to be shown on the sub-graph
    def set_selected_node(self, node: str):
        self.__selected_node = node
        self.__network.set_selected_node(node)

    # Toggles the sub-graph to display in/out nodes from the selected node
    def toggle(self):
        if self.__toggle_value == "out":
            self.__toggle_value = "in"
        else:
            self.__toggle_value = "out"

    # Sets the metric scope
    def set_metric_scope(self, value: int):
        self.__selected_metric_scope = value

    # Sets the metric
    def set_metric(self, value: int):
        self.__selected_metric = value

    # Returns the RangeSlider object held within the DateSlider object
    # ACCESSORS
    def get_slider(self):
        return self.__date_slider.get_slider()

    # Updates the main graph, then returns the elements within it
    def get_main_graph_elements(self):
        self.__network.create_cytoscape_nodes_and_edges(False,
                                                        self.__date_slider.get_date_at_pos(self.__slider_start_pos),
                                                        self.__date_slider.get_date_at_pos(self.__slider_end_pos)
                                                        )
        return self.__network.get_cytoscape_nodes() + self.__network.get_cytoscape_edges()

    # Returns the sub-graph elements
    def get_sub_graph_elements(self):
        return self.__network.get_specific_node_elements(self.__toggle_value)

    # Returns a plot of the selected metric over the selected time range
    def get_plot(self, metric_name: str):
        data = self.__network.iterate(self.__date_slider.get_date_at_pos(self.__slider_start_pos),
                                      self.__date_slider.get_date_at_pos(self.__slider_end_pos),
                                      self.__date_slider.get_slice_resolution(),
                                      self.__date_slider.get_slice_size(),
                                      self.__selected_metric_scope,
                                      self.__selected_metric
                                      )
        return px.line(x=[i for i in range(len(data))],
                       y=[data[i] for i in range(len(data))],
                       labels={'x': 'date', 'y': metric_name},
                       title="Graph showing " + metric_name + ", for the node: " + self.__selected_node
                       )

    # Here we build an instance of an analysis
    def get_layout(self):
        return html.Div(
            children=[
                # 1st row - Title and close button
                html.Div(
                    children=[
                        html.H1(children="Instance " + str(self.__instance_id),
                                style={'text-align': 'center',
                                       'position': 'absolute',
                                       'width': '100%',
                                       'left': '0px',
                                       'font-family': 'Arial'
                                       }
                                ),
                        html.Button(id='close_button_' + self.__instance_id,
                                    children="CLOSE",
                                    style={'width': '8%',
                                           'height': '80%',
                                           'position': 'absolute',
                                           'right': '2%',
                                           'top': '20%'
                                           }
                                    ),

                        ],
                    style={
                        'position': 'absolute',
                        'width': '100%',
                        'height': '8%',
                    }
                ),

                # 2nd row - Date selection
                html.Div(
                    children=[
                        html.Div(children=[
                            dcc.DatePickerRange(id="instance" + str(self.__instance_id) + "date_range_picker", style={'width': '90%', 'position': 'absolute', 'left': '10%', 'top': '25%'}, display_format='DD/MM/YYYY',
                                                start_date=date(day=1, month=1, year=2000),
                                                end_date=datetime.today().date(), persistence=False),
                        ],
                                 style={'position': 'absolute', 'width': '33.3%', 'height': '100%'}
                        ),
                        html.Div(children=[
                            dcc.Dropdown(id="instance" + str(self.__instance_id) + "date_resolution", options=['Year', 'Month', 'Day'],
                                         style={'position': 'absolute', 'left': '0%', 'top': '33%', 'width': '100%', 'height': '50%'},
                                         value='Year', clearable=False, persistence=False),
                        ],
                                 style={'position': 'absolute', 'left': '33.3%', 'width': '33.3%', 'height': '100%'}
                        ),
                        html.Div(children=[
                            dcc.Input(id="instance" + str(self.__instance_id) + "slice_size", value=1, style={'width': '90%', 'height': '50%', 'margin-left': '4%', 'margin-top': '6.5%'},
                                      required=True, min=1, type='number', persistence=False),

                        ],
                                 style={'position': 'absolute', 'right': '0px', 'width': '33.3%', 'height': '100%'}
                        ),
                    ],
                    style={'position': 'absolute', 'top': '8%', 'width': '100%', 'height': '10%'}
                ),



                # 3rd row - Date slider
                html.Div(children=[
                    self.__date_slider.get_slider()
                ],
                    style={'position': 'absolute', 'top': '18%', 'width': '100%', 'height': '10%'},
                    id="instance" + str(self.__instance_id) + "date_slider_container"
                ),



                # 4th row - Graphs
                html.Div(
                    children=[
                        self.__network.get_cytoscape_graph("instance" + str(self.__instance_id) + "main_graph"),
                        self.__network.get_specific_node_cytoscape_graph("instance" + str(self.__instance_id) + "sub_graph", "out"),
                        html.Button("TOGGLE IN/OUT", id="instance" + str(self.__instance_id) + "toggle", style={'position': 'absolute', 'left': '85.7%', 'top': '35%', 'width': '14%', 'height': '30%'})
                    ],
                    style={'position': 'absolute', 'top': '28%', 'width': '100%', 'height': '40%'}

                ),


                # 5th row - Graph metrics
                html.Div(
                    children=[
                        # Graph Selection
                        html.Div(
                            children=[
                                html.Div(children=[
                                    html.H1("Metric Scope:", style={'margin': '0px'})
                                ],
                                    style={
                                        'position': 'absolute',
                                        'left': '0%',
                                        'width': '25%',
                                        'height': '100%'
                                    }
                                    ),
                                html.Div(children=[
                                    dcc.Dropdown(id="instance" + str(self.__instance_id) + "metric_scope",
                                                 clearable=False,
                                                 options=['Graph Level', 'Node Level'],
                                                 value='Node Level',
                                                 style={
                                                     'position': 'absolute',
                                                     'top': '2px',
                                                     'width': '100%'
                                                 }
                                                 )
                                ],
                                    style={
                                        'position': 'absolute',
                                        'left': '25%',
                                        'width': '25%',
                                        'height': '100%'
                                    }
                                ),
                                html.Div(children=[
                                    html.H1("Metric:", style={'margin': '0px'})
                                ],
                                    style={
                                        'position': 'absolute',
                                        'left': '50%',
                                        'width': '25%',
                                        'height': '100%'
                                    }
                                ),
                                html.Div(children=[
                                    dcc.Dropdown(id="instance" + str(self.__instance_id) + "metric",
                                                 clearable=False,
                                                 options=['Degree Centrality', 'Betweenness Centrality', 'Modularity Centrality', 'Eigenvector Centrality'],
                                                 value='Degree Centrality',
                                                 style={
                                                     'position': 'absolute',
                                                     'top': '2px',
                                                     'width': '100%',
                                                 }
                                                 )
                                ],
                                    style={
                                        'position': 'absolute',
                                        'left': '75%',
                                        'width': '25%',
                                        'height': '100%'
                                    }
                                ),

                            ],
                            style={
                                'position': 'absolute',
                                'top': '2px',
                                'width': '90%',
                                'height': '8%'
                            }
                        ),
                        html.Button(id='instance' + str(self.__instance_id) + "info_button",
                                    children="What's this?",
                                    style={
                                        'position': 'absolute',
                                        'left': '90%',
                                        'width': '10%',
                                        'height': '8%',
                                        'top': '2%'

                                    }
                                    ),
                        dcc.Graph(id="instance" + str(self.__instance_id) + "plot", figure=px.line(x=[0], y=[0], title="EMPTY GRAPH"), style={'position': 'absolute', 'width': '100%', 'height': '90%', 'top': '10%'})
                    ],
                    style={'position': 'absolute', 'top': '68%', 'width': '100%', 'height': '32%'}

                )







            ],


            style={'position': 'relative', 'width': '80vw', 'height': '80vw', 'background-color': '#CEF0ED', 'margin-left': 'auto', 'margin-right': 'auto', 'margin-bottom': '50px', 'border-style': 'solid', 'border-radius': '20px', 'overflow': 'hidden'}
        )


