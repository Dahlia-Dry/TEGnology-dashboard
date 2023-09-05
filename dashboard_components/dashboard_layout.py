from dash import html, dcc

LAYOUT = html.Div([
    html.H1(children='TEGnology real-time sensing dashboard', style={'textAlign':'center'}),
    dcc.Graph(id='temp-graph'),
    dcc.Interval(id='update_interval',interval=5000),
    dcc.Markdown(id='last_updated')
])