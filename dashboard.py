from dash import Dash, callback, Output, Input, State,no_update
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import tago
import datetime
from dash.exceptions import PreventUpdate
from decouple import config

from dashboard_components.dashboard_layout import *
from dashboard_components.send_email import *
import dashboard_components.settings as settings

temp2_code = config('WATTECO_TEMP2')
print(temp2_code)
temp_sensor = tago.Device(temp2_code)
fontawesome='https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css'
mathjax = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,fontawesome])
app.scripts.append_script({ 'external_url' : mathjax })
server = app.server
app.layout = LAYOUT

@callback(
    [Output('temp-graph', 'figure'),
     Output('last-updated','children')],
    Input('update_interval', 'n_intervals'),
    [State('n_points','value')]
)
def update_graph(value,buffer_length):
    temp1_query= {'qty':buffer_length,'variable':'temp1'}
    temp2_query= {'qty':buffer_length,'variable':'temp2'}
    result1 = temp_sensor.find(temp1_query)['result']
    result2 = temp_sensor.find(temp2_query)['result']
    times = [pd.to_datetime(result1[i]['time'])+datetime.timedelta(hours=2) for i in range(len(result1))]
    if (datetime.datetime.now(times[-1].tzinfo)-times[-1]).total_seconds() > 60: #check if data is current within the last minute
        last_updated = f"*{pd.to_datetime(datetime.datetime.now()).round('1s')}: the harvester is currently recharging its internal buffer; thus the system is in sleep mode and no recent readings are available.*"
    else:
        last_updated = f"*{pd.to_datetime(datetime.datetime.now()).round('1s')}: the harvester is powering the sensor and data collection is live*"
    temp1 = [result1[i]['value'] for i in range(len(result1))]
    temp2 = [result2[i]['value'] for i in range(len(result2))]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=times,y=temp1,mode='lines',name='air sensor'))
    fig.add_trace(go.Scatter(x=times,y=temp2,mode='lines',name = 'surface sensor'))
    fig.update_layout(yaxis_title = 'Temperature [C]',xaxis_title='Time',hovermode = "x unified")
    return fig,last_updated

@app.callback(Output('submit-div', 'children'),
     Input("button-submit", 'n_clicks'),
     [State("email-row", 'value'),
      State("name-row", 'value'),
      State("message-row", 'value')]
    )
def submit_message(n, email, name, message):
    content = f"Subject: New Message from Dashboard!\n\n Sender: {name} [{email}] \n\n {message}"
    if n>0:
        status = send_email(settings.email_recipients,content)
        if status == 'success':
            return [html.P("Message Sent")]
        else:
            return[dbc.Button('Submit', color = 'primary', id='button-submit', n_clicks=0)]
    else:
        raise PreventUpdate
if __name__ == '__main__':
    app.run(debug=True)