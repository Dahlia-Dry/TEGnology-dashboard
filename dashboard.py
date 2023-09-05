from dash import Dash, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import tago
import datetime

from dashboard_components.dashboard_layout import *

temp_sensor = tago.Device('20e8e742-e5e2-4c6b-acfc-8520022e5d8a')
buffer_length = 100
fontawesome='https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css'
mathjax = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,fontawesome])
app.scripts.append_script({ 'external_url' : mathjax })
server = app.server
app.layout = LAYOUT

@callback(
    [Output('temp-graph', 'figure'),
     Output('last_updated','children')],
    Input('update_interval', 'n_intervals')
)
def update_graph(value):
    temp1_query= {'qty':buffer_length,'variable':'temperature1'}
    temp2_query= {'qty':buffer_length,'variable':'temperature2'}
    result1 = temp_sensor.find(temp1_query)['result']
    result2 = temp_sensor.find(temp2_query)['result']
    times = [result1[i]['time'] for i in range(len(result1))]
    temp1 = [result1[i]['value'] for i in range(len(result1))]
    temp2 = [result2[i]['value'] for i in range(len(result2))]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times,y=temp1,mode='lines',name='probe 1'))
    fig.add_trace(go.Scatter(x=times,y=temp2,mode='lines',name = 'probe 2'))
    fig.update_layout(yaxis_title = 'Temperature [C]',xaxis_title='Time')
    return fig,f"Last updated {pd.to_datetime(datetime.datetime.now()).round('1s')}"

if __name__ == '__main__':
    app.run(debug=True)