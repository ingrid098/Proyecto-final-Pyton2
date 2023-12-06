import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


print("\n--------------Dataset de ventas de una empresa automotriz----------------\n")

# Leer el DataFrame original
df_autos = pd.read_csv(
    r"C:\Users\ingri\OneDrive\Escritorio\dataframe\Datasets_Proyecto_Python2\Auto Sales data.csv")
print("\n-----------DataFrame original-----------\n")
df_autos.info()

# 2. LIMPIEZA

# Eliminar las filas con valores nulos
print("\n------------DataFrame sin valores nulos------------\n")
df_autos = df_autos.dropna()
df_autos.info()

# Verificar duplicados
print("\n------------Valores duplicados------------\n")
duplicados_total = df_autos.duplicated()
print(df_autos[duplicados_total])

# Eliminar duplicados
print("\n------------DataFrame sin duplicados------------\n")
df_autos = df_autos.drop_duplicates()
df_autos.info()

# Crear subconjunto
df_autos_sub = df_autos[["ORDERNUMBER", "QUANTITYORDERED", "SALES", "ORDERDATE",
                         "DAYS_SINCE_LASTORDER", "STATUS", "PRODUCTLINE",
                         "PRODUCTCODE", "COUNTRY", "CITY"]]

print("\n------------Subconjunto del DataFrame ------------\n")
df_autos_sub.info()

# Convierte la columna 'ORDERDATE' en datetime
df_autos_sub = df_autos_sub.sort_values(by="ORDERDATE")
df_autos_sub["ORDERDATE"] = pd.to_datetime(
    df_autos_sub["ORDERDATE"], format="%d/%m/%Y")

# 3.1 PARAMETROS ESTADISTICOS DEL DATASET
print("\n------------Estadisticas descriptivas para columnas numericas:------------\n")
print(df_autos_sub.describe())
print()
# 3.2 MOSTRAR MATRIZ DE CORRELACION


def factorizar_y_correlacion(df):
    # Factorizar DataFrame
    df_factorizado = df_autos_sub.apply(lambda x: pd.factorize(x)[0])

    # Calcular la matriz de correlacion
    corr_matrix = df_factorizado.corr()
    print(corr_matrix)

    # Visualizar la matriz de correlacion
    decision = input(
        "\n¿Quieres ver la matriz de correlacion representada en un mapa de calor?.Escribe si o no: \n")
    if decision.lower() == "si":
        plt.figure(figsize=(10, 10))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm",
                    fmt=".2f", linewidths=.5)
        plt.title("Matriz de Correlacion")
        plt.xticks(rotation=25, ha="right")
        plt.show()
    else:
        print("Sigamos")
    return df_factorizado, corr_matrix


# Llamada a la funcion
resultados_factorizacion = factorizar_y_correlacion(df_autos_sub)

# 3.3 OPERACIONES DE AGRUPAMIENTO Y AGREGACION
print("\n------------OPERACIONES DE AGRUPAMIENTO Y AGREGACIÓN:------------\n")

# Agrupar por pais
grupo_pais = df_autos_sub.groupby("COUNTRY")
# Aplicar multiples funciones de agregacion
resumen_pais = grupo_pais.agg({
    "SALES": ["sum"],
    "QUANTITYORDERED": ["mean"],
    "COUNTRY": ["size"]})

# Renombrar columnas
resumen_pais.columns = [
    "Ventas (Suma)", "Cantidad (Promedio)", "Registros (Total)"]

# Redondear decimales
print("\nResumen por pais:\n", resumen_pais.round(2).head())

# Agrupar por linea de producto
grupo_linea_producto = df_autos_sub.groupby("PRODUCTLINE")

# Aplicar múltiples funciones de agregacion
resumen_linea_producto = grupo_linea_producto.agg({
    "SALES": ["sum"],
    "QUANTITYORDERED": ["mean"],
    "PRODUCTLINE": ["size"]
})

resumen_linea_producto.columns = [
    "Ventas (Suma)", "Cantidad (Promedio)", "Registros (Total)"]

# Redondear decimales
print("\nResumen por linea de producto :\n",
      resumen_linea_producto.round(2).head())

# 3.4 PARA EL DATASET CON SERIE DE TIEMPO

# Crear tabla pivotante
pvt_autos = df_autos_sub.pivot_table(
    index="ORDERDATE", columns="PRODUCTLINE", values="SALES", aggfunc="sum")
print("------------TABLA PIVOTE---------")
print(pvt_autos.head())


# Asegurate de ordenar el indice y convertirlo a datetime
pvt_autos = pvt_autos.sort_index()
pvt_autos.index = pd.to_datetime(pvt_autos.index, format="%d/%m/%Y")


# 4.Graficos
# Grafico de lineas para las ventas a lo largo del tiempo por linea de producto
def plot_line(pvt_autos):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=pvt_autos.resample("M").sum(), dashes=False)
    plt.title("Ventas a lo largo del tiempo por Linea de Producto")
    plt.xlabel("Fecha de Orden")
    plt.ylabel("Ventas")
    plt.show()

# Grafico de barras apiladas para las ventas por linea de producto a lo largo del tiempo


def plot_bar_productline(pvt_autos):
    plt.figure(figsize=(12, 6))
    # pvt_autos.resample("Y").sum().plot(kind="bar", stacked=True)
    sns.barplot(data=pvt_autos.resample("Y").sum().stack().reset_index(),
                x="ORDERDATE", y=0, hue="PRODUCTLINE")
    plt.title("Ventas por Linea de Producto a lo largo del tiempo")
    plt.xlabel("Fecha de Orden")
    plt.xticks(rotation=360, ha="right")
    plt.ylabel("Ventas")
    plt.show()

# Grafico de Barras para la Cantidad de Pedidos por Pais#


def plot_bar_country(resumen_pais):
    plt.figure(figsize=(12, 6))
    sns.barplot(x=resumen_pais.index, y=resumen_pais["Registros (Total)"])
    plt.title("Cantidad de Pedidos por Pais")
    plt.xlabel("Pais")
    plt.ylabel("Cantidad de Pedidos")
    plt.xticks(rotation=45, ha="right")
    plt.show()

# Grafico de Puntos para la Cantidad de Pedidos por Linea de Producto


def plot_bar_productlin_total(resumen_linea_producto):
    plt.figure(figsize=(12, 6))
    sns.pointplot(x=resumen_linea_producto.index,
                  y="Registros (Total)", data=resumen_linea_producto)
    plt.title("Cantidad de Pedidos por Linea de Producto")
    plt.xlabel("Linea de Producto")
    plt.ylabel("Cantidad de Pedidos")
    plt.xticks(rotation=50, ha="right")
    plt.show()


while True:
    print("\nSeleccione el grafico que desea visualizar:")
    print("1. Ventas a lo largo del tiempo por linea de producto")
    print("2. ventas por linea de producto a lo largo del tiempo")
    print("3. Cantidad de Pedidos por Pais")
    print("4. Cantidad de Pedidos por Linea de Producto")
    print("0. Salir")

    opcion = input("Ingrese el numero de la opcion (0-4): ")

    # Verificar y mostrar el gráfico según la elección del usuario
    if opcion == '0':
        print("Gracias")
        break
    elif opcion == '1':
        plot_line(pvt_autos)
    elif opcion == '2':
        plot_bar_productline(pvt_autos)
    elif opcion == '3':
        plot_bar_country(resumen_pais)
    elif opcion == '4':
        plot_bar_productlin_total(resumen_linea_producto)
    else:
        print("Opción no reconocida. Por favor, selecciona una opción valida.\n")

