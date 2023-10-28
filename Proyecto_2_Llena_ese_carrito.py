# %% [markdown]
# # Paso 1. Descripción de los datos
# 
# Lee los archivos de datos (`/datasets/instacart_orders.csv`, `/datasets/products.csv`, `/datasets/aisles.csv`, `/datasets/departments.csv` y `/datasets/order_products.csv`) con `pd.read_csv()` usando los parámetros adecuados para leer los datos correctamente. Verifica la información para cada DataFrame creado.
# 

# %% [markdown]
# ## Plan de solución
# 
# Escribe aquí tu plan de solución para el Paso 1. Descripción de los datos.

# %%
# importar librerías
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# %%
# leer conjuntos de datos en los DataFrames
# el separador de los datos es ';', por lo que se se usa el parámetro sep= ';'
df_instacart_orders = pd.read_csv('files/datasets/instacart_orders.csv', sep= ';') 
df_products = pd.read_csv('files/datasets/products.csv', sep= ';')
df_order_products = pd.read_csv('files/datasets/order_products.csv', sep= ';')
df_aisles = pd.read_csv('files/datasets/aisles.csv', sep= ';')
df_departments = pd.read_csv('files/datasets/departments.csv', sep= ';')

# %%
# mostrar información del DataFrame instacart_orders
df_instacart_orders.info()

# %%
# mostrar información del DataFrame products
df_products.info()

# %%
# mostrar información del DataFrame order_products
# Se emplea el parámetro show_counts=True, ya que contiene muchas filas de datos y se requiere que se muestren los recuentos
df_order_products.info(show_counts=True)

# %%
# mostrar información del DataFrame
df_aisles.info()

# %%
# mostrar información del DataFrame
df_departments.info()

# %% [markdown]
# ## Conclusiones
# 
# Los archivos de los datos a pesar que tienen una extensión csv, el separador es un ``';'``, por ello se usó el parámetro ``sep= ';'``.
# 
# El DatraFrame ``df_instacart``_orders únicamnete la columna days_since_prior_order tiene datos nulos.  
# El DatraFrame ``df_products`` únicamnete la columna product_name tiene datos nulos.  
# El DatraFrame ``order_products`` únicamnete la columna add_to_cart_order tiene datos nulos.  
# No hay datos nulos en DataFrame ``df_aisles``.  
# Tampoco hay datos nulos en DataFrame ``df_departments``.  
# 
# En los siguientes pasos se procesarán los datos ausentes, además de analizar si hay datos duplicados.

# %% [markdown]
# # Paso 2. Preprocesamiento de los datos
# 
# Preprocesa los datos de la siguiente manera:
# 
# - Verifica y corrige los tipos de datos (por ejemplo, asegúrate de que las columnas de ID sean números enteros).
# - Identifica y completa los valores ausentes.
# - Identifica y elimina los valores duplicados.
# 
# Asegúrate de explicar qué tipos de valores ausentes y duplicados encontraste, cómo los completaste o eliminaste y por qué usaste esos métodos. ¿Por qué crees que estos valores ausentes y duplicados pueden haber estado presentes en el conjunto de datos?

# %% [markdown]
# ## Plan de solución
# 
# Escribe aquí tu plan para el Paso 2. Preprocesamiento de los datos.  
# <span style="color:darkgreen">
# Primero se buscarán los valores duplicados en cada DataFrame. Para esto se empleará el método ``duplicated()`` en combinación con ``sum()``. Después se usará el método ``drop_duplicates()`` con ``reset_index(drop=True)`` para reiniciar el índice después de eliminar los duplicados.
# Posteriormente en las columnas de cada DataFrame también se buscarán los valores ausentes con el método ``isna()`` con ``sum()``. Se evaluarán estos datos ausentes para determinar con cuál valor reemplazarlos cuando sea pertinente.  
# También se revisará el tipo de dato para cada columna, esto se puede hacer con el método ``info()`` o con el atributo ``dtypes``. En donde sea necesario el tipo de dato se cambiará con el método ``astype()`` o si es necesario el método ``to_numeric()``
# </span>. 

# %% [markdown]
# ## Encuentra y elimina los valores duplicados (y describe cómo tomaste tus decisiones).

# %% [markdown]
# ### `orders` data frame

# %%
# Revisa si hay pedidos duplicados
# contar duplicados explícitos para el DataFrame df_instacart_orders
# uso del método duplicated() con sum()
df_instacart_orders.duplicated().sum()

# %%
# Se filtra el DataFrame con los valores duplicado
df_instacart_orders[df_instacart_orders.duplicated()]

# %% [markdown]
# ¿Tienes líneas duplicadas? Si sí, ¿qué tienen en común?  
# <span style="color:darkgreen">
#     Si, hay 15 datos o líneas duplicadas de acuerdo al resultado después de aplicar el método duplicated() y sum() al DataFrame (``df_instacart_orders.duplicated().sum()``).  
#     Después de filtrar el DataFrame solo con los valores duplicados se observa que el día (``order_dow``) y la hora (``order_hour_of_day``) en la que se hizo el pedido son los mismos valores en las líneas duplicadas.
# </span>.  

# %%
# Basándote en tus hallazgos,
# Verifica todos los pedidos que se hicieron el miércoles a las 2:00 a.m.
df_instacart_orders[(df_instacart_orders['order_dow'] == 3) & (df_instacart_orders['order_hour_of_day'] == 2)]

# %% [markdown]
# ¿Qué sugiere este resultado?  
# <span style="color:darkgreen">
# El resultado podría sugerir que los duplicados ocurrieron probablemente a un error de captura, ya que es un horario nocturno y el factor del cansancio pudo haber influenciado para que se cometiera un error humano.
# </span>.  

