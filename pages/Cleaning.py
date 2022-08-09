import dash
from dash import html, dcc


layout = html.Div(
    html.H1("Cleaning")

)


dash.register_page(__name__, '/Cleaning')