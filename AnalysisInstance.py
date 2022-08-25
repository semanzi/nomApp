import dash
from dash import html, dcc
from datetime import date
from DateSlider import DateSlider

class AnalysisInstance:
    analysis_name = ""
    exit_page_shown = False


    def __init__(self, analysis_name: str):
        self.analysis_name = analysis_name
        #self.app = app
        self.slider = DateSlider(start_date=date(day=1, month=1, year=2000), end_date=date(day=1, month=1, year=2050),
                            slice_size=1,
                            slice_resolution='Year')




    # Here we build an instance of an analysis
    def get(self):
        if self.exit_page_shown:
            pass

        return html.Div(
            children=[
                # 1st row - Title and close button
                html.Div(
                    children=[
                        html.H1("Instance", style={'text-align': 'center',
                                                'position': 'absolute',
                                                'width': '100%',
                                                'left': '0px'
                                                }
                                ),
                        html.Button(id='close_button_' + self.analysis_name,
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
                        'position': 'relative',
                        'width': '100%',
                        'height': '8%',
                    }
                ),

                # 2nd row - Date selection
                html.Div(
                    children=[
                        html.Div(children=[
                            dcc.DatePickerRange(id='date_picker', style={'width': '90%', 'position': 'absolute', 'left': '10%', 'top': '25%'}, display_format='DD/MM/YYYY',
                                                start_date=date(day=1, month=1, year=2000),
                                                end_date=date(day=1, month=1, year=2050)),
                        ],
                                 style={'position': 'absolute', 'width': '33.3%', 'height': '100%'}
                        ),
                        html.Div(children=[
                            dcc.Dropdown(id='dropdown', options=['Year', 'Month', 'Day'],
                                         style={'position': 'absolute', 'left': '0%', 'top': '33%', 'width': '100%', 'height': '50%'},
                                         value='Year', clearable=False),
                        ],
                                 style={'position': 'absolute', 'left': '33.3%', 'width': '33.3%', 'height': '100%'}
                        ),
                        html.Div(children=[
                            dcc.Input(id='slice_size_input', value=1, style={'width': '90%', 'height': '50%', 'margin-left': '4%', 'margin-top': '6.5%'},
                                      required=True, min=1),

                        ],
                                 style={'position': 'absolute', 'right': '0px', 'width': '33.3%', 'height': '100%'}
                        ),
                    ],
                    style={'position': 'relative', 'width': '100%', 'height': '10%'}
                ),



                # 3rd row - Date slider
                html.Div(children=[
                    self.slider.get_slider()

                ],
                         style={'position': 'relative', 'width': '100%', 'height': '10%'}
                ),



                # 4th row
                html.Div(
                    children=[],
                    style={'position': 'relative', 'width': '100%', 'height': '50%', 'background-color': 'red'}


                )







            ],


            style={'width': '80vw', 'height': '80vw', 'background-color': '#4acc16', 'margin': 'auto'}
        )