# %%
# Elimina los pedidos duplicados
# Ahora estos 15 valores duplicados se eliminarán con el método drop_duplicates con reset_index(drop=True) 
# para eliminar los duplicados y reiniciar los índices
df_instacart_orders = df_instacart_orders.drop_duplicates().reset_index(drop= True)

# %%
# Vuelve a verificar si hay filas duplicadas
df_instacart_orders.duplicated().sum()

# %%
# Vuelve a verificar únicamente si hay IDs duplicados de pedidos
# Se emplea el parámetro subset= del método duplicated() para buscar duplicados en las columnas de interés
df_instacart_orders.duplicated(subset=['order_id', 'user_id']).sum()

# %% [markdown]
# Describe brevemente tus hallazgos y lo que hiciste con ellos  
# <span style="color:darkgreen">
# Se encontraron duplicados, por lo que se eliminaron con el método ``drop_duplicates()``   
# Problamente los duplicados se debieron a un error de captura.  
# No se hizo cambio de tip de dato en ninguna columna, las columnas de ID su tipo de dato es entero.
# </span>.  

# %% [markdown]
# ### `products` data frame

# %%
# Verifica si hay filas totalmente duplicadas
df_products.duplicated().sum()

# %%
# Verifica únicamente si hay IDs duplicadas de productos
df_products['product_id'].duplicated().sum()

# %%
# Revisa únicamente si hay nombres duplicados de productos (convierte los nombres a letras mayúsculas para compararlos mejor)
df_products['product_name'] = df_products['product_name'].str.upper() # str.upper() para convertir los nombres a mayúsculas
df_products['product_name'].duplicated().sum()

# %%
# Se filtra el DataFrame con los duplicados de la columna product_name
df_products[df_products['product_name'].duplicated()]

# %%
# Revisa si hay nombres duplicados de productos no faltantes
# se emplea ~ para invertir el resultado del filtro
# Al DataFrame resultante después del filtro se revisa si hay valores duplicados
df_products[~df_products['product_name'].isna()]['product_name'].duplicated().sum()

# %%
df_products_no_null = df_products[~df_products['product_name'].isna()]

# %% [markdown]
# .
# <span style="color:darkgreen">
# Después de revisar los duplicados en la columna ``product_name`` sin valores faltantes se encontró que hay sólo 104 nombres de productos duplicados. Lo cual indica que en el primer resultado de 1361 duplicados se estaban considerando los valores ausentes
# </span>. 

# %% [markdown]
# .
# <span style="color:darkgreen">
# Ahora para ver algunos de estos valores duplicados al DataFrame **df_products_no_null** en dónde no hay valores ausentes en la columna ``product_name`` se aplica un filtro, donde se usa el método ``duplicated(keep=False)``, el parámetro ``keep=`` se incluye para que el resultado incluya todos los valores duplicados.  
# Después se ordena el DataFrame por la columna ``product_name`` con ``sort_values``. Y se muestran las primeras 50 filas con ``head()``
# </span>. 

# %%
df_products_no_null[df_products_no_null['product_name'].duplicated(keep=False)].sort_values(by= ['product_name']).head(50)

# %% [markdown]
# Describe brevemente tus hallazgos y lo que hiciste con ellos.  
# <span style="color:darkgreen">
# -> Primero se encontró que habian 1361 duplicados en la columna ``product_name``, después se aplicó un filtro al DataFrame para mostrar unicamente los datos en donde estaban los duplicados. En el DataFrame resultante se observó que habian valores ausentes en la columna.  
# -> Luego, al  revisar si habian nombres duplicados de los productos en la columna ``product_name`` sin considerar los valores ausentes el resultado fue 104.  
# -> Luego los datos se filtraron del DataFrame sin los valores ausentes en la columna ``product_name``, donde se mostraban todos los productos duplicados ordenados en orden alfabético, en algunos productos el valor para ``aisle_id`` y ``department_id`` son iguales, pero en otros no, además de que el ``product_id`` si es diferente para cada producto. Por lo tanto, se decidió dejar estos valores y no eliminarlos.
# </span>. 

# %% [markdown]
# ### `departments` data frame

# %%
# Revisa si hay filas totalmente duplicadas
df_departments.duplicated().sum()

# %%
# Revisa únicamente si hay IDs duplicadas de productos
df_departments['department_id'].duplicated().sum()

# %% [markdown]
# Describe brevemente tus hallazgos y lo que hiciste con ellos.  
# <span style="color:darkgreen">
# Para este DataFrame no se tienen filas duplicadas ni tampoco IDs duplicados, entonces no hay necesidad de procesar los datos respecto a los duplicados.
# </span>. 

# %% [markdown]
# ### `aisles` data frame

# %%
# Revisa si hay filas totalmente duplicadas
df_aisles.duplicated().sum()

# %%
# Revisa únicamente si hay IDs duplicadas de productos
df_aisles['aisle_id'].duplicated().sum()

# %% [markdown]
# Describe brevemente tus hallazgos y lo que hiciste con ellos.  
# <span style="color:darkgreen">
# Este DataFrame no se tienen filas duplicadas ni tampoco IDs duplicados, entonces no hay necesidad de procesar los datos respecto a los duplicados
# </span>. 

# %% [markdown]
# ### `order_products` data frame

# %%
# Revisa si hay filas totalmente duplicadas
df_order_products.duplicated().sum()

# %%
df_order_products.info(show_counts=True)

