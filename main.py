import dash
from dash import html, dcc, Input, Output, State

app = dash.Dash(__name__, use_pages=True)
server = app.server


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                dcc.Link('Home', href=dash.page_registry['pages.home']['path'], style={'margin': '10px', 'font-size': '30px'}),
                dcc.Link('Import Data', href=dash.page_registry['pages.Import']['path'], style={'margin': '10px', 'font-size': '30px'}),
                dcc.Link('Data Summary and Cleaning', href=dash.page_registry['pages.Cleaning']['path'], style={'margin': '10px', 'font-size': '30px'}),
                dcc.Link('Data Visualisation and Graph Metrics', href=dash.page_registry['pages.Visualisation']['path'], style={'margin': '10px', 'font-size': '30px'}),
                html.Img(src="https://pbs.twimg.com/media/FRXCr36XwAcpQop?format=jpg&name=large", width='150px', height='150px', style={'position': 'absolute', 'left': '10px'})
            ],
            style={
                'width': '100vw',
                'height': '10vw',
                'top': '0px',
                'left': '0px',
                'background-color': 'red',
                'display': 'flex',
                'align-items': 'center',
                'justify-content': 'center',
                'position': 'fixed',
                'z-index': '1',
            }
        ),
        html.Div(
            children=[
                dash.page_container
            ],
            style={'width': '100vw', 'height': '600px', 'position': 'relative', 'top': '12vw'}

        )
    ],

)









if __name__ == '__main__':
    app.run_server(debug=True)
