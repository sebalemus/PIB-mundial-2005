# -*- coding: utf-8 -*-
"""analisis_naciones_gdp.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/gist/sebalemus/920525a7d2b73490a63fb45aa2dd50c2/analisis_naciones_gdp.ipynb

# En este notebook analizaremos las distintas variables de desarrollo humano en los distintos paises de todos los continentes segun su PIB del año 2005
"""

#Importemos las librerías con las que trabajaremos
import pandas as pd                             #manipulación y análisis de datos
import numpy as np                              #funciones matematicas, algebralineal
import seaborn as sns                           #creación de graficos
import matplotlib.pyplot as plt                 #importamos librería matplot
import statsmodels.formula.api as smf           #Statsmodels es la biblioteca para realizar modelos

"""El dataset 'nations', contiene información sobre diferentes atributos de desarrollo humano en 194 países, recolectados por las Naciones Unidas en el año 2005.

* Contiene información a nivel mundial sobre demografía:
    * `country`: País.
    * `region`: Continente del país.
    * `gdp`: Producto Interno Bruto per cápita, precios 2005.
    * `school`: Promedio años de escolaridad.
    * `adfert`: Fertilidad adolescente (Nacimientos 1:1000 en mujeres entre 15 y 19).
    * `chldmort`: Probabilidad de muerte antes de los 5 años por cada 1000.
    * `life`: Esperanza de vida al nacer.
    * `pop`: Población total.
    * `urban`: Porcentaje de población urbana.
    * `femlab`: Tasa entre hombres y mujeres en el mercado laboral.
    * `literacy`: Tasa de alfabetismo.
    * `co2`: Toneladas de Co2 emitidas per cápita.
    * `gini`: Coeficiente de desigualdad del ingreso.


"""

#cargamos el dataset y lo guardamos en "naciones"
naciones = pd.read_csv("https://raw.githubusercontent.com/DireccionAcademicaADL/Nations-DB/main/nations.csv", encoding="ISO-8859-1")

naciones

"""Se puede apreciar que la columna "Unnamed:  0" parece no tener información relevante, por lo que la eliminaremos."""

naciones.drop(columns=["Unnamed: 0"], inplace = True)     #inplace=true-->elimina sobre el mismo DF en vez de copiar o hacer uno nuevo

naciones.head(3)

"""La columna "gdp" se mide en dólares corrientes del año 2005. haremos la conversion a este año 2023 con 1 USD = 813 pesos chilenos."""

naciones["gdp_pesos2023"] = naciones["gdp"]*813
naciones.head(1)

"""##Usaremos describe() para ver las estadisticas del dataset"""

naciones.describe()

"""##Observamos las caracteristicas del gini: Coeficiente de desigualdad del ingreso."""

naciones["gini"].describe()

"""##Contamos la cantidad de paises que tenemos por cada región"""

naciones["region"].value_counts()

naciones.groupby(["region"])[["country"]].count()

"""¿Cuántos países tienen índices de _co2_ mayores a la media?"""

naciones["co2_mayor_a_media"] = np.where(naciones["co2"]> naciones["co2"].mean(), 'si', 'no')

# % de paises que superan la media de valores de CO2
naciones["co2_mayor_a_media"].value_counts('%')

#Graficamos
sns.histplot(naciones, x="co2_mayor_a_media")
plt.xlabel('Sobrepasan la media de CO2')
plt.ylabel('Cantidad de paises')
plt.title('Promedio de emisiones CO2')
plt.show()

"""##Separaremos los datos por region para hacer comparaciones"""

africa = naciones[naciones["region"]=="Africa"]
europa = naciones[naciones["region"]=="Europe"]
america = naciones[naciones["region"]=="Americas"]
asia = naciones[naciones["region"]=="Asia"]
oceania = naciones[naciones["region"]=="Oceania"]

"""##comparamos el nivel de alfabetismos por region"""

# Guardaremos el valor promedio de alfabetización por región
alf_africa = africa["literacy"].mean()
alf_europa = europa["literacy"].mean()
alf_america = america["literacy"].mean()
alf_asia = asia["literacy"].mean()
alf_oceania = oceania["literacy"].mean()

#Graficamos
regiones = ['Africa','Europa','America', 'Asia', 'Oceania']
medias = [alf_africa,alf_europa,alf_america,alf_asia, alf_oceania]
fig, ax = plt.subplots(figsize = (6, 4))
sns.barplot(x=regiones, y=medias,palette = "coolwarm")
plt.xlabel('Región')
plt.ylabel('Prom_Alfabetización')
plt.title('Niveles promedio de alfabetización por Región')
plt.show()