# %%
# Vuelve a verificar si hay cualquier otro duplicado engañoso
# Se revisa si hay duplicados de IDs en la columna order_id
df_order_products['order_id'].duplicated().sum()

# %%
# Se revisa si hay duplicados de IDs en la columna product_id
df_order_products['product_id'].duplicated().sum()

# %% [markdown]
# Describe brevemente tus hallazgos y lo que hiciste con ellos.  
# <span style="color:darkgreen">
# Para este DataFrame no se encontraron filas duplicadas.  
# En cuanto al resto de las columnas al revisar si hay duplicados en ``order_id`` y ``product_id``, de acuerdo al resultado si hay valores duplicados, sin embargo, no se eliminan estos valores debido a que cada ID de una orden hace referencia a un producto diferente y visceversa, cada ID de un producto pertenece a una orden diferente
# </span>. 

# %% [markdown]
# ## Encuentra y elimina los valores ausentes
# 
# Al trabajar con valores duplicados, pudimos observar que también nos falta investigar valores ausentes:
# 
# * La columna `'product_name'` de la tabla products.
# * La columna `'days_since_prior_order'` de la tabla orders.
# * La columna `'add_to_cart_order'` de la tabla order_productos.

# %% [markdown]
# ### `products` data frame

# %%
# Encuentra los valores ausentes en la columna 'product_name'
df_products['product_name'].isna().sum()

# %% [markdown]
# Describe brevemente cuáles son tus hallazgos.  
# <span style="color:darkgreen">
# Hay un total de 1258 valores ausentes en la columna ``product_name``
# </span>. 

# %%
#  ¿Todos los nombres de productos ausentes están relacionados con el pasillo con ID 100?
# Se filtra el DataFrame df_products en donde la columna product_name tenga valores ausentes
df_products[df_products['product_name'].isna()]

# %% [markdown]
# Describe brevemente cuáles son tus hallazgos.  
# <span style="color:darkgreen">
# Los valores ausentes para columna product_name si están relacionados con el pasillo con ID 100
# </span>.

# %%
# ¿Todos los nombres de productos ausentes están relacionados con el departamento con ID 21?
df_products[df_products['department_id'] == 21]

# %% [markdown]
# Describe brevemente cuáles son tus hallazgos.  
# <span style="color:darkgreen">
# Los valores ausentes para columna product_name si están relacionados con el departamento con ID 21
# </span>.

# %%
# Usa las tablas department y aisle para revisar los datos del pasillo con ID 100 y el departamento con ID 21.
# Se aplica un filtro para el DataFrame df_departments en donde el ID del departamento sea 21
df_departments[df_departments['department_id'] == 21]

# %%
# Se aplica un filtro para el DataFrame df_aisles en donde el ID del pasillo sea 100
df_aisles[df_aisles['aisle_id'] == 100]

# %% [markdown]
# Describe brevemente cuáles son tus hallazgos.  
# <span style="color:darkgreen">
# E ambos casos los valores para el ID del departemento 21 y el ID de pasillo 100 el valor es ausente
# </span>.

# %%
# Completa los nombres de productos ausentes con 'Unknown'
df_products['product_name'].fillna('Unknown', inplace= True)

# %% [markdown]
# Describe brevemente tus hallazgos y lo que hiciste con ellos.  
# <span style="color:darkgreen">
# Para los valores ausentes de la columna ``product_name`` estan relacionados con el departamento con ID 21 y con el pasillo con ID 100. Al revisar los DataFrames de departments y aisles se encontró que dichos IDs están indicados como ausentes para el departamente y pasillo
# </span>.

# %% [markdown]
# ### `orders` data frame

# %%
# Encuentra los valores ausentes
df_instacart_orders.isna().sum()

# %%
# ¿Hay algún valor ausente que no sea el primer pedido del cliente?
df_instacart_orders[df_instacart_orders['order_number'] != 1].isna().sum()

# %% [markdown]
# Describe brevemente tus hallazgos y lo que hiciste con ellos.  
# <span style="color:darkgreen">
# Los valores ausentes en la columna ``days_since_prior_order`` están cuando son el primer pedido del cliente. Por lo tanto no se eliminarán o reemplazarán con cero, se decidió dejar esos valores ausentes así y no midificarlos
# </span>.

# %% [markdown]
# ### `order_products` data frame

# %%
df_order_products.info()

# %%
# Encuentra los valores ausentes
df_order_products.isna().sum()

# %%
# ¿Cuáles son los valores mínimos y máximos en esta columna?
print(f"El valor mínimo es: {df_order_products['add_to_cart_order'].min()}")
print(f"El valor máximo es: {df_order_products['add_to_cart_order'].max()}")

# %% [markdown]
# Describe brevemente cuáles son tus hallazgos.  
# <span style="color:darkgreen">
# La columna ``add_to_cart_order`` es la única con valores ausentes, el valor mínimo y máximo de esa columna son 1 y 64, respectivamente
# </span>.

# %%
# Guarda todas las IDs de pedidos que tengan un valor ausente en 'add_to_cart_order'
df_order_products_null = df_order_products[df_order_products['add_to_cart_order'].isna()]
df_order_products_null.head()

# %%
# ¿Todos los pedidos con valores ausentes tienen más de 64 productos?
# Agrupa todos los pedidos con datos ausentes por su ID de pedido.
# Cuenta el número de 'product_id' en cada pedido y revisa el valor mínimo del conteo.
# Los datos se dividen con el método groupby(), con la función count() se cuentan el número de productos en la columna 'product_id'
# Los valores se ordenan de menor a mayor con el método sort_values()
df_order_products_null.groupby('order_id')['product_id'].count().sort_values()

