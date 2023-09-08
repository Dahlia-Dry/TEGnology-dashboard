from dash import Dash, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import tago
import datetime

from dashboard_components.dashboard_layout import *

temp_sensor = tago.Device('16efae85-3236-4c45-a515-fa9dc1f77e90')
fontawesome='https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css'
mathjax = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,fontawesome])
app.scripts.append_script({ 'external_url' : mathjax })
server = app.server
app.layout = LAYOUT

@callback(
    [Output('temp-graph', 'figure'),
     Output('last_updated','children')],
    Input('update_interval', 'n_intervals'),
    State('n_points','value')
)
def update_graph(value,buffer_length):
    temp1_query= {'qty':buffer_length,'variable':'temperature1'}
    temp2_query= {'qty':buffer_length,'variable':'temperature2'}
    result1 = temp_sensor.find(temp1_query)['result']
    result2 = temp_sensor.find(temp2_query)['result']
    times = [pd.to_datetime(result1[i]['time'])+datetime.timedelta(hours=2) for i in range(len(result1))]
    temp1 = [result1[i]['value'] for i in range(len(result1))]
    temp2 = [result2[i]['value'] for i in range(len(result2))]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times,y=temp1,mode='lines',name='air sensor'))
    fig.add_trace(go.Scatter(x=times,y=temp2,mode='lines',name = 'pipe sensor'))
    fig.update_layout(yaxis_title = 'Temperature [C]',xaxis_title='Time')
    return fig,f"*Last updated {pd.to_datetime(datetime.datetime.now()).round('1s')}*"

if __name__ == '__main__':
    app.run(debug=True)