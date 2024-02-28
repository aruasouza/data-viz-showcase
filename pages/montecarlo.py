import dash
from dash import html,dcc
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from scipy.optimize import curve_fit
import math
import warnings

def square(x,a,b,c):
    return x ** 2 * a + x * b + c
def wave(x,a,b,c,d,e,f,g,h,i,j):
    return a * np.sin(x * 2 * math.pi / 12) + b * np.cos(x * 2 * math.pi / 12) +\
        c * np.sin(x * 2 * math.pi / 6) + d * np.cos(x * 2 * math.pi / 6) +\
        e * np.sin(x * 2 * math.pi / 4) + f * np.cos(x * 2 * math.pi / 4) +\
        g * np.sin(x * 2 * math.pi / 3) + h * np.cos(x * 2 * math.pi / 3) +\
        i * np.sin(x * 2 * math.pi / 2) + j * np.cos(x * 2 * math.pi / 2)
def simulate(size,mean,std):
    return np.cumsum(np.random.normal(mean,std,size))
def serie_f(x,trend,seazon):
    seazonal_component = wave(x,*seazon)
    trend_component = square(x,*trend)
    return np.exp(seazonal_component + trend_component)

df = pd.read_csv('AirPassengers.csv')
df['Month'] = pd.to_datetime(df['Month'])
df['Log'] = np.log(df['#Passengers'])
x = np.array(df.index)
y = df['Log'].values
trend,pcov = curve_fit(square,x,y)
df['Log Trend'] = square(x,*trend)
df['Trend'] = np.exp(df['Log Trend'])
df['Static'] = df['Log'] - df['Log Trend']
with warnings.catch_warnings(action="ignore"):
    seazon,pcov = curve_fit(wave,x,df['Static'].values)
df['Wave'] = wave(x,*seazon)
df['Seazon'] = np.exp(df['Wave'] + df['Log Trend'].mean())
df['Prediction'] = serie_f(x,trend,seazon)
df['Noise'] = df['#Passengers'] - df['Prediction']
mean,std = df['Noise'].mean(),df['Noise'].std()

predrange = 24
predstart = df.index[-1] + 1
xpred = np.arange(predstart,predstart + predrange)
pred = pd.Series(serie_f(xpred,trend,seazon),xpred)
dates_pred = pd.date_range(df['Month'].iloc[-1],freq = 'm',periods = predrange + 1)[1:]
minimo,maximo = df['#Passengers'].min(),df['#Passengers'].max()
space = (maximo - minimo) / 2
mean,std = df['Noise'].mean(),df['Noise'].std()
simulations = pd.DataFrame({i:pred + simulate(predrange,mean,std) for i in range(1000)},index = xpred)
median = simulations.median(axis = 1)
q25 = simulations.quantile(0.25,axis = 1)
q05 = simulations.quantile(0.05,axis = 1)
q75 = simulations.quantile(0.75,axis = 1)
q95 = simulations.quantile(0.95,axis = 1)
hovertemplate =\
    '<b>%{x}</b>'+\
    '<br>%{y}'

fig = make_subplots(
    rows=4,cols=2,shared_xaxes = True,vertical_spacing=0.1,horizontal_spacing=0.03, 
    specs=[[{},{'rowspan': 2}],[{},None],[{},{'rowspan': 2}],[{},None]],
    subplot_titles=("Série Original","Simulação de Monte Carlo","Tendência","Sazonalidade","Cenários","Ruído"))

fig.add_trace(go.Scatter(x = df['Month'],y = df['#Passengers'],mode = 'lines',line=dict(color='rgb(95, 158, 160)'),
                         name = 'Série',hovertemplate = hovertemplate),row = 1,col = 1)
fig.add_trace(go.Scatter(x = df['Month'],y = df['Trend'],mode = 'lines',line=dict(color='rgb(95, 158, 160)'),
                         name = 'Tendência',hovertemplate = hovertemplate),row = 2,col = 1)
fig.add_trace(go.Scatter(x = df['Month'],y = df['Seazon'],mode = 'lines',line=dict(color='rgb(95, 158, 160)'),
                         name = 'Sazonalidade',hovertemplate = hovertemplate),row = 3,col = 1)
fig.add_trace(go.Scatter(x = df['Month'],y = df['Noise'],mode = 'lines',line=dict(color='rgb(95, 158, 160)'),
                         name = 'Ruído',hovertemplate = hovertemplate),row = 4,col = 1)
fig.add_trace(go.Scatter(x = df['Month'],y = df['#Passengers'],mode = 'lines',line=dict(color='rgb(95, 158, 160)'),
                         name = 'Série',hovertemplate = hovertemplate),row = 1,col = 2)
for i in range(200):
    fig.add_trace(go.Scatter(x = dates_pred,y = simulations[i],mode = 'lines',hoverinfo = 'skip',
                             line=dict(color='rgba(255,255,0,0.1)', width=1)),row = 1,col = 2)

fig.add_trace(go.Scatter(x = df['Month'],y = df['#Passengers'],mode = 'lines',line=dict(color='rgb(95, 158, 160)'),
                         name = 'Série',hovertemplate = hovertemplate),row = 3,col = 2)
fig.add_trace(go.Scatter(x = dates_pred,y = q05,mode = 'lines',line=dict(color='lightgray',width=1),
                         name = 'Percentil 5%',hovertemplate = hovertemplate),row = 3,col = 2)
fig.add_trace(go.Scatter(x = dates_pred,y = q25,mode = 'lines',line=dict(color='darkgray',width=1),
                         name = 'Percentil 25%',hovertemplate = hovertemplate,fill = 'tonexty',fillcolor='lightgray'),row = 3,col = 2)
fig.add_trace(go.Scatter(x = dates_pred,y = median,mode = 'lines',line=dict(color='black',width=1),
                         name = 'Mediana',hovertemplate = hovertemplate,fill='tonexty',fillcolor = 'darkgray'),row = 3,col = 2)
fig.add_trace(go.Scatter(x = dates_pred,y = q75,mode = 'lines',line=dict(color='darkgray',width=1),
                         name = 'Percentil 75%',hovertemplate = hovertemplate,fill='tonexty',fillcolor = 'darkgray'),row = 3,col = 2)
fig.add_trace(go.Scatter(x = dates_pred,y = q95,mode = 'lines',line=dict(color='lightgray',width=1),
                         name = 'Percentil 95%',hovertemplate = hovertemplate,fill = 'tonexty',fillcolor = 'lightgray'),row = 3,col = 2)

med_2 = np.median(df['Trend'])
med_3 = np.median(df['Seazon'])
med_4 = np.median(df['Noise'])
fig.update_yaxes(range=[minimo,maximo],showticklabels = False,row = 1,col = 1)
fig.update_yaxes(range=[med_2 - space,med_2 + space],showticklabels = False,row = 2,col = 1)
fig.update_yaxes(range=[med_3 - space,med_3 + space],showticklabels = False,row = 3,col = 1)
fig.update_yaxes(range=[med_4 - space,med_4 + space],showticklabels = False,row = 4,col = 1)
fig.update_yaxes(showticklabels = False,row = 1,col = 2)
fig.update_yaxes(showticklabels = False,row = 3,col = 2)
fig.update_layout(showlegend = False,template="plotly_dark",
                      paper_bgcolor="#0E1116",plot_bgcolor='rgba(255,255,255,0.1)',margin=dict(l=0,r=0,b=0,t=20))


dash.register_page(__name__)

layout = html.Div(
    [
        html.H2('Série Temporal com Simulação de Montecarlo',className = 'graph-title'),
        dcc.Graph(figure=fig,className = 'graph')
    ]
)