# %% [markdown]
# Describe brevemente cuáles son tus hallazgos.  
# <span style="color:darkgreen">
# El valor mínimo del conteo de productos por pedido es 1. Mientras que, los pedidos con valores ausentes no tienen más de 64 productos
# </span>.

# %%
# Remplaza los valores ausentes en la columna 'add_to_cart? con 999 y convierte la columna al tipo entero.
# con fillna() se reemplazan los valores ausentes con 999
df_order_products['add_to_cart_order'].fillna(999, inplace= True)

# %%
# se comprueba si es seguro convertir la columna 'add_to_cart_order' a entero con la función array_equal() 
np.array_equal(df_order_products['add_to_cart_order'], df_order_products['add_to_cart_order'].astype('int'))

# %% [markdown]
# .  
# <span style="color:darkgreen">
# El resultado es ``True`` por lo que no hay problema para cambiar el tipo de dato de la columna
# </span>.

# %%
df_order_products['add_to_cart_order'] = df_order_products['add_to_cart_order'].astype('int')

# %% [markdown]
# Describe brevemente tus hallazgos y lo que hiciste con ellos.  
# <span style="color:darkgreen">
# Los datos ausentes sólo estaban en la columna ``add_to_cart_order``, los cuáles se reemplazaron con el valor de 999
# </span>.

# %% [markdown]
# ## Conclusiones  
# <span style="color:darkgreen">
#     
# El tipo de dato en las columanas de IDs son del tipo entero.  
# Algunas columnas de los DataFrames tenian valores duplicados, en algunos casos se eliminaron y en otros no.
# En el DataFrame de productos ``df_products`` los valores ausentes se estaban considerando como duplicados, para ello se aplicó un filtro para no tomarlos como duplicados.  
# Se encontraron valores ausentes en algunas columnas, los cuales se reemplazaron con sus valores correspodientes de acuerdo a la información de cada DataFrame, sólo en la columna ``days_since_prior_order`` del DataFrame de las ordenes ``df_orders`` no se reemplazaron los valores ausentes, se decidió dejarlos así como ausentes
# </span>.

# %% [markdown]
# # Paso 3. Análisis de los datos
# 
# Una vez los datos estén procesados y listos, haz el siguiente análisis:

# %% [markdown]
# # [A] Fácil (deben completarse todos para aprobar)
# 
# 1. Verifica que los valores en las columnas `'order_hour_of_day'` y `'order_dow'` de la tabla `orders` sean sensibles (es decir, `'order_hour_of_day'` va de 0 a 23 y `'order_dow'` va de 0 a 6).
# 2. Crea un gráfico que muestre el número de personas que hacen pedidos dependiendo de la hora del día.
# 3. Crea un gráfico que muestre qué día de la semana la gente hace sus compras.
# 4. Crea un gráfico que muestre el tiempo que la gente espera hasta hacer su siguiente pedido, y comenta sobre los valores mínimos y máximos.

# %% [markdown]
# ### [A1] Verifica que los valores sean sensibles

# %%
# Se contabilizan los valores únicos de la columna 'order_hour_of_day' con el método value_counts() y se ordenan de acuerdo a la hora, de menor a mayor (0 a 23)
df_instacart_orders['order_hour_of_day'].value_counts().sort_index()

# %%
# Se contabilizan los valores únicos de la columna 'order_dow' con el método value_counts() y se ordenan de acuerdo a la hora, de menor a mayor (0 a 23)
df_instacart_orders['order_dow'].value_counts().sort_index()

# %%
# Las horas del día se agrupan y se contabilizan el número de usuarios que hicieron un pedido en cada del día
# El resultado se asigna a hour_of_day_orders
hour_of_day_orders = df_instacart_orders.groupby('order_hour_of_day')['user_id'].count()
hour_of_day_orders

# %%
# Los días de la semana se agrupan y se contabilizan el número de usuarios que hicieron un pedido en cada día de la semana
# El resultado se asigna week_day_orders
week_day_orders = df_instacart_orders.groupby('order_dow')['user_id'].count()
week_day_orders

# %% [markdown]
# Escribe aquí tus conclusiones  
# <span style="color:darkgreen">
# Los valores de las columnas ``order_hour_of_day`` y ``order_dow`` se contaron sus valores únicos y se ordenaron de menor a mayor de acuerdo a la hora o al día, se observa que que tanto la hora como los días los valores están dentro de los rangos apropiados, los datos o valores son lógicos y adecuados para sus respectivas columnas.
# </span>

# %% [markdown]
# ### [A2] Para cada hora del día, ¿cuántas personas hacen órdenes?

# %%
# Ahora se grafican el número de personas que hicieron pedidos para cada hora del día
# Para esto se usa el método plot() de Pandas y pyplot de matplotlib (plt) para mostrar el gráfico
hour_of_day_orders.plot(x='order_hour_of_day', 
                       title= 'Número de personas que hacen pedidos por hora del día',
                       xlabel= 'Hora del día',
                       ylabel='Cantidad de personas',
                       style=',-',
                       xticks= range(0,24,2)
                       )
plt.show()

# %% [markdown]
# Escribe aquí tus conclusiones  
# <span style="color:darkgreen">
# La hora en la que las personas hacen un mayor número de pedidos es a las 9, asimismo en el intervalo entre las 9 y las 16 hay un mayor número de personas que hicieron pedidos respecto a las otras horas
# </span>.

# %% [markdown]
# ### [A3] ¿Qué día de la semana compran víveres las personas?

