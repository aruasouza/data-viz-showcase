import dash
from dash import html,dcc
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

dash.register_page(__name__)

relevo = pd.read_csv('relevo.csv')
wide = relevo.pivot_table(values = 'z',index = 'y',columns = 'x')

def build_graph():
    red = np.linspace(0,1000,256,dtype = 'int')
    red[red > 200] = 200
    green = np.linspace(150,0,256,dtype = 'int')
    blue = np.ones(256,dtype = 'int') * 0
    vals = np.linspace(0,1,256)
    colorscale = [[vals[i],f'rgb({red[i]}, {green[i]}, {blue[i]})'] for i in range(len(vals))]
    camera = dict(
    eye=dict(x=0., y=-0.1, z=1.5))
    fig = go.Figure(go.Surface(y = wide.index,x = wide.columns,z = wide.values,colorscale = colorscale))
    fig.update_layout(scene_camera=camera,template="plotly_dark",margin=dict(l=100,r=100,b=70,t=100),
                      title=dict(text = "Topografia Brasil",font = dict(size=20),y=.95,x=.07),
                      paper_bgcolor="#0E1116",plot_bgcolor='rgba(255,255,255,0.1)')
    return fig


layout = html.Div(
    dcc.Graph(figure = build_graph(),className = 'graph')
)