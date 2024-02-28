import dash
from dash import html,dcc,Dash

app = Dash(__name__,use_pages = True,title = 'Aruã viggiano Souza',update_title = 'Carregando...',meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])

cabecalho = html.Div([
    html.Div([
        dcc.Link('Início',className = 'nav',href = '/'),
        dcc.Link('Biografia',className = 'nav',href = 'biografia')
    ],className = 'nav-div'),
    html.Div([
        html.A(
            html.Img(src = 'assets/linkedin.png',className = 'linkedin'),
        href = 'https://www.linkedin.com/in/aru%C3%A3-viggiano-souza/',className = 'links'),
        html.A(
            html.Img(src = 'assets/github.png',className = 'github'),
        href = 'https://github.com/aruasouza',className = 'links'),
    ],className = 'nav-div')],className = 'cabecalho')

app.layout = html.Div([
    cabecalho,
    dash.page_container
],className = 'main_div')