# %%
# Ahora se grafican el número de personas que hicieron pedidos para cada día de la semana
# Para esto se usa el método plot() de Pandas y pyplot de matplotlib (plt) para mostrar el gráfico
day = [0,1,2,3,4,5,6]
# Lista con el nombre de los días de la semana, cada nombre de la semana corresponde a un elemento de la lista day, en elorden que aparecen
week_day = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
week_day_orders.plot(x= 'order_dow',
                     kind= 'bar',
                     title= 'Número de personas que hacen pedidos por día de la semana',
                     xlabel= 'Día de la Semana',
                     ylabel='Cantidad de personas',
                     rot= 45
                       )

plt.xticks(day, week_day)
plt.show()

# %% [markdown]
# Escribe aquí tus conclusiones  
# <span style="color:darkgreen">
# Los días Domingo y Lunes, que es el inicio de semana, hay un mayor número de personas que hicieron pedidos.
# </span>.

# %% [markdown]
# <div class="alert alert-block alert-success">
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
#     
# Perfecto.
# </div>

# %% [markdown]
# ### [A4] ¿Cuánto tiempo esperan las personas hasta hacer otro pedido? Comenta sobre los valores mínimos y máximos.

# %%
df_instacart_orders['days_since_prior_order'].max()

# %%
df_instacart_orders['days_since_prior_order'].describe()

# %%
df_instacart_orders['days_since_prior_order'].plot(kind= 'hist', 
                                                   bins=30,
                                                  title= 'Tiempo que la gente espera hasta hacer su siguiente pedido',
                                                  edgecolor ='white',
                                                  figsize= [8,6])

plt.ylabel('Frecuencia')
plt.xlabel('Número de días trancurridos')
plt.show()

# %% [markdown]
# Escribe aquí tus conclusiones  
# <span style="color:darkgreen">
# Hay un pico que es para 30 días transcurridos desde que el cliente hizo su último pedido, el cual es el valor de días máximo que transcurren,. Mientras que el valor mínimo de los días transcurridos es 0, el cual no tiene muchos valores.
# </span>.

# %% [markdown]
# # [B] Intermedio (deben completarse todos para aprobar)
# 
# 1. ¿Existe alguna diferencia entre las distribuciones `'order_hour_of_day'` de los miércoles y los sábados? Traza gráficos de barra de `'order_hour_of_day'` para ambos días en la misma figura y describe las diferencias que observes.
# 2. Grafica la distribución para el número de órdenes que hacen los clientes (es decir, cuántos clientes hicieron solo 1 pedido, cuántos hicieron 2, cuántos 3, y así sucesivamente...).
# 3. ¿Cuáles son los 20 principales productos que se piden con más frecuencia (muestra su identificación y nombre)?

# %% [markdown]
# ### [B1] Diferencia entre miércoles y sábados para  `'order_hour_of_day'`. Traza gráficos de barra para los dos días y describe las diferencias que veas.

# %%
# Se crean dos DataFrames uno en donde se tengan los valores sólo para el día miércoles y otro para el día sábado
df_wed_orders = df_instacart_orders[(df_instacart_orders['order_dow'] == 3)]
df_sat_orders = df_instacart_orders[(df_instacart_orders['order_dow'] == 6)]

# %%
# A partir de los DataFrames df_wed_orders y df_sat_orders se crea sus respectivos histogramas en el mismo gráfico
df_wed_orders['order_hour_of_day'].plot(kind='hist',
                                        bins= 30, 
                                        alpha= 0.8,
                                        figsize= [8,6],
                                        xticks= range(0,24,2)
                                       )
df_sat_orders['order_hour_of_day'].plot(kind='hist', 
                                        bins= 30, 
                                        alpha= 0.6,
                                        figsize= [8,6],
                                        xticks= range(0,24,2)
                                       )
plt.title('Hora del día en que se hizo el pedido') # para colocar un título
plt.ylabel('Frecuencia') # Para nombrar el eje y
plt.legend(['Miércoles', 'Sábado']) # para colocar las leyendas del gráfico
plt.show()

# %% [markdown]
# Escribe aquí tus conclusiones  
# <span style="color:darkgreen">
# Las distribuciones de los datos para el día miércoles y sábado son muy similares, el intervalo de las horas en las que se hicieron más pedidos fueron entre las 10 y 16. Al parecer en estos días se realizan aproximadamente el mismo número de pedidos en las mismas horas
# </span>.

# %% [markdown]
# ### [B2] ¿Cuál es la distribución para el número de pedidos por cliente?

# %%
# se crea un DataFrame que sólo tenga las columnas 'order_number' y 'user_id'
df_ordernum_user = df_instacart_orders[['order_number','user_id']]
df_ordernum_user.head() # se muestran las primeras 5 filas

# %%
# se crea un histograma para observar la distribución para el número de pedidos por cliente
df_ordernum_user['order_number'].plot(kind='hist', 
                       bins= 30,
                       figsize= [12,6],
                       edgecolor ='white',
                       xticks= range(0,105,5)
                      )
plt.title('Número de pedidos')
plt.ylabel('Frecuencia')
plt.show()

# %% [markdown]
# Escribe aquí tus conclusiones  
# <span style="color:darkgreen">
# La cantidad de pedidos que hacen la mayoria de los clientes son menos de 5.  
# Hay menos clientes que hacen más de 5 pedidos
# </span>.

# %% [markdown]
# ### [B3] ¿Cuáles son los 20 productos más populares (muestra su ID y nombre)?

# %% [markdown]
# <span style="color:darkgreen">Primero se mostrarán con el método ``head()`` las primeras 5 filas de los DataFrames ``df_products`` y ``df_order_products`` para identificar cuáles columnas tienen en común y posteriormente hacer un merge de estos Datasets.
# </span>

