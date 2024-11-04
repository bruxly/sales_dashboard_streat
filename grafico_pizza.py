import pandas as pd
import plotly.express as px

def crear_grafico(df):
    df_reviewn= df.groupby('review_score').agg(
        total_ventas = ('cantidad_itens','sum'),

    ).reset_index()

    colors = ['#0077b6','#1A4D83','#D63970','#2f567D','#4B6A92']
    fig = px.pie(df_reviewn,
        values = 'total_ventas',
        names = 'review_score',
        title = 'Calificación de las Ventas',
        color_discrete_sequence = colors

    )

    fig.update_layout(yaxis_title = 'Calificacón', xaxis_title='Ventas', showlegend=False)
    fig.update_traces(textposition = 'inside',textinfo = 'percent+label', insidetextfont=dict(size=16))
    return fig
