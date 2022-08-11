import dash
from dash import html, dcc, Input, Output, State, dash_table
import dash_uploader as du
import pandas as pd
import dash_cytoscape as cyto
import NetworkCreation

app = dash.Dash(__name__)
server = app.server

du.configure_upload(app=app, folder="uploaded_files")

file = None
dataset_is_clean = False
network_creator = NetworkCreation.NetworkCreator()


app.layout = html.Div(
    children=[
        # NAVIGATION BAR
        html.Div(
            children=[
                dcc.Link('Home', href='/', style={'margin': '10px', 'font-size': '20px'}),
                dcc.Link('Import Data', href='/Import', style={'margin': '10px', 'font-size': '20px'}),
                dcc.Link('Data Summary and Cleaning', href='/Cleaning', style={'margin': '10px', 'font-size': '20px'}),
                dcc.Link('Data Visualisation and Graph Metrics', href='Visualisation',
                         style={'margin': '10px', 'font-size': '20px'}),
                html.Img(src="https://pbs.twimg.com/media/FRXCr36XwAcpQop?format=jpg&name=large", width='50px',
                         height='50px', style={'position': 'absolute', 'left': '10px'})
            ],
            style={
                'width': '100vw',
                'height': '6vw',
                'top': '0px',
                'left': '0px',
                'background-color': '#E6C2AA',
                'display': 'flex',
                'align-items': 'center',
                'justify-content': 'center',
                'position': 'fixed',
                'z-index': '1',
            }
        ),
        # PAGE VIEWER
        html.Div(
            id='page-viewer',
            children=[],
            style={'background-color': '#D6FDFF', 'width': '100vw', 'height': '100vh', 'position': 'relative', 'top': '12vw', 'left': '0px', 'margin': '0px', 'padding': '0px'}

        ),
        dcc.Location(id='url', refresh=False)
    ],
    style={'background-color': '#D6FDFF', 'height': 'auto', 'position': 'absolute', 'left': '0px', 'padding': '0px', 'margin': '0px', 'width': '100%'}
)


def summarise_data(dataset: pd.DataFrame):
    summary = ""
    num_of_rows = len(dataset)
    num_of_headers = len(dataset.columns)
    list_of_headers = [0 for k in range(num_of_headers)]

    for i in range(num_of_rows):
        for j in range(num_of_headers):
            if not pd.isnull(dataset.iloc[i][j]):
                list_of_headers[j] += 1

    for a in range(num_of_headers):
        summary += (str(dataset.columns[a]) + " " + str(list_of_headers[a]) + "\n\n\n")

    return summary


##### CLEANING DATA #####

def get_column_completeness(dataset: pd.DataFrame):
    num_of_rows = len(dataset)
    num_of_headers = len(dataset.columns)
    column_completeness = [0 for k in range(num_of_headers)]
    columns = dataset.columns
    for i in range(num_of_rows):
        for j in range(num_of_headers):
            if not pd.isnull(dataset.iloc[i][j]):
                column_completeness[j] += 1
    return {columns[i]: column_completeness[i] for i in range(len(columns))}


def columns_complete(dataset: pd.DataFrame):
    rows = len(dataset)
    column_completeness = get_column_completeness()
    id_completeness = column_completeness['id']
    service_completeness = column_completeness['service']
    referral_date_completeness = column_completeness['referraldate']
    if id_completeness == rows and service_completeness == rows and referral_date_completeness == rows:
        return True
    return False


def headers_labelled_correctly(dataset: pd.DataFrame):
    headers = dataset.columns
    if headers.__contains__('service') and headers.__contains__('id') and headers.__contains__('referraldate') and headers.__contains__('dischargedate'):
        return True
    return False


def id_formatted(dataset: pd.DataFrame):
    rows = len(dataset)
    for i in range(rows):
        if int(dataset.loc[i]['id']) / int(abs(dataset.loc[i]['id'])) == 1:
            return True
    return False


def data_time_formatted(dataset: pd.DataFrame):
    rows = len(dataset)
    for i in range(rows):
        # Check referral date
        referral_date = dataset.loc[i]['referraldate']
        referral_date_split = referral_date.split('/')
        if int(referral_date_split[0]) <= 0 or int(referral_date_split[1]) <= 0 or int(referral_date_split[2]) <= 0:
            return False
        if int(referral_date_split[0]) > 31 or int(referral_date_split[1]) > 12:
            return False
        # Check discharge date
        discharge_date = dataset.loc[i]['dischargedate']



    return True


