import dash
from dash import html,dcc

dash.register_page(__name__, path='/')

layout = html.Div([
        html.Div([
            html.H1('Aruã Viggiano Souza',className = 'titulo'),
            html.H2('Cientista de Dados',className = 'subtitulo'),
            html.P('Demostração de visualisações de dados e aprendizado de máquina.',className = 'intro')
        ],className = 'bloco_apresentacao'),
        html.Div([
            dcc.Link([
                html.Img(src = 'assets/topografia-brasil.png',className = 'graph_img'),
                html.P('Topografia Brasil')
                ],className = 'graph_button',href = 'topografia'),
            dcc.Link([
                html.Img(src = 'assets/economia-brasil.png',className = 'graph_img'),
                html.P('Economia Brasil')
                ],className = 'graph_button',href = 'economia'),
            dcc.Link([
            html.Img(src = 'assets/iris.png',className = 'graph_img'),
            html.P('Iris Regressão')
            ],className = 'graph_button',href = 'iris'),
            dcc.Link([
            html.Img(src = 'assets/montecarlo.png',className = 'graph_img'),
            html.P('Simulação de Montecarlo')
            ],className = 'graph_button',href = 'montecarlo')
        ],className = 'bloco_graficos')
    ],className = 'body_div')