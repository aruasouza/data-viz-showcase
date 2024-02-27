import dash
from dash import html,dcc,Input, Output, callback
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

dash.register_page(__name__)

models = {'Regressão Linear':LinearRegression,
          'Árvore de Decisão':DecisionTreeRegressor,
          'Máquina de Vetor de Suporte':SVR
          }

df = px.data.iris().rename({'sepal_width':'Largura Sépala',
                            'sepal_length':'Comprimento Sépala',
                            'petal_width':'Largura Pétala',
                            'petal_length':'Comprimento Pétala',
                            'species':'Espécie'},axis = 1)
train,test = train_test_split(df,test_size = .3,random_state = 1)
names = ['Largura Sépala','Comprimento Sépala','Largura Pétala','Comprimento Pétala']

def regression(model,target,x1,x2):
    x = train[[x1,x2]].values
    y = train[target].values
    model.fit(x,y)
    return model

layout = html.Div([
    html.Div([
        html.Div([
                'Modelo',
                dcc.Dropdown(list(models.keys()),'Regressão Linear',id='model',className = 'dropdown_iris')
            ],className = 'div_dropdown'),
        html.Div([
                'Variável Alvo',
                dcc.Dropdown(names,names[2],id='target',className = 'dropdown_iris')
            ],className = 'div_dropdown'),
        html.Div([
                'Atributo "X"',
                dcc.Dropdown(names,names[0],id='x1',className = 'dropdown_iris')
            ],className = 'div_dropdown'),
        html.Div([
                'Atributo "Y"',
                dcc.Dropdown(names,names[1],id='x2',className = 'dropdown_iris')
            ],className = 'div_dropdown')
    ],className = 'selection_bar'),
    dcc.Graph(id = 'graph',className='graph')
])

@callback(
    Output(component_id='graph', component_property='figure'),
    Input(component_id='model', component_property='value'),
    Input(component_id='target', component_property='value'),
    Input(component_id='x1', component_property='value'),
    Input(component_id='x2', component_property='value')
)
def build_graph(model_name,target,x1,x2):
    hovertemplate = '<b>%{text}</b><br>' +\
                    f'{x1}: ' +\
                    '%{x}<br>' +\
                    f'{x2}: ' +\
                    '%{y}'
    hovertemplate_2 = '<b>%{z}</b><br>' +\
                    f'{x1}: ' +\
                    '%{x}<br>' +\
                    f'{x2}: ' +\
                    '%{y}'
    l = 100
    model = models[model_name]()
    model = regression(model,target,x1,x2)
    x1max,x1min = df[x1].max(),df[x1].min()
    x2max,x2min = df[x2].max(),df[x2].min()
    xx1,xx2 = np.linspace(x1min,x1max,100),np.linspace(x2min,x2max,100)
    x1mesh,x2mesh = np.meshgrid(xx1,xx2)
    z = np.concatenate([model.predict(np.concatenate((x1mesh[i].reshape(-1,1),x2mesh[i].reshape(-1,1)),axis = 1)) for i in range(l)]).reshape(-1,l)
    pred = [round(x,6) for x in model.predict(test[[x1,x2]].values)]
    fig = make_subplots(rows=2,cols=2,subplot_titles=("Treino","Modelo","Teste","Predição"),horizontal_spacing = 0.05,
    vertical_spacing = 0.15)
    fig.add_trace(go.Scatter(x = train[x1],
                             y = train[x2],
                             mode='markers',
                             marker=dict(color=train[target],coloraxis = 'coloraxis1'),
                             hovertemplate = hovertemplate,
                             text = train[target],
                             name = 'Treino'),row = 1,col = 1)
    fig.add_trace(go.Heatmap(x = xx1,
                             y = xx2,
                             z = z,
                             coloraxis='coloraxis1',
                             hovertemplate=hovertemplate_2,
                             name = 'Modelo'),row = 1,col = 2)
    fig.add_trace(go.Scatter(x = test[x1],
                             y = test[x2],
                             mode='markers',
                             marker=dict(color=test[target],coloraxis = 'coloraxis1'),
                             hovertemplate = hovertemplate,
                             text = test[target],
                             name = 'Teste'),row = 2,col = 1)
    fig.add_trace(go.Scatter(x = test[x1],
                             y = test[x2],
                             mode='markers',
                             marker=dict(color=pred,coloraxis = 'coloraxis1'),
                             hovertemplate = hovertemplate,
                             text = pred,
                             name = 'Predição'),row = 2,col = 2)
    fig.update_layout(showlegend = False,template="plotly_dark",margin=dict(l=100,r=100,b=70,t=200),
                      title=dict(text = "Predição de Características de Flores Iris",font = dict(size=20),y=.95,x=.07),
                      paper_bgcolor="#0E1116",plot_bgcolor='rgba(255,255,255,0.1)',coloraxis=dict(colorscale='RdBu'))
    return fig