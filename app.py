"""Serves as the entry point for the project module."""
from dash import Dash


app = Dash(__name__, pages_folder="incident_reporting/pages/", use_pages=True)


if __name__ == "__main__":
    app.run(debug=True)
