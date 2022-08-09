import dash
from dash import html, dcc, Input, Output, State
import dash_uploader as du


app = dash.get_app()
du.configure_upload(app=app, folder="uploaded_files")


layout = html.Div(
    children=[
        html.H1("Import"),
        html.P("In this page, you will be able to import a dataset", style={'font-size': '20px'}),
        html.H1(id='upload-status', children="File not yet uploaded"),

        du.Upload(id='dash-uploader', text='Drag and Drop Here to upload a dataset', filetypes=['csv'], max_files=1)



    ]


)


@du.callback(id='dash-uploader',
             output=Output(component_id='upload-status', component_property='children')
             )
def uploaded_file(status: du.UploadStatus):
    if status.is_completed:
        print("File has uploaded")
        pages.Cleaning.start()
        return "File has uploaded"
    return "File is not yet uploaded"




dash.register_page(__name__, path='/Import')