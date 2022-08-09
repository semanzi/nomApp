import dash
from dash import html, dcc


layout = html.Div(
    html.H1("Visualisation")

)


dash.register_page(__name__, '/Visualisation')