import dash
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
from styles import *

app = Dash(__name__,use_pages = True)

cabecalho = html.Div([
    dcc.Link('Início',style = nav,href = '/'),
    dcc.Link('Sobre mim',style = nav,href = 'about')
],style = cabecalho)

app.layout = html.Div([
    cabecalho,
    dash.page_container
],style = main_div)

if __name__ == '__main__':
    app.run(debug=True)