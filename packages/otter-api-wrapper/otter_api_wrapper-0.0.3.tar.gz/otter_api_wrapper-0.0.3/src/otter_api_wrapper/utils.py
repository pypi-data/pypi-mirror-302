import plotly
import json

def save_plotly_figure(json_fig, filename):
    fig = plotly.io.from_json(json.dumps(json_fig))
    fig.write_image(filename)