import dash
from dash import html, dcc, Input, Output, State
import dash_uploader as du
import pandas as pd

app = dash.Dash(__name__)
server = app.server

du.configure_upload(app=app, folder="uploaded_files")

global file
file = None


app.layout = html.Div(
    children=[
        # NAVIGATION BAR
        html.Div(
            children=[
                dcc.Link('Home', href='/', style={'margin': '10px', 'font-size': '30px'}),
                dcc.Link('Import Data', href='/Import', style={'margin': '10px', 'font-size': '30px'}),
                dcc.Link('Data Summary and Cleaning', href='/Cleaning', style={'margin': '10px', 'font-size': '30px'}),
                dcc.Link('Data Visualisation and Graph Metrics', href='Visualisation', style={'margin': '10px', 'font-size': '30px'}),
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
        # PAGE VIEWER
        html.Div(
            id = 'page-viewer',
            children=[],
            style={'width': '100vw', 'height': '600px', 'position': 'relative', 'top': '12vw'}

        ),
        dcc.Location(id='url', refresh=False)
    ],

)


##### CREATE PAGES #####

uploader_component = du.Upload(id='dash-uploader', max_files=1, filetypes=['csv'], text="Drag and Drop a dataset.csv file here")


def get_home_page():
    return [
        html.H1("Welcome", style={'text-align' : 'center'}),
        html.H2("What is this application?", style={'font-size': '30px'}),
        html.P("This application is a tool that allows users to visualise the NHS and its services as a network graph,"
               "then calculate graph metrics such as clustering, degree and centrality. These metrics can then be "
               "plotted over time", style={'font-size': '25px'}),
        html.H2("Features", style={'font-size': '30px'}),
        html.P("", style={'font-size': '25px'}),
        html.H2("Why is the tool useful?", style={'font-size': '30px'}),
        html.P("", style={'font-size': '25px'}),
        html.H2("We encourage you to extend this...", style={'font-size': '30px'}),
        html.P("If there is a feature that you wish to have, but that is not included in this toolset, feel free to add "
               "it yourself! This application is fully documented, with explanations of the algorithms used in creating "
               "the network graphs and calculating graph metrics", style={'font-size': '25px'}),

        html.Div(style={'background-color': 'green', 'width': '100vw', 'height': '600px'}),
        html.Div(style={'background-color': 'yellow', 'width': '100vw', 'height': '600px'}),

    ]


def get_import_page():
    if file is None:
        return [
            html.H1("On this page, you can import your dataset"),
            uploader_component,
            html.H1(children="The file has not yet been uploaded", id='upload-status')
        ]
    else:
        return [
            html.H1("On this page, you can import your dataset"),
            uploader_component,
            html.H1(children='A file has already been uploaded, but you may upload a different one', id='upload-status')


        ]



def get_cleaning_page():
    global file
    if file is None:
        return [
            html.H1("This is the cleaning page"),
            html.H2("No file has been uploaded")
        ]
    else:
        return[
            html.H1("This is the cleaning page"),
            html.H2(file.columns + "\n\n\n\n\n\n")

        ]












# Deal with different pages

@app.callback(
    Output(component_id='page-viewer', component_property='children'),
    Input(component_id='url', component_property='pathname')
)
def change_page(pathname):
    if pathname == '/':
        # HOME
        return get_home_page()
    elif pathname == '/Import':
        # IMPORT
        return get_import_page()
    elif pathname == '/Cleaning':
        # CLEANING
        return get_cleaning_page()
    elif pathname == '/Visualisation':
        # VISUALISATION
        pass
    else:
        # 404 NOT FOUND
        pass


@du.callback(
    output=Output(component_id='upload-status', component_property='children'),
    id='dash-uploader'
)
def uploaded(status: du.UploadStatus):
    if status.is_completed:
        global file
        file = pd.read_csv(status.latest_file)
        return "THE FILE HAS BEEN UPLOADED"




if __name__ == '__main__':
    app.run_server(debug=True)
