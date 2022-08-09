import dash
from dash import html, dcc
import dash_uploader as du


layout = html.Div(
    children=[
        html.H1("Import"),
        html.P("In this page, you will be able to import a dataset", style={'font-size': '20px'}),

        #du.Upload(id='dash-uploader', text='Drag and Drop Here to upload a dataset', filetypes=['csv'], max_files=1)



    ]


)


dash.register_page(__name__, path='/Import')