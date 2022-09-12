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
    __exit_page_shown = False
    __dataset = None
    __slider = None
    __network = None
    __toggle_value = "out"

    selected_node = ""
    slider_start_pos = None
    slider_end_pos = None
    selected_metric_scope = 1
    selected_metric = 1

    def __init__(self):
        pass

    def initialise(self, instance_id: str, dataset: pd.DataFrame):
        self.__instance_id = instance_id
        self.__dataset = dataset
        self.__slider = DateSlider(id="instance" + str(instance_id) + "date_slider", start_date=date(day=1, month=1, year=2000), end_date=datetime.today().date(),
                                   slice_size=1,
                                   slice_resolution=1)
        self.slider_start_pos = 0
        self.slider_end_pos = self.__slider.length - 1
        self.__network = Network()
        self.__network.initialise(dataset)

    def set_selected_node(self, selected_node: str):
        self.selected_node = selected_node
        self.__network.set_selected_node(selected_node)

    def get_specific_node_elements(self):
        return self.__network.get_specific_node_elements(self.__toggle_value)

    def toggle(self):
        if self.__toggle_value == "out":
            self.__toggle_value = "in"
        else:
            self.__toggle_value = "out"
        return self.__network.get_specific_node_elements(self.__toggle_value)

    def set_date_range(self, start_date: date, end_date: date):
        self.__slider.update_slider(start_date, end_date, self.__slider.slice_size, self.__slider.slice_resolution)

    def set_date_resolution(self, resolution: int):
        self.__slider.update_slider(self.__slider.start_date, self.__slider.end_date, self.__slider.slice_size, resolution)

    def set_slice_size(self, slice_size: int):
        self.__slider.update_slider(self.__slider.start_date, self.__slider.end_date, slice_size, self.__slider.slice_resolution)

    def get_slider(self):
        return self.__slider.get_slider()

    def update_main_graph(self, start_pos: int, end_pos: int):
        self.__network.create_cytoscape_nodes_and_edges(all_nodes_and_edges=False, start_date=self.__slider.get_date_at_pos(start_pos), end_date=self.__slider.get_date_at_pos(end_pos))
        return self.__network.get_cytoscape_nodes() + self.__network.get_cytoscape_edges()

    def get_plot(self):
        return self.__network.iterate(self.__slider.get_date_at_pos(self.slider_start_pos), self.__slider.get_date_at_pos(self.slider_end_pos), self.__slider.slice_resolution, self.__slider.slice_size, self.selected_metric_scope, self.selected_metric)



    # Here we build an instance of an analysis
    def get_layout(self):
        if self.__exit_page_shown:
            pass

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
                    self.__slider.get_slider()
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
                        html.Button(id='',
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


