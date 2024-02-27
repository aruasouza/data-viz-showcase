import dash
from dash import html

dash.register_page(__name__)

paragraph = '''
Aruã nasceu em 1999 na cidade de Florianópolis e em 2023 casou-se com Bruna Gengnagel Souza.
\nÉ formado em eletrotécnica pelo Instituto Federal se Santa Catarina (2018) e atualmente é
graduando em Engenharia de Controle e Automação pela Universidade Federal de Santa Catarina.
\nEm 2022 começou a trabalhar com ciência de dados e análise de dados, área na qual segue atuando, 
desenvolvendo modelos de machine learning e modelos estatísticos de predição, 
além de APIs e interfaces gráficas.'''

def intersperse(lst,item):
    result = [item] * (len(lst) * 2 - 1)
    result[0::2] = lst
    return result

layout = html.Div([
    html.Div([
            html.H1('Biografia',className = 'titulo'),
            html.H2('Aruã Viggiano Souza',className = 'subtitulo'),
            html.P(intersperse(paragraph.split('\n'),html.Br()),className = 'intro')
        ],className = 'bloco_apresentacao'),
    html.Div(
        html.Img(src = 'assets/arua.jpg',className = 'arua_img')
    ,className = 'arua_div')
    ],className = 'body_div')