##### CREATE PAGES #####

uploader_component = du.Upload(id='dash-uploader', max_files=1, filetypes=['csv'],
                               text="Drag and Drop a dataset.csv file here")

# HOME
def get_home_page():
    return [
        html.H1("Welcome", style={'text-align': 'center'}),
        html.H2("What is this application?", style={'font-size': '30px'}),
        html.P("This application is a tool that allows users to visualise the NHS and its services as a network graph,"
               "then calculate graph metrics such as clustering, degree and centrality. These metrics can then be "
               "plotted over time", style={'font-size': '25px'}),
        html.H2("Features", style={'font-size': '30px'}),
        html.Ul(
            children=[
                html.Li("Visualise a dataset as a network graph", style={'font-size': '25px'}),
                html.Li("Select specific nodes (services) and get metrics", style={'font-size': '25px'}),
                html.Li("Create sub-graphs that satisfy conditions", style={'font-size': '25px'}),
                html.Li("View data from a slice of time", style={'font-size': '25px'}),
                html.Li("Plot graph metrics over time", style={'font-size': '25px'}),
                html.Li("Export graphs as images", style={'font-size': '25px'}),
            ],
            style={'list-style-type': 'disc'}
        ),
        html.H2("Why is the tool useful?", style={'font-size': '30px'}),
        html.P("", style={'font-size': '25px'}),
        html.H2("We encourage you to extend this...", style={'font-size': '30px'}),
        html.P(
            "If there is a feature that you wish to have, but that is not included in this toolset, feel free to add "
            "it yourself! This application is fully documented, with explanations of the algorithms used in creating "
            "the network graphs and calculating graph metrics", style={'font-size': '25px'}),


    ]

# IMPORTING
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

# CLEANING
def get_cleaning_page():
    global file
    if file is None:
        return [
            html.H1("No dataset has been imported, please go to the \"Import Data\" page and import a dataset",
                    style={'text-align': 'center', 'font-size': '40px', 'top': '50%', 'position': 'relative'}),
        ]
    else:
        summary = summarise_data(file)
        if headers_labelled_correctly(file):
            summary += "The headers have been labelled correctly"
        else:
            summary += "The headers have been labelled incorrectly"

        return [
            html.H1("This is the cleaning page", style={'text-align': 'center', 'font-size': '40px'}),
            html.H2("The checks that need to be done:"),
            html.Ul(
                children=[
                    html.Li(children="Check correct header names, should be: ID, Service, ReferralDate, DischargeDate", id='check_header_names'),
                    html.Li(children="Check that ID, Service, ReferralDate are complete", id='check_column_completeness'),
                    html.Li(children="Check ID is correct format (non-negative)", id='check_id'),
                    html.Li(children="Check ReferralDate and DischargeDate are in correct format (non-negative, sensible values, dd/mm/yy)", id='check_datetime'),

                ],
                style={'list-style-type': 'disc'}
                    ),
            html.H2("The number of rows in the dataset is " + str(len(file))),
            html.P(summary),
            dash_table.DataTable(data=file.to_dict('records'), columns=[{"name": i, "id": i} for i in ['id', 'service', 'referraldate', 'dischargedate']], style_table={'width': '50vw', 'margin': '10px'})

        ]

elements = []

# VISUALISATION
def get_visualisation_page():
    global file
    global network_creator
    if file is None:
        return [
            html.H1("No dataset has been imported, please go to the \"Import Data\" page and import a dataset",
                    style={'text-align': 'center', 'font-size': '40px', 'top': '50%', 'position': 'relative'}),
        ]
    else:
        return [
            network_creator.get_cytoscape_graph('main-graph')

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
        return get_visualisation_page()
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
        file.columns = [x.lower() for x in file.columns]
        global network_creator
        network_creator.initialise(file)
        global elements
        elements = network_creator.get_cytoscape_nodes() + network_creator.get_cytoscape_edges()

        return "THE FILE HAS BEEN UPLOADED"


if __name__ == '__main__':
    app.run_server(debug=True)
