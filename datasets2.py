import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st



# Configuración de carpeta
folder_path = "datasets"  

os.makedirs(folder_path, exist_ok=True)  
# Crea la carpeta si no existe. 

# Generar datos base

product_names = np.random.choice(["Laptop", "Mouse", "Keyboard", "Monitor", "Printer","PS5","PS4","XBOX"], size=500, replace=True)  
# np.random.choice es una funcion que me permite escoger aleatoriamente entre los daros de la lista. También se pueden repetir
# np → numpy



prices = np.round(np.random.uniform(20.0, 2000.0, size=500), 2)  
# Genera 500 precios aleatorios entre 20 y 2000 con 2 decimales. np.uniform da float, round lo deja con 2 decimales
# round → redondea los decimales  np.round ( limite inferior, limite superior, size=numero de numeros, numero de decimales)
# random.uniform sigue una distribución normal (campana de Gauss)


quantities = np.random.choice([10, 20, 50, 100, 200, 50], size=500, replace=True)  
# Cantidad vendida. Elige aleatoriamente entre esos valores.

dates = pd.date_range(start="2023-01-01", end="2023-12-31", periods=500).strftime("%Y-%m-%d")  
# pd.date_range (). strftime ()
# Crea 500 fechas distribuidas uniformemente en todo 2023. strftime las convierte a string formato "2023-01-01"

# Crear DataFrame
data = {
    "product_name": product_names,
    "price": prices,
    "quantity_sold": quantities,
    "sale_date": dates,
}
df_large = pd.DataFrame(data)  
"""
df_large es solo el nombre de mi variable
pd.DataFrame es la funcion que junta todos los arrays en un DataFrame de pandas con 500 filas x 5 columnas
"""

# Guardar en un archivo CSV para reutilizarlo
output_path = os.path.join(folder_path, "large_sales_data.csv")  
# os.path.join arma la ruta completa. Como folder_path=".", queda "./large_sales_data.csv"

df_large.to_csv(output_path, index=False)  
# Guarda el DataFrame en CSV. index=False quita la columna de índice 0,1,2... que pandas agrega por defecto



""" 
Le pedí a Gemini que me grafique esta info

"""



# 1. Leemos el archivo que acabas de crear
ruta_archivo = "datasets/large_sales_data.csv"
df = pd.read_csv(ruta_archivo)

# 2. Creamos una columna nueva y súper útil: Ventas Totales (Precio x Cantidad)
# Esto es matemática pura aplicada a columnas enteras
df['total_revenue'] = df['price'] * df['quantity_sold']

# --- CONFIGURACIÓN VISUAL ---

# Le decimos a Seaborn que use su diseño moderno con cuadrícula de fondo
sns.set_theme(style="whitegrid")

# Creamos un "lienzo" grande (15 pulgadas de ancho x 6 de alto)
plt.figure(figsize=(15, 6))

# --- GRÁFICO 1: Ingresos por Producto (Barras) ---
# plt.subplot(filas, columnas, posición_del_gráfico)
plt.subplot(1, 2, 1) 

# Usamos la "Joya de la Corona" (groupby) para sumar el dinero por cada producto
ingresos = df.groupby('product_name')['total_revenue'].sum().reset_index()
# Ordenamos de mayor a menor para que el gráfico se vea profesional
ingresos = ingresos.sort_values('total_revenue', ascending=False)

# Dibujamos usando la paleta de colores 'viridis' que vimos antes
sns.barplot(data=ingresos, x='total_revenue', y='product_name', palette="viridis")
plt.title('Ingresos Totales por Producto', fontsize=14, fontweight='bold')
plt.xlabel('Ingresos ($)')
plt.ylabel('Producto')

# --- GRÁFICO 2: Distribución de Precios (Histograma) ---
plt.subplot(1, 2, 2)

# Un histograma agrupa los precios en "cajas" (bins=20) para ver cuáles son los más comunes
sns.histplot(data=df, x='price', bins=20, color='coral', kde=True)
plt.title('Distribución de los Precios', fontsize=14, fontweight='bold')
plt.xlabel('Precio del Producto ($)')
plt.ylabel('Frecuencia (Cantidad de veces)')

# --- TOQUES FINALES ---
# Esta función ajusta los espacios mágicamente para que los textos no se monten
plt.tight_layout()

# Nuestro interruptor final para mostrar la ventana
# plt.show() # Comentamos esto porque bloquea el código en la nube

# Usamos Streamlit para mostrar el gráfico en la web
st.pyplot(plt.gcf())


"""

Ahora le pedí a Gemini que publique esto en streamlit
"""



# 1. Le damos un título a tu página web
st.title("Mi Primer Dashboard de Ventas 🚀")

# 2. Leemos tu archivo CSV con Pandas
df = pd.read_csv("datasets/large_sales_data.csv")

# 3. INTERACTIVIDAD: Creamos un menú desplegable en la web
# df["product_name"].unique() saca una lista sin repetir de tus productos (PS5, Laptop, etc.)
producto_elegido = st.selectbox("Elige un producto para analizar:", df["product_name"].unique())

# 4. FILTRO: Usamos la lógica de comparación que ya dominas
df_filtrado = df[df["product_name"] == producto_elegido]

# 5. Mostramos la tabla filtrada en la pantalla
st.dataframe(df_filtrado)

