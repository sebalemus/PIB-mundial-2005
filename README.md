# PIB-mundial-2005
En este notebook analizaremos las distintas variables de desarrollo humano en los distintos paises de todos los continentes segun su PIB del año 2005
El dataset 'nations', contiene información sobre diferentes atributos de desarrollo humano en 194 países, recolectados por las Naciones Unidas en el año 2005.

Contiene información a nivel mundial sobre demografía:
country: País.
region: Continente del país.
gdp: Producto Interno Bruto per cápita, precios 2005.
school: Promedio años de escolaridad.
adfert: Fertilidad adolescente (Nacimientos 1:1000 en mujeres entre 15 y 19).
chldmort: Probabilidad de muerte antes de los 5 años por cada 1000.
life: Esperanza de vida al nacer.
pop: Población total.
urban: Porcentaje de población urbana.
femlab: Tasa entre hombres y mujeres en el mercado laboral.
literacy: Tasa de alfabetismo.
co2: Toneladas de Co2 emitidas per cápita.
gini: Coeficiente de desigualdad del ingreso.

Conclusiones
OLS (Mínimos Cuadrados Ordinarios):
Coeficiente de Determinación (R-cuadrado): En este caso, el valor es 0.684, lo que significa que aproximadamente el 68.4% de la variabilidad en el PIB puede explicarse por el modelo. Es decir, las emisiones de CO2 tienen una influencia significativa en el crecimiento económico del país.
R-cuadrado ajustado: Es similar al R-cuadrado, pero tiene en cuenta la cantidad de variables incluidas en el modelo. Un valor de 0.682 sugiere que el modelo sigue siendo efectivo incluso después de ajustar la complejidad del modelo.
F-Estadístico: Es una prueba global de la significancia del modelo en su conjunto. Un F-Estadístico alto (373.8 en este caso) y un valor de probabilidad extremadamente bajo (4.27e-45) indican que el modelo es altamente significativo.
Estadístico AIC y BIC: Estos son criterios de información que miden la bondad de ajuste del modelo. Cuanto menor sea su valor, mejor será el ajuste. En este caso, el AIC es 3641 y el BIC es 3647, lo que sugiere un buen ajuste del modelo.
Coeficientes: El modelo proporciona estimaciones de los coeficientes para el intercepto y la variable independiente "co2". En este caso, el intercepto es 4184.3277, lo que representa el valor estimado del PIB cuando las emisiones de CO2 son cero. El coeficiente de "co2" es 444.9360, lo que indica que, en promedio, un aumento de una unidad en las emisiones de CO2 se asocia con un aumento de 444.9360 en el PIB.
Errores estándar: Estos indican la precisión de las estimaciones de los coeficientes. En este caso, los errores estándar son 730.662 para el intercepto y 23.012 para la variable "co2".
Prueba de Hipótesis: Los valores P (P>|t|) indican si los coeficientes son estadísticamente diferentes de cero. Valores P muy bajos (en este caso, p < 0.001) indican que tanto el intercepto como el coeficiente de "co2" son altamente significativos en el modelo.

Los resultados de la regresión indican que hay una relación significativa y positiva entre las emisiones de CO2 y el PIB. Aproximadamente el 68.4% de la variabilidad en el PIB puede ser explicada por las emisiones de CO2. Sin embargo, es importante tener en cuenta que este análisis se basa en datos específicos y la relación causal entre las variables puede estar influenciada por otros factores que no se han incluido en el modelo.