"""## Comparamos el GDP(pib) con los años de escolaridad por regiones"""

g = sns.FacetGrid(naciones, col="region")
g.map_dataframe(sns.scatterplot, x="school", y="gdp")
g.add_legend()

"""## Ahora comparamos el GDP con el nivel de alfabetización"""

g = sns.FacetGrid(naciones, col="region")
g.map_dataframe(sns.scatterplot, x="literacy", y="gdp")
g.add_legend()

"""## Por ultimo comparamos la escolaridad con la alfabetización"""

g = sns.FacetGrid(naciones, col="region")
g.map_dataframe(sns.scatterplot, x="school", y="literacy")
g.add_legend()

"""## vemos la relacion del GDP con la experanza de vida"""

g = sns.FacetGrid(naciones, col="region")
g.map_dataframe(sns.scatterplot, x="gdp", y="life")
g.add_legend()

"""##buscamos una correlacion positiva entre nuesras variables"""

corr = naciones.corr(numeric_only=True)                       #usamos numeric_only=true para trabajar solo con los valores numericos

plt.rcParams["figure.figsize"] =(7,7)                         # ajustamos el tamaño
sns.heatmap(corr, cmap="Oranges", annot=True, linewidth=.5)   #(df, colormap=' ', mostrar valores(true, si es false no se pone)

plt.figure()
sns.pairplot(corr)
plt.show()

"""##Podemos ver fuertes correlaciones positivas entre el promedio de años de escolaridad y tasa de alfabetización, y  entre PIB per capita y CO2.

## Por último, aplicaremos un modelo de regresión lineal para ver la variabilidad de la variable dependiente, la cual es explicado por la vaiabilidad de las variables independientes
"""

#planteamos el modelo
modelo1 = smf.ols("gdp ~ co2", data=naciones)

#Ajustar el modelo utilizando el método .fit()
modelo1 = modelo1.fit()

# mostramos los resultados del modelo
modelo1.summary()

"""OLS (Mínimos Cuadrados Ordinarios):

Coeficiente de Determinación (R-cuadrado): En este caso, el valor es 0.684, lo que significa que aproximadamente el 68.4% de la variabilidad en el PIB puede explicarse por el modelo. Es decir, las emisiones de CO2 tienen una influencia significativa en el crecimiento económico del país.

R-cuadrado ajustado: Es similar al R-cuadrado, pero tiene en cuenta la cantidad de variables incluidas en el modelo. Un valor de 0.682 sugiere que el modelo sigue siendo efectivo incluso después de ajustar la complejidad del modelo.

F-Estadístico: Es una prueba global de la significancia del modelo en su conjunto. Un F-Estadístico alto (373.8 en este caso) y un valor de probabilidad extremadamente bajo (4.27e-45) indican que el modelo es altamente significativo.

Estadístico AIC y BIC: Estos son criterios de información que miden la bondad de ajuste del modelo. Cuanto menor sea su valor, mejor será el ajuste. En este caso, el AIC es 3641 y el BIC es 3647, lo que sugiere un buen ajuste del modelo.

Coeficientes: El modelo proporciona estimaciones de los coeficientes para el intercepto y la variable independiente "co2". En este caso, el intercepto es 4184.3277, lo que representa el valor estimado del PIB cuando las emisiones de CO2 son cero. El coeficiente de "co2" es 444.9360, lo que indica que, en promedio, un aumento de una unidad en las emisiones de CO2 se asocia con un aumento de 444.9360 en el PIB.

Errores estándar: Estos indican la precisión de las estimaciones de los coeficientes. En este caso, los errores estándar son 730.662 para el intercepto y 23.012 para la variable "co2".

Prueba de Hipótesis: Los valores P (P>|t|) indican si los coeficientes son estadísticamente diferentes de cero. Valores P muy bajos (en este caso, p < 0.001) indican que tanto el intercepto como el coeficiente de "co2" son altamente significativos en el modelo.

Los resultados de la regresión indican que hay una relación significativa y positiva entre las emisiones de CO2 y el PIB. Aproximadamente el 68.4% de la variabilidad en el PIB puede ser explicada por las emisiones de CO2. Sin embargo, es importante tener en cuenta que este análisis se basa en datos específicos y la relación causal entre las variables puede estar influenciada por otros factores que no se han incluido en el modelo.
"""

sns.scatterplot(naciones, x='co2', y='gdp', alpha=0.5)
# Crear la línea de regresión ajustada
x = np.linspace(min(naciones['co2']), max(naciones['co2']), 100)
y = modelo1.params[0] + modelo1.params[1] * x
plt.plot(x, y, color='red')
plt.xlabel('CO2')
plt.ylabel('GDP')
plt.title('Relación entre CO2 y GDP')
plt.show()

