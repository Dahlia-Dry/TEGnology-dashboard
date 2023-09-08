from dash import html, dcc
import dash_bootstrap_components as dbc

LAYOUT = html.Div([
    #hidden components
    dcc.Interval(id='update_interval',interval=5000),
    #header
    dbc.Row([
            dbc.Col([html.Img(src='assets/logo.png',style={'width':'100%'})],width=3),
            dbc.Col([html.H1(children='Real-time sensing dashboard')],width=9)],
            style={'padding':10}),
    #temperature graph
    dcc.Graph(id='temp-graph'),
    html.Div([
        dcc.Markdown('Number of data points:'),
        dcc.Input(id='n_points',type='number',value=100)],className ="d-grid gap-2 d-md-flex",style={'padding':10}),
    dcc.Markdown(id='last_updated',style={'padding':10,'font-size':'10px'}),
    dbc.Row([
        dbc.Col([html.Img(src='assets/setup.jpeg',style={'width':'100%'})],width=4),
        dbc.Col([dcc.Markdown(children=open('assets/tempgraph_description.md').read())],width=8)],
        style={'padding':10}),
])