# %%
df_products.head()

# %%
df_order_products.head()

# %%
# Se hace el primer merge con las DataFrames df_products y df_order_products, la columna en común es el 'product_id'
products_and_orders = df_products.merge(df_order_products, on= 'product_id')
products_and_orders

# %%
# Se agrupan las columas de product_id y el nombre del producto ('product_name') y se contabilizan el las ordenes para cada producto
products_and_orders.groupby(['product_id', 'product_name'])['order_id'].count().sort_values(ascending= False).head(20)

# %% [markdown]
# Escribe aquí tus conclusiones  
# <span style="color:darkgreen">  
# Los 20 productos más populares entre los clientes son frutas y verduras, a excepción de la leche, lo cuál podría indicar que son parte fundamental de su canasta básica para su alimentación
# </span>.

# %% [markdown]
# # [C] Difícil (deben completarse todos para aprobar)
# 
# 1. ¿Cuántos artículos suelen comprar las personas en un pedido? ¿Cómo es la distribución?
# 2. ¿Cuáles son los 20 principales artículos que vuelven a pedirse con mayor frecuencia (muestra sus nombres e IDs de los productos)?
# 3. Para cada producto, ¿cuál es la tasa de repetición del pedido (número de repeticiones de pedido/total de pedidos?
# 4. Para cada cliente, ¿qué proporción de los productos que pidió ya los había pedido? Calcula la tasa de repetición de pedido para cada usuario en lugar de para cada producto.
# 5. ¿Cuáles son los 20 principales artículos que la gente pone primero en sus carritos (muestra las IDs de los productos, sus nombres, y el número de veces en que fueron el primer artículo en añadirse al carrito)?

# %% [markdown]
# ### [C1] ¿Cuántos artículos compran normalmente las personas en un pedido? ¿Cómo es la distribución?

# %% [markdown]
# <span style="color: darkgreen">Primero se muestran con el método ``head()`` los DataFrame de ``df_instacart_orders`` y ``df_order_products``, los cuales son de utilidad para conocer la cantidad de artículos por pedido, la columna que tienen en común es ``order_id``, la cual se usará más adelante para hacer un merge de ambos Dataset.
# </span>

# %%
# 
df_instacart_orders.head()

# %%
df_order_products.head()

# %%
# Se hace el merge de los DataFrames
merged_orders_products = df_instacart_orders.merge(df_order_products, on= 'order_id')
merged_orders_products.head(10)

# %%
# Se agrupan los pedidos y se contabilizan el número de de productos para cada pedido
products_by_order = merged_orders_products.groupby('order_id')['product_id'].count()
products_by_order.sort_values()

# %%
# Ahora se grafica un histograma para observar la distribución de la cantidad de artículos por cada orden
products_by_order.plot(kind= 'hist',
                       bins= 130,
                       figsize= [18,8],
                       xticks= range(0,130,5),
                       edgecolor ='white',
                       fontsize= 12
                      )
plt.title('Número de artículos', fontsize=15)
plt.ylabel('Frecuencia', fontsize=15)
plt.show()

# %% [markdown]
# Escribe aquí tus conclusiones  
# <span style="color: darkgreen">De acuerdo con el histograma la cantidad de artículos que compran o que se realiza por pedidos son entre 5 y 6, ya que tienen los picos más grandes.</span>

# %% [markdown]
# ### [C2] ¿Cuáles son los 20 principales artículos que vuelven a pedirse con mayor frecuencia (muestra sus nombres e IDs de los productos)?

# %% [markdown]
# <span style="color: darkgreen">Los DataFrame de ``df_products`` y ``df_order_products`` tienen la información para conocer los 20 artículos que más se vuelven a pedir, la columna que tienen en común es ``product_id``.  
# Es importante mencionar que en la sección **7.7 [B3]** ya se hizo un merge de estos DataFrames, el cual es ``products_and_orders``.
# </span>

# %%
# DataFrame resultante de la unión de los DataFrame de df_products y df_order_products
products_and_orders.head()

# %% [markdown]
# <span style="color: darkgreen">Recordatorio: en la columna ``reordered`` si es **0**  el cliente nunca ha pedido este producto antes, **1** si lo ha pedido.
# </span>

# %%
# Se emplea el método query() para hacer un filtrado del DataFrame products_and_orders, en dónde la columna 'reordered' sea 1
# Y únicamente se incluyen en DatFrame resultante las columnas de 'product_id','product_name' y'reordered'
df_reordered = products_and_orders.query('reordered == 1')[['product_id','product_name','reordered']]
df_reordered.sample(5)

# %%
# Ahora se agrupan el ID de los productos y el nombre del producto, y se contabilizan las veces que se ha pedido cada producto
# Los valores se ordenan con sort_values() de mayor a menor y se muestran con head() los 20 artículos que más se vuelven a ordenar 
top_20_reordered_products = df_reordered.groupby(['product_id','product_name'])['reordered'].count().sort_values(ascending=False).head(20)
top_20_reordered_products

# %% [markdown]
# Escribe aquí tus conclusiones  
# <span style="color: darkgreen">Los 20 artículos que más vuelven a pedir los usuarios o usuarias principalmente son los productos frescos, a excepción de la leche (ORGANIC WHOLE MILK) y la media crema (ORGANIC HALF & HALF), también varios de los productos frescos son orgánicos.
# </span>

# %% [markdown]
# ### [C3] Para cada producto, ¿cuál es la proporción de las veces que se pide y que se vuelve a pedir?

