import dash_bootstrap_components as dbc
from dash import html
import pandas as pd

# Load your data
df = pd.read_excel('Test_info.xls')
# Define your app layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Col([
                html.P('Select Items', className="tittle"),
                dbc.Checklist(
                    id='item-checklist',
                    options=[{'label': f"{row['Name']} - ${row['Price']} , {row['Weight']}g", 'value': idx} for idx, row in df.iterrows()],
                    value=[],
                    inline=False,
                    className="check_list"
                ),
                dbc.Button('Place Order', id='place-order-btn', color='primary', className='mt-3'),
            ], className="inner_container"),
        ], className="outer_container")
    ]),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Order Summary")),
        dbc.ModalBody(id='order-summary-body'),
        dbc.ModalFooter(dbc.Button("Close", id='close-modal', className="ms-auto", n_clicks=0))
    ], id='order-summary-modal', is_open=False, size="lg"),
], fluid=True)

