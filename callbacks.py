import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
from app import app

df = pd.read_excel('test/Test_info.xls')

###Backend
def calculate_courier_price(weight): #For courier price
    if weight <= 200:
        return 5
    elif weight <= 500:
        return 10
    elif weight <= 1000:
        return 15
    elif weight <= 5000:
        return 20
    else:
        return 20  # Assuming this is the price for anything above 5000g


def create_packages(items, max_package_value=250):
    items = items.copy()
    packages = []
    
    while not items.empty:
        current_package = {'items': [], 'weight': 0, 'price': 0}
        items_to_remove = []

        for index, row in items.iterrows():
            if current_package['price'] + row['Price'] < max_package_value:
                current_package['items'].append(row['Name'])
                current_package['weight'] += row['Weight']
                current_package['price'] += row['Price']
                items_to_remove.append(index)

        # Remove the items that we've already added to a package
        items.drop(items_to_remove, inplace=True)
        
        # If no items were added, break the loop to avoid an infinite loop
        if not items_to_remove:
            break
        
        packages.append(current_package)

    return packages


def register_callbacks(app):
    @app.callback(
        [Output('order-summary-body', 'children'),
        Output('order-summary-modal', 'is_open')],
        [Input('place-order-btn', 'n_clicks'),
        Input('close-modal', 'n_clicks')],
        [State('item-checklist', 'value'),
        State('order-summary-modal', 'is_open')],
        prevent_initial_call=True
    )
    def update_order_summary(place_order_clicks, close_modal_clicks, selected_indices, is_modal_open):
        ctx = dash.callback_context

        if not ctx.triggered:
            # If no buttons were clicked, do nothing.
            return dash.no_update
        
        # Determine the button that triggered the callback
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == 'close-modal':
            return dash.no_update, False  # Close the modal

        if button_id == 'place-order-btn' and selected_indices:
            # Create a new dataframe for the selected items
            selected_items = df.iloc[selected_indices]

            # Create packages
            packages = create_packages(selected_items)
            
            # Generate the summary including all packages
            summary = [html.P("This order has the following packages:")]
            courier_price_total = 0
            for i, pkg in enumerate(packages, start=1):
                courier_price = calculate_courier_price(pkg['weight'])
                courier_price_total += courier_price
                summary.append(html.P(f"Package {i}:",style={'font-weight': 'bolder'}))
                summary.append(html.P(f"Items: {', '.join(pkg['items'])}"))
                summary.append(html.P(f"Total weight: {pkg['weight']}g"))
                summary.append(html.P(f"Total price: ${pkg['price']}", style={'font-weight': 'bold'}))
                summary.append(html.P(f"Courier price: ${courier_price}"))


            # Add courier price total to the summary
            summary.append(html.P(f"Total courier price for all packages - ${courier_price_total}"))

            return summary, True

        # In case we have any other button clicks (future-proofing)
        return dash.no_update, is_modal_open

if __name__ == '__main__':
    app.run_server(debug=True)
