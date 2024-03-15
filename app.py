import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd

# Initialize your Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Import your app layout and callbacks
from layout import layout
from callbacks import register_callbacks


app.layout = layout
register_callbacks(app)


# Flask instance to be used by Gunicorn
server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
