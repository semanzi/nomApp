import dash
from dash import html, dcc, Input, Output, State

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                    html.Div(children=[html.Div(style={'width': '20%', 'height': '20%', 'margin': 'auto', 'background-color': 'red'}),
                    html.Div(style={'width': '20%', 'height': '20%', 'margin': 'auto', 'background-color': 'red'}),
                    html.Div(style={'width': '20%', 'height': '20%', 'margin': 'auto', 'background-color': 'red'}),
                    html.Div(style={'width': '20%', 'height': '20%', 'margin': 'auto', 'background-color': 'red'}),], style={'height': '30%', 'width': '80%', 'background-color': 'blue', 'margin': 'auto'}),




                    #html.Div(style={'width': '20%', 'height': '20%', 'margin': 'auto', 'background-color': 'red'}),
                    #html.Div(style={'width': '20%', 'height': '20%', 'margin': 'auto', 'background-color': 'red'}),
                    #html.Div(style={'width': '20%', 'height': '20%', 'margin': 'auto', 'background-color': 'red'}),
                    #html.Div(style={'width': '20%', 'height': '20%', 'margin': 'auto', 'background-color': 'red'}),


                    #html.H3("Home", style={'color': 'white', 'position': 'absolute', 'left': '25vw', 'top': '25%'}),
                    #html.H3("Upload", style={'color': 'white', 'position': 'absolute', 'left': '40vw'}),
                    #html.H3("Cleaning and Data Summary", style={'color': 'white', 'position': 'absolute', 'left': '60vw'}),
                    #html.H3("Network Visualisation", style={'color': 'white', 'position': 'absolute', 'left': '75vw'})
                      ],
            style={'width': '100vw', 'height': '20vh', 'background-color': '#000000', 'position': 'fixed'}
        ),



        html.H1("Hello World", style={'height': '110vh', 'position': 'relative', 'top': '25vh'})

    ]


)







if __name__ == '__main__':
    app.run_server(debug=True)
