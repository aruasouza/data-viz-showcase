import dash
from dash import html,dcc
import pandas as pd
from bcb import sgs,Expectativas
from datetime import date,timedelta
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def load_data_local():
    pib = pd.read_csv('dados_economicos/pib.csv',index_col=0)
    ipca = pd.read_csv('dados_economicos/ipca.csv',index_col=0)
    selic = pd.read_csv('dados_economicos/selic.csv',index_col=0)
    pib_exp = pd.read_csv('dados_economicos/pib_exp.csv',index_col=0)
    ipca_exp = pd.read_csv('dados_economicos/ipca_exp.csv',index_col=0)
    selic_exp = pd.read_csv('dados_economicos/selic_exp.csv',index_col=0)
    return pib,ipca,selic,pib_exp,ipca_exp,selic_exp

def get_exp(var,ep):
    df = ep.query()\
    .filter(ep.Indicador == var)\
    .filter(ep.Data >= date.today() - timedelta(days = 30))\
    .filter(ep.baseCalculo == 0)\
    .select(ep.Data, ep.DataReferencia, ep.Minimo, ep.Maximo, ep.Mediana)\
    .collect()
    menor_data = df['Data'].min()
    return df.loc[df['Data'] == menor_data].drop('Data',axis = 1).set_index('DataReferencia')

def refresh_data():
    ano_atual = date.today().year
    pib = sgs.get({'PIB':7326},last = 20)
    pib['Ano'] = pib.index.year
    pib = pib.set_index('Ano')
    ipca = sgs.get({'IPCA':13522},last = 240)
    ipca['Ano'] = ipca.index.year
    ipca = ipca.drop_duplicates('Ano',keep = 'last').set_index('Ano').drop(ano_atual)
    selic = sgs.get({'SELIC':1178},last = int(20 * 252))
    selic['Ano'] = selic.index.year
    selic = selic.drop_duplicates('Ano',keep = 'last').set_index('Ano').drop(ano_atual)
    em = Expectativas()
    ep = em.get_endpoint('ExpectativasMercadoAnuais')
    ipca_exp = get_exp('IPCA',ep)
    pib_exp = get_exp('PIB Total',ep)
    selic_exp = get_exp('Selic',ep)
    pib.to_csv('dados_economicos/pib.csv')
    ipca.to_csv('dados_economicos/ipca.csv')
    selic.to_csv('dados_economicos/selic.csv')
    pib_exp.to_csv('dados_economicos/pib_exp.csv')
    ipca_exp.to_csv('dados_economicos/ipca_exp.csv')
    selic_exp.to_csv('dados_economicos/selic_exp.csv')
    print('Dados econômicos atualizados')
    return pib,ipca,selic,pib_exp,ipca_exp,selic_exp

def load_data():
    last_ref = open('dados_economicos/last_refresh','r').read().split('-')
    last_date = date(*[int(n) for n in last_ref])
    if (date.today() - last_date).days >= 7:
        try:
            data = refresh_data()
            with open('dados_economicos/last_refresh','w') as f:
                f.write(str(date.today()))
            return data
        except:
            print('Erro ao atualizar dados econômicos')
            return load_data_local()
    return load_data_local()

def build_figure():
    pib,ipca,selic,pib_exp,ipca_exp,selic_exp = load_data()
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"colspan": 2}, None],[{}, {}]],
        subplot_titles=("PIB","IPCA", "SELIC"),
        horizontal_spacing = 0.05,
        vertical_spacing = 0.15)

    fig.add_trace(go.Bar(x = pib.index,y = pib['PIB'],name = 'PIB',marker_color='rgb(55, 83, 109)',hovertemplate="%{y}%"),row = 1,col = 1)
    fig.add_trace(go.Scatter(x = pib_exp.index,y = pib_exp['Maximo'],name = 'Proj. Maxima',marker_color='orange',hovertemplate="%{y}%"),row = 1,col = 1)
    fig.add_trace(go.Scatter(x = pib_exp.index,y = pib_exp['Mediana'],name = 'Proj. Mediana',marker_color='orange',hovertemplate="%{y}%"),row = 1,col = 1)
    fig.add_trace(go.Scatter(x = pib_exp.index,y = pib_exp['Minimo'],name = 'Proj. Minima',marker_color='orange',hovertemplate="%{y}%"),row = 1,col = 1)
    fig.add_trace(go.Bar(x = ipca.index,y = ipca['IPCA'],name = 'IPCA',marker_color='rgb(55, 83, 150)',hovertemplate="%{y}%"),row = 2,col = 1)
    fig.add_trace(go.Scatter(x = ipca_exp.index,y = ipca_exp['Maximo'],name = 'Proj. Maxima',marker_color='coral',hovertemplate="%{y}%"),row = 2,col = 1)
    fig.add_trace(go.Scatter(x = ipca_exp.index,y = ipca_exp['Mediana'],name = 'Proj. Mediana',marker_color='coral',hovertemplate="%{y}%"),row = 2,col = 1)
    fig.add_trace(go.Scatter(x = ipca_exp.index,y = ipca_exp['Minimo'],name = 'Proj. Minima',marker_color='coral',hovertemplate="%{y}%"),row = 2,col = 1)
    fig.add_trace(go.Bar(x = selic.index,y = selic['SELIC'],name = 'SELIC',marker_color='rgb(0, 83, 109)',hovertemplate="%{y}%"),row = 2,col = 2)
    fig.add_trace(go.Scatter(x = selic_exp.index,y = selic_exp['Maximo'],name = 'Proj. Maxima',marker_color='gold',hovertemplate="%{y}%"),row = 2,col = 2)
    fig.add_trace(go.Scatter(x = selic_exp.index,y = selic_exp['Mediana'],name = 'Proj. Mediana',marker_color='gold',hovertemplate="%{y}%"),row = 2,col = 2)
    fig.add_trace(go.Scatter(x = selic_exp.index,y = selic_exp['Minimo'],name = 'Proj. Minima',marker_color='gold',hovertemplate="%{y}%"),row = 2,col = 2)

    fig.update_layout(showlegend=False,hovermode='x unified',template="plotly_dark",margin=dict(l=100,r=100,b=70,t=100),
                      title=dict(text = "Economia Brasil",font = dict(size=20),y=.95,x=.07),
                      paper_bgcolor="#0E1116",plot_bgcolor='rgba(255,255,255,0.1)')
    return fig

dash.register_page(__name__)

layout = html.Div(
    dcc.Graph(figure=build_figure(),className = 'graph')
)