# %% [markdown]
# <span style="color: darkgreen">Nuevamente se empleará el DataFrame ``products_and_orders`` que se creó con un merge en la sección **7.7 [B3]**, que tiene la información de los productos y de los artículos pedidos en un pedido.
# </span>

# %%
# Ahora se agrupan los productos por su nombre y se contabilizan todos sus valores de las columnas, hayan sido pedidos nuevamente o no
# El Series resultante se asigna a total_ordered_products
total_ordered_products = products_and_orders.groupby(['product_id','product_name'])['reordered'].count()
total_ordered_products.head()

# %%
# Se emplea el DataFrame df_reordered que tiene solo los artículos que se volvieron a pedir
# Ahora se agrupan los productos por su nombre y se contabilizan todas los valores de la columna 'reordered'
# El Series resultante se asigna a ordered_again_product
ordered_again_product = df_reordered.groupby(['product_id', 'product_name'])['reordered'].count()
ordered_again_product.head()

# %%
# Ahora los Series total_ordered_products y ordered_again_product se concatenan con concat, con axis= 'columns' para asegurarnos de que se combinaran como columnas
reordered_by_products = pd.concat([total_ordered_products, ordered_again_product], axis='columns')
# Se renombran las columnas
reordered_by_products.columns = ['total_ordered', 'reps_orders']
# con reset_index() se reinicia el índice del DataFrame reordered_by_products
reordered_by_products.reset_index(inplace= True)

# %%
reordered_by_products.head()

# %% [markdown]
# <span style="color: darkgreen">El DataFrame ``reordered_by_products`` tiene dos columnas, ``total_ordered`` que es el total de pedidos y ``reps_orders`` que es el número de veces que se vuelve a pedir. Ahora se crea una nueva columna para calcular la tasa de repetición para cada producto. Además, en la columna ``reps_orders`` los valores ausente significa que no se volvieron a ordenar por lo que estos valores se llenan con 0.
# </span>

# %%
# Se llenan los vlores ausente de la columna 'reps_orders' con 0
reordered_by_products['reps_orders'].fillna(0, inplace= True)

# %%
# Ahora se crea una nueva columna para calcular la tasa de repetición, dividiento número de repeticiones de pedido entre el total de pedidos
reordered_by_products['rep_ratio'] = reordered_by_products['reps_orders'] / reordered_by_products['total_ordered']
reordered_by_products

# %%
# se ordenan de mayor a menor con base a la columna rep_ratio y se muestran 20 filas con head()
reordered_by_products.sort_values(by= ['rep_ratio'], ascending= False).head(20)

# %% [markdown]
# <span style="color: darkgreen">Para mostrar la distribución de la tasa de repetición para los productos se grafica un histograma. 
# </span>

# %%
reordered_by_products['rep_ratio'].plot(kind= 'hist',
                       bins= 30,
                       figsize= [12,8],
                       edgecolor ='white',
                       fontsize= 12
                      )

plt.title('Tasa de repetición para productos', fontsize=15)
plt.ylabel('Frecuencia', fontsize=15)
plt.show()

# %% [markdown]
# Escribe aquí tus conclusiones  
# <span style="color: darkgreen">La tasa de repetición para los primeros 20 artículos es de 1, lo que significa que de todas veces que se pidió, el 100% se volvió a pedir. Además, estos 20 artículos son muy variados, no sólo son alimentos. 
# De acuerdo al histograma el pico mayor esta en 0, lo significa que el artículo no vuelve a ser pedido, el segundo pico de mayor altura esta alrdedor de 0.5, lo que quiere decir que el 50 % de los productos se vuelve a pedir.
# </span>

# %% [markdown]
# ### [C4] Para cada cliente, ¿qué proporción de sus productos ya los había pedido?

# %% [markdown]
# <span style="color: darkgreen">El DataFrame ``products_and_orders`` tiene información del producto y la información del artículo pedido en un pedido. Ahora se hace un merge con el DataFrame ``instacart_orders`` que tiene información sobre los usurios.
# </span>

# %%
# Se hace un merge para unir los DataFrames, la columna en común con los IDs es 'order_id'
products_orders_users = products_and_orders.merge(df_instacart_orders, on= 'order_id')
products_orders_users.head()

# %%
orders_count_user = products_orders_users.groupby('user_id')['reordered'].count().sort_values(ascending= False)
orders_count_user

# %%
reordered_count_user = products_orders_users.query('reordered == 1').groupby('user_id')['reordered'].count().sort_values(ascending= False)
reordered_count_user

# %%
# Ahora los Series orders_count_user y reordered_count_user se concatenan con concat, con axis= 'columns' para asegurarnos de que se combinaran como columnas
reordered_by_user = pd.concat([orders_count_user, reordered_count_user], axis='columns')
# Se renombran las columnas
reordered_by_user.columns = ['total_ordered', 'reps_orders']
# # con reset_index() se reinicia el índice del DataFrame reordered_by_user
reordered_by_user.reset_index(inplace= True)

# %%
reordered_by_user.head()

# %% [markdown]
# <span style="color: darkgreen"> En la columna ``reps_orders`` los valores ausente significa que no se volvieron a ordenar por lo que estos valores se llenan con 0.
# </span>

# %%
# Se llenan los vlores ausente de la columna 'reps_orders' con 0
reordered_by_user['reps_orders'].fillna(0, inplace= True)

# %%
# Ahora se crea una nueva columna para calcular la tasa de repetición por usuario, dividiento número de repeticiones de pedido entre el total de pedidos
reordered_by_user['rep_ratio'] = reordered_by_user['reps_orders'] / reordered_by_user['total_ordered']
reordered_by_user.head(10)

