import dash
from dash import html,dcc
from styles import *

dash.register_page(__name__)

paragraph = '''Graduando em Engenharia de Controle e Automação (UFSC)
e técnico em eletrotécnica (IFSC), trabalho com mineração de dados, 
desenvolvimento de modelos de machine learning e modelos estatísticos de predição, 
além de desenvolvimento de APIs e interfaces.'''

layout = html.Div([
    html.Div([
            html.H1('Sobre mim',style = titulo),
            html.H2('Aruã Viggiano Souza',style = subtitulo),
            html.P(paragraph,style = intro)
        ],style = bloco_apresentacao),
    html.Div(
        html.Img(src = 'assets/arua.jpg',style = arua_img)
    ,style = arua_div)
    ],style = body_div)