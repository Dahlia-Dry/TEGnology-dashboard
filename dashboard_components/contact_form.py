import dash_bootstrap_components as dbc
from dash import html, dcc

email_input = dbc.Row([
        dbc.Label("Email"
                , html_for="email-row"
                , width=2),
        dbc.Col(dbc.Input(
                type="email"
                , id="email-row"
                , placeholder="Enter email"
            ),width=10,
        )],className="mb-3"
)
name_input = dbc.Row([
        dbc.Label("Name", html_for="name-row", width=2),
        dbc.Col(
            dbc.Input(
                type="text"
                , id="name-row"
                , placeholder="Enter name"
                , maxLength = 80
            ),width=10
        )], className="mb-3"
)
message = dbc.Row([
        dbc.Label("Message"
         , html_for="message-row", width=2)
        ,dbc.Col(
            dbc.Textarea(id = "message-row"
                , className="mb-3"
                , placeholder="Enter message"
                , required = True)
            , width=10)
        ], className="mb-3")

contact_form = html.Div([ dbc.Container([
            html.H2("Want to learn more? We'd love to hear from you!"),
            dbc.Card(
                dbc.CardBody([
                     dbc.Form([name_input,email_input,message])
                ,html.Div(id = 'submit-div', children = [
                    dbc.Button('Submit'
                    , color = 'primary'
                    , id='button-submit'
                    , n_clicks=0)
                ]) 
                ])
            )
        ])
        ])