# %% [markdown]
# <span style="color: darkgreen">Para mostrar la distribución de la proporción de los productos que los usuarios o usuarias ya los habían pedido se grafica un histograma. 
# </span>

# %%
reordered_by_user['rep_ratio'].plot(kind= 'hist',
                       bins= 30,
                       figsize= [12,8],
                       edgecolor ='white',
                       fontsize= 12
                      )

plt.title('Tasa de repetición para usuarios', fontsize=15)
plt.ylabel('Frecuencia', fontsize=15)
plt.show()

# %% [markdown]
# Escribe aquí tus conclusiones  
# <span style="color: darkgreen"> 
# De acuerdo con el histograma el pico mayor esta en 0, lo significa que el artículo no vuelve a ser pedido por los usuarios o usuarias, el segundo pico de mayor altura esta alrdedor de 0.5, lo que quiere decir que el 50 % de los productos se volvieron a pedir por los usuarios.
# </span>

# %% [markdown]
# ### [C5] ¿Cuáles son los 20 principales artículos que las personas ponen primero en sus carritos?

# %% [markdown]
# <span style="color: darkgreen">Nuevamente se emplea el DataFrame ``products_and_orders`` que se creó con un merge en la sección **7.7 [B3]**, que tiene la información de los productos y de los artículos pedidos en un pedido.
# </span>

# %%
# Priemras filas del Dataframe products_and_orders
products_and_orders.head()

# %%
# Se aplica un filtro con el método query() sobre la columna 'add_to_cart_order' en donde sólo devuelva los valores igual a 1
# Al resultado de este filtro se agrupa por el ID del producto y el nombre del producto y se cuentan los valores de la 
# columna 'add_to_cart_order' con count()
# Al resultado del conteo se aplica el método sort_values() para que ordene los valores de mayor a menor y se muestran los 20 primeros productos
products_and_orders.query('add_to_cart_order == 1').groupby(['product_id','product_name'])['add_to_cart_order'].count().sort_values(ascending= False).head(20)

# %% [markdown]
# Escribe aquí tus conclusiones  
# <span style="color: darkgreen">Los artículos que los usuarios o usuarias ponen primero en sus carritos principalmente son frutas y verduras, hay otros artículos como refresco, agua y leche. Todos los artículos son alimentos, no hay otro artículo que no sea un alimento y/o bebida.
# </span>

# %% [markdown]
# <div class="alert alert-block alert-info">
# <b>Resumen general de los pasos realizados:</b> <a class="tocSkip"></a>
#  
# Para trabajar con todo el conjunto de datos se importaron las librerías necesarias y se importaron los Datasets. Después se hizo un exploración de cada DatFrame con ``info()`` para detectar de manera general la cantidad de datos, columnas y valores ausentes. Posteriormente, los datos se procesaron para cada DataFrame encontrando y eliminando los valores duplicados y ausentes, así como detectar el tipo de dato de las columnas.  
#     
# En algunos casos fue necesario aplicar algunos filtros, usando máscaras booleanas o el método ``query()``. También se crearon varios gráficos con la ayuda del método ``plot()`` de Pandas y para visualizarlos se empleó Pyplot de la librería Matplotlib, algunos de los gráficos que se crearon fueron histogramas, gráficos de barras y de líneas.  
#     
# También se tuvieron que realizar algunos ``merge()`` para unir diferentes DataFrames, ya que la información para hacer los análisis está en varios conjunto de datos. De igual forma se utilizó ``concat()`` para unir algunos Series, porque estos se complementaban para completar la información y a partir del DataFrame resultante crear otra columna.  
#     
# 
# <b>Conclusiones:</b> <a class="tocSkip"></a>
#     
# Al importar los Dataset se encontró que el archivo csv tenía como separador un ';', entonces se indicó al importarlos el tipo de separador.  Algunos DataFrame tenían valores duplicados y se eliminaron, no obstante, en otros casos se decidió no hacerlo. También se encontraron valores ausentes, los cuales se llenaron con información que se consideró adecuada para hacerla, ya que si se eliminaban se perdería mucha información. En otros casos, se optó por no eliminar los datos ausentes y dejarlos así.  
#     
# De acuerdo al análisis, los usuarios y usuarias realizan más pedidos entre las 9:00 y 16:00 horas, asimismo los días con mayor cantidad de compras son los domingos y lunes. Por otra parte, los días miércoles y sábados los pedidos son muy similares en los mismos horarios.  
#     
# Aproximadamente el mayor número de días transcurridos que esperan los usuarios y usuarias para hacer el siguiente pedido es 30, sin embargo, hay otro grupo en el cual transcurren alrededor de 8 días para que hagan el siguiente pedido.  
#     
# La mayoría de clientes y clientas hacen menos de 5 pedidos.  
#     
# Los 20 productos más populares entre los usuarios y usuarias son los productos frescos, varios de estos son orgánicos.  
#     
# En cada pedido la cantidad de artículos que se compran son entre 5 y 6, de acuerdo con los resultados al menos uno de estos artículos podría ser un producto fresco, agua, soda o leche, ya que son los productos que ponen primero en sus carritos.  
#     
# Los 20 productos que vuelven a pedirse con más frecuencia son de la sección o departamento de frutas y verduras.  
#     
# Del total de las veces que los productos se vuelven a pedir, el 50% de estos se vuelve a ordenar. Por su parte, en su mayoría el 0 % de las veces los usuarios y usuarias vuelven a pedir el artículo, sin embargo, hay otros clientes que el 50 % vuelve a pedir el producto.  
# </div>


