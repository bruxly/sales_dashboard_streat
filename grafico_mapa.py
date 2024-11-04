import pandas as pd
import plotly.express as px

def crear_grafico(df):
    df_mapa = df.groupby('geolocation_state').agg({
        'valor_total':'sum',
        'geolocation_lat': 'mean',
        'geolocation_lng':'mean'
    }).reset_index().sort_values(by='valor_total',ascending=False)

    #creo el mapa
    graf_mapa = px.scatter_geo(df_mapa,
        lat ='geolocation_lat',
        lon = 'geolocation_lng',
        scope = 'south america',#solo me muestra america
        template = 'seaborn',#color del mapa
        size = 'valor_total',#tamaño de los puntos de los estados
        hover_name = 'geolocation_state',#muestra el nombre del estado
        hover_data = {'geolocation_lat': False,'geolocation_lng': False},#oculta las coordenadas
        title = 'Ingresos por estado'

    )
    return graf_mapa
