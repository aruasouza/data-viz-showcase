import dash
from dash import html, dcc, Dash
from styles import *

app = Dash(__name__,use_pages = True,meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])

cabecalho = html.Div([
    dcc.Link('Início',style = nav,href = '/'),
    dcc.Link('Sobre mim',style = nav,href = 'about'),
    html.Div(style = middle_div),
    html.A(
        html.Img(src = 'assets/linkedin.png',style = linkedin),
    href = 'https://www.linkedin.com/in/aru%C3%A3-viggiano-souza/',style = links),
    html.A(
        html.Img(src = 'assets/github.png',style = github),
    href = 'https://github.com/aruasouza',style = links),
    ],style = cabecalho)

app.layout = html.Div([
    cabecalho,
    dash.page_container
],style = main_div)