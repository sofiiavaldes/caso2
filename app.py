import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Cargar datos de cambio de dólar
cambio_dols = pd.read_csv('cambio_dols.csv')
cambio_dols = cambio_dols.set_index('Fecha')

# Cargar datos de inflación
inflacion = pd.read_csv('inflacion.csv')
inflacion = inflacion.set_index('Periodo')
# Filtrar las columnas de los años 2019 al 2023
inflacion = inflacion[['2019', '2020', '2021', '2022', '2023']]

# Cargar datos de IMAE
imae = pd.read_csv('imae.csv')
imae = imae.set_index('Período')

# Crear gráfico interactivo de cambio de dólar
fig_cambio_dols = px.line(cambio_dols, x=cambio_dols.index, y=cambio_dols.columns,
                         title='Cambio de Dólar por Mes')
fig_cambio_dols.update_xaxes(title_text='Fecha')
fig_cambio_dols.update_yaxes(title_text='Tipo de Cambio')

# Crear gráfico interactivo de inflación
fig_inflacion = go.Figure()
for col in inflacion.columns:
    fig_inflacion.add_trace(go.Scatter(x=inflacion.index, y=inflacion[col], mode='lines',
                                      name=str(col)))

fig_inflacion.update_layout(title='Inflación por Mes (2019 - 2023)',
                            xaxis_title='Fecha',
                            yaxis_title='Tasa de Inflación')

# Crear gráfico interactivo de IMAE
fig_imae = go.Figure()
fig_imae.add_trace(go.Bar(x=imae.index, y=imae['Var. % interanual'], name='Var. % interanual'))
fig_imae.update_layout(title='IMAE - Var. % Interanual vs. Var. % Acumulada',
                      xaxis_title='Período',
                      yaxis_title='Valor')
fig_imae.update_xaxes(categoryorder='total ascending')

# Crear panel interactivo de Dash
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server=app.server

app.layout = html.Div([
    dcc.Graph(figure=fig_cambio_dols),
    dcc.Graph(figure=fig_inflacion),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'Gráfico de Cambio de Dólar', 'value': 'cambio_dols'},
            {'label': 'Gráfico de Inflación', 'value': 'inflacion'},
            {'label': 'Gráfico de IMAE', 'value': 'imae'}
        ],
        value='cambio_dols'
    ),
    dcc.Graph(id='selected-graph'),
    dcc.RadioItems(
        id='imae-radio',
        options=[
            {'label': 'Var. % Interanual', 'value': 'Var. % interanual'},
            {'label': 'Var. % Acumulada', 'value': 'Var. % acumulada'}
        ],
        value='Var. % interanual',
        labelStyle={'display': 'block'}
    ),
    dcc.Graph(id='imae-graph')
])

@app.callback(
    Output('selected-graph', 'figure'),
    Input('dropdown', 'value')
)
def update_graph(selected_value):
    if selected_value == 'cambio_dols':
        return fig_cambio_dols
    elif selected_value == 'inflacion':
        return fig_inflacion
    elif selected_value == 'imae':
        return fig_imae

@app.callback(
    Output('imae-graph', 'figure'),
    Input('imae-radio', 'value')
)
def update_imae_graph(selected_value):
    if selected_value == 'Var. % interanual':
        return go.Figure(data=[go.Bar(x=imae.index, y=imae['Var. % interanual'])], 
                        layout={'title': 'IMAE - Var. % Interanual'})
    elif selected_value == 'Var. % acumulada':
        return go.Figure(data=[go.Bar(x=imae.index, y=imae['Var. % acumulada'])], 
                        layout={'title': 'IMAE - Var. % Acumulada'})

if __name__ == '__main__':
    app.run_server(debug=False, host='0.0.0.0',port=10000)
