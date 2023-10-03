from dash import Dash, callback, Output, Input, State,no_update
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import pymysql
import datetime
from dash.exceptions import PreventUpdate
from decouple import config
import boto3

from dashboard_components.dashboard_layout import *
import dashboard_components.email_smtp as email_smtp
import dashboard_components.settings as settings
import dashboard_components.timestream_wrapper as aws_ts

fontawesome='https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css'
mathjax = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP,fontawesome])
app.scripts.append_script({ 'external_url' : mathjax })
server = app.server
app.layout = LAYOUT
timestream_region_name='eu-central-1'

temp2db = aws_ts.TimestreamDB('tegnology_demo_sensors','watteco_temp_2')


@callback(
    [Output('temp-graph', 'figure'),
     Output('last-updated','children')],
    [Input('update_interval', 'n_intervals'),
     Input('n_points','value')]
)
def update_graph(value,buffer_length,sampling_frequency = 180):
    try:
        results = pd.DataFrame.from_records(temp2db.read(buffer_length))
        results['time'] = pd.to_datetime(results['time'])+datetime.timedelta(hours=2)
        if (datetime.datetime.now(results['time'].iloc[0].tzinfo)-results['time'].iloc[0]).total_seconds() > 250: #check if data is current 
            last_updated = f"*{pd.to_datetime(datetime.datetime.now()).round('1s')}: the harvester is currently recharging its internal buffer; thus the system is in sleep mode and no recent readings are available.*"
        else:
            last_updated = f"*{pd.to_datetime(datetime.datetime.now()).round('1s')}: the harvester is powering the sensor and data collection is live*"
        #todo later
        """date_rng = pd.date_range(start=min(results['time']).date(), end=max(results['time']).date(), freq='3min')
        datetimes = pd.DataFrame(date_rng,columns=['time'])
        print(min(results['time']).date(),max(results['time']).date(),len(datetimes))
        datetimes['temp1'] = [None for i in range(len(datetimes))]
        datetimes['temp2'] = [None for i in range(len(datetimes))]
        datetimes = datetimes[datetimes['time'] not in results['time']]
        results= pd.merge(results,datetimes,how='left')
        print(results.head())"""
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=results['time'],y=results['temp1'].astype('float'),mode='lines',name='air sensor',connectgaps=False))
        fig.add_trace(go.Scatter(x=results['time'],y=results['temp2'].astype('float'),mode='lines',name = 'surface sensor',connectgaps=False))
    except Exception as e:
        print(e)
        fig=go.Figure()
        df = pd.read_csv('assets/demo-data.csv')
        fig.add_trace(go.Scatter(x=pd.to_datetime(df['Date and Time'])[-buffer_length::-1],y=df['temp1'][-buffer_length::-1],mode='lines',name='air sensor'))
        fig.add_trace(go.Scatter(x=pd.to_datetime(df['Date and Time'])[-buffer_length::-1],y=df['temp2'][-buffer_length::-1],mode='lines',name='surface sensor'))
        last_updated = f"*{pd.to_datetime(datetime.datetime.now()).round('1s')}: the harvester is currently recharging its internal buffer; thus the system is in sleep mode and no recent readings are available.*"
    fig.update_layout(yaxis_title = 'Temperature [C]',xaxis_title='Time',hovermode = "x unified")
    return fig,last_updated

@callback(
    Output('data-download','data'),
    Input('download-button', 'n_clicks'),
    [State('n_points','value')],
    prevent_initial_call=True
)
def download_data(n,buffer_length):
    try:
        conn =  pymysql.connect(host=config('AWS_SQL_ENDPOINT'), user=config('AWS_SQL_USER'), passwd=config('AWS_SQL_PASSWORD'), port=3306, database='sensors')
        cur = conn.cursor()
        cur.execute('SELECT * FROM watteco_temp_2 ORDER BY timestamp DESC')
        results = cur.fetchmany(buffer_length)
        times = [results[i][0]+datetime.timedelta(hours=2) for i in range(len(results))]
        if (datetime.datetime.now(times[0].tzinfo)-times[0]).total_seconds() > 120: #check if data is current within the last 2 minutes
            last_updated = f"*{pd.to_datetime(datetime.datetime.now()).round('1s')}: the harvester is currently recharging its internal buffer; thus the system is in sleep mode and no recent readings are available.*"
        else:
            last_updated = f"*{pd.to_datetime(datetime.datetime.now()).round('1s')}: the harvester is powering the sensor and data collection is live*"
        temp1 = [results[i][1] for i in range(len(results))]
        temp2 = [results[i][2] for i in range(len(results))]
        df = pd.DataFrame({'Timestamp':times,'Temperature 1 [C]':temp1,'Temperature 2 [C]':temp2})
        return dcc.send_data_frame(df.to_csv, 'watteco_temp_2_export.csv')
    except Exception as e:
        raise PreventUpdate

@app.callback(Output('submit-div', 'children'),
     Input("button-submit", 'n_clicks'),
     [State("email-row", 'value'),
      State("name-row", 'value'),
      State("message-row", 'value')]
    )
def submit_message(n, email, name, message):
    content = f"Subject: New Message from Dashboard!\n\n Sender: {name} [{email}] \n\n {message}"
    if n>0:
        status = email_smtp.send(settings.email_recipients,content)
        if status == 'success':
            return [html.P("Message Sent")]
        else:
            return[dbc.Button('Submit', color = 'primary', id='button-submit', n_clicks=0)]
    else:
        raise PreventUpdate
if __name__ == '__main__':
    app.run(debug=True)