"""##Elaboramos un segundo modelo, ahora con las variables gdp ~ chldmort + life + school + co2"

"""

modelo2 =smf.ols("gdp ~ chldmort + life + school + co2", data=naciones)

modelo2 =modelo2.fit()

modelo2.summary()

""" Múltiples variables independientes (predictores) para explicar el Producto Interno Bruto (PIB) de un país.

Coeficiente de Determinación (R-cuadrado): El valor de R-cuadrado es 0.813, lo que significa que aproximadamente el 81.3% de la variabilidad en el PIB se puede explicar por las variables incluidas en el modelo. Esto indica que el modelo tiene una muy buena capacidad para explicar las fluctuaciones en el PIB.

R-cuadrado ajustado: El R-cuadrado ajustado es 0.808, lo que sigue siendo alto y sugiere que el modelo es efectivo incluso después de ajustar por la cantidad de variables incluidas.

F-Estadístico: El valor del F-Estadístico es 183.1, y el valor p asociado es extremadamente bajo (2.58e-60), lo que indica que el modelo en su conjunto es altamente significativo.

Coeficientes y Valores P: Cada variable independiente tiene un coeficiente y un valor p asociado que mide su significancia estadística:

Intercepto: El intercepto tiene un valor de -7.351e+04 (aproximadamente -73,510) con un valor p muy bajo (p < 0.001), lo que significa que es estadísticamente significativo y representa el valor estimado del PIB cuando todas las variables independientes son cero.

chldmort: El coeficiente de "chldmort" es 148.4275 con un valor p extremadamente bajo (p < 0.001). Esto sugiere que la tasa de mortalidad infantil (chldmort) tiene un efecto significativo y positivo en el PIB.

life: El coeficiente de "life" es 924.2773 con un valor p muy bajo (p < 0.001). Esto indica que la esperanza de vida (life) también tiene un impacto significativo y positivo en el PIB.

school: El coeficiente de "school" es 1162.4090 con un valor p muy bajo (p < 0.001). Esto significa que la duración promedio de la educación (school) tiene una influencia significativa y positiva en el PIB.

co2: El coeficiente de "co2" es 359.4860 con un valor p extremadamente bajo (p < 0.001). Esto indica que las emisiones de CO2 (co2) tienen un efecto significativo y positivo en el PIB.

Errores estándar: Cada coeficiente tiene un error estándar asociado, que mide la precisión de la estimación. Los errores estándar permiten evaluar la fiabilidad de los coeficientes.

Pruebas de Hipótesis: En este caso, todos los valores p para los coeficientes son muy bajos, lo que indica que todas las variables independientes tienen una asociación significativa con el PIB.

Estadísticas de Residuos: El valor de Durbin-Watson es 1.878, que sugiere que los residuos pueden no estar correlacionados (autocorrelación). El valor de Jarque-Bera es 87.940, lo que indica cierta desviación de la normalidad en los residuos.

Condición Numérica: La alta condición numérica (1.99e+03) sugiere que podría haber problemas de multicolinealidad o problemas numéricos debido a la correlación entre las variables independientes.

Elmodelo muestra que las variables "chldmort", "life", "school" y "co2" tienen una influencia significativa y positiva en el PIB. Alrededor del 81.3% de la variabilidad en el PIB se puede explicar mediante estas variables. Sin embargo, es importante recordar que el análisis de regresión no establece relaciones causales y que otros factores no incluidos en el modelo también pueden influir en el PIB.
"""

fig, axs = plt.subplots(2, 2, figsize=(10, 8))
axs[0, 0].scatter(naciones['chldmort'], naciones['gdp'], alpha=0.5)
axs[0, 0].set_xlabel('chldmort')
axs[0, 0].set_ylabel('gdp')

axs[0, 1].scatter(naciones['life'], naciones['gdp'], alpha=0.5)
axs[0, 1].set_xlabel('life')
axs[0, 1].set_ylabel('gdp')

axs[1, 0].scatter(naciones['school'], naciones['gdp'], alpha=0.5)
axs[1, 0].set_xlabel('school')
axs[1, 0].set_ylabel('gdp')

axs[1, 1].scatter(naciones['co2'], naciones['gdp'], alpha=0.5)
axs[1, 1].set_xlabel('co2')
axs[1, 1].set_ylabel('gdp')
plt.tight_layout()   #Ajustamos los gráficos
plt.show()