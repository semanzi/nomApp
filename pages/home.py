import dash
from dash import html, dcc


layout = html.Div(
    children=[
        html.H1("Welcome!", style={'text-align': 'center'}),
        html.Div(style={'width': '100vw', 'height': '500px', 'background-color': 'green'}),
        html.Div(style={'width': '100vw', 'height': '500px', 'background-color': 'yellow'})
    ]


)


dash.register_page(__name__, path='/')