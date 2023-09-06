from dash import html, dcc
import dash_bootstrap_components as dbc

LAYOUT = html.Div([
    #hidden components
    dcc.Interval(id='update_interval',interval=5000),
    #header
    dbc.Row([
            dbc.Col(html.Img(src='assets/logo.png',style={'width':'50%','display':'inline-block'})),
            dbc.Col(html.H1(children='Real-time sensing dashboard',style={'display':'inline-block'}))],
            style={'padding':'10'},className="g-0",justify="left"),
    #temperature graph
    dcc.Graph(id='temp-graph'),
    dcc.Markdown(id='last_updated',style={'padding':'10','font-size':'10px'}),
    dcc.Markdown(children=open('assets/tempgraph_description.md').read(),style={'padding':'10'})
])