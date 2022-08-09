import dash
from dash import html, dcc


layout = html.Div(
    children=[
        html.H1("This page does not exist", style={'text-align': 'center'})
    ]

)


dash.register_page(__name__)