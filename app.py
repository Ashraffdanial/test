import dash
import index

app = dash.Dash(__name__, suppress_callback_exceptions=True)
server = app.server  # Expose the server variable for deployments

index.registercallbacks(app)