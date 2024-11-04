import streamlit as st
import pandas as pd
import grafico_mapa as graf1
import graficos_lineas as graf2
import grafico_barras as graf3
import grafico_pizza as graf4


st.set_page_config(layout = 'wide')#actualiza la pagina de modo ancho

st.title('Dashboard de Ventas :shopping_trolley:')

def formata_numero(valor,prefijo = ''):
    for unidad in ['','k']:
        if valor < 1000:
            return f'{prefijo}{valor:.2f}{unidad}'
            
        valor /= 1000  

    return f'{prefijo} {valor:.2f} M'

#Habrimos las bases de datos

df_ventas = pd.read_csv("https://raw.githubusercontent.com/bruxly/sales_dashboard_streat/main/base_ventas.csv")
df_ventas['valor_total'] = (df_ventas.price * df_ventas.cantidad_itens) + (df_ventas.freight_value * df_ventas.cantidad_itens)
df_ventas['order_purchase_timestamp'] = pd.to_datetime(df_ventas['order_purchase_timestamp'])
df_ventas['tipo_producto'] = df_ventas['product_category_name'].str.split('_').str[0]#en la barra de top ingresos por productos los nombres que tienen guion solo nos quedamos con el primer nombre del producto eliminando los nombres despues del primer guion

#Configuración de filtros
st.sidebar.image('logo_Domiray.jpg',)
st.sidebar.title('Filtros')

estados = sorted(list(df_ventas['geolocation_state'].unique()))
ciudades = st.sidebar.multiselect('Estados',estados)#muestra en orden alfabetico todos los estados en filtros

productos = sorted(list(df_ventas['tipo_producto'].dropna().unique()))
#adiciono elementos a una lista productos
productos.insert(0,'Todos')

producto = st.sidebar.selectbox('Productos',productos)

años = st.sidebar.checkbox('Todo el periodo', value=True)#el cliente puede interactuar con los años
if not años:
    año = st.sidebar.slider('Año',df_ventas['order_purchase_timestamp'].dt.year.min(),df_ventas['order_purchase_timestamp'].dt.year.max())

#filtranso lo datos
#damos interactividad a los datos, cuando el cliente manipula los datos la informacion va cambiando
if ciudades:
    df_ventas = df_ventas[df_ventas['geolocation_state'].isin(ciudades)]
if producto != 'Todos':
    df_ventas = df_ventas[df_ventas['tipo_producto'] == producto]

if not años:
    df_ventas = df_ventas[df_ventas['order_purchase_timestamp'].dt.year == año]



#llamar a los graficos
graf_mapa = graf1.crear_grafico(df_ventas)
graf_lineas = graf2.crear_grafico(df_ventas)
graf_barras = graf3.crear_grafico(df_ventas)
graf_pizza = graf4.crear_grafico(df_ventas)


col1,col2 = st.columns(2)

with col1:
    st.metric('**Total de Revenues**',formata_numero(df_ventas['valor_total'].sum(),'$'))
    st.plotly_chart(graf_mapa,use_container_width=True)
    st.plotly_chart(graf_barras, use_container_width=True)


with col2:
    st.metric('**Total Ventas**',formata_numero(df_ventas['cantidad_itens'].sum()))
    st.plotly_chart(graf_lineas,use_continer_width=True)
    st.plotly_chart(graf_pizza,use_container_width=True)

