import dash
from dash import html,dcc
from styles import *

dash.register_page(__name__, path='/')

layout = html.Div([
        html.Div([
            html.H1('Aruã Viggiano Souza',style = titulo),
            html.H2('Cientista de Dados',style = subtitulo),
            html.P('Demostração de visualisações de dados e aprendizado de máquina.',style = intro)
        ],style = bloco_apresentacao),
        html.Div([
            dcc.Link([
                html.Img(src = 'assets/topografia-brasil.png',style = graph_img),
                html.P('Topografia Brasil')
                ],style = graph_button,href = 'topografia'),
            dcc.Link([
                html.Img(src = 'assets/economia-brasil.png',style = graph_img),
                html.P('Economia Brasil')
                ],style = graph_button,href = 'economia'),
            dcc.Link([
            html.Img(src = 'assets/iris.png',style = graph_img),
            html.P('Iris Regressão')
            ],style = graph_button,href = 'iris')
        ],style = bloco_graficos)
    ],style = body_div)