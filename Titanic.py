import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("------------\nDataset sobre el hundimiento del titanic--------------\n")

df_titanic = pd.read_csv(
    r"C:\Users\ingri\OneDrive\Escritorio\dataframe\Datasets_Proyecto_Python2\titanic.csv")
print("\n-----------DataFrame original-----------\n")
df_titanic.info()

# 2. LIMPIEZA

print("\n------------DataFrame sin valores nulos------------\n")

# Se decidio sacar media columna Age
df_titanic['Age'].fillna(df_titanic['Age'].median(), inplace=True)

# Eliminar columna con muchos datos nulos
df_titanic.drop('Cabin', axis=1, inplace=True)
df_titanic.info()

# Elimiar datos nulos
df_titanic.dropna(subset=['Embarked'], inplace=True)

# Verificar duplicados
duplicados_total = df_titanic.duplicated()
# print(df_titanic[duplicados_total])
# no hay valores duplicados

df_titanic["Age"] = df_titanic["Age"].astype(int)

# Crear subconjunto
df_titanic_sub = df_titanic[["Survived", "Sex", "Age",
                             "Pclass", "Embarked", "SibSp", "Parch"]]
print("\n------------Subconjunto del DataFrame ------------\n")
df_titanic_sub.info()


# 3.1 PARAMETROS ESTADISTICOS DEL DATASET
print("\n------------Estadisticas descriptivas para columnas numericas:------------\n")

print(df_titanic_sub.describe())

print("Edad minima")
minimo = df_titanic_sub["Age"].min()
print(minimo)
print("Edad maxima")
maximo = df_titanic_sub["Age"].max()
print(maximo)

# 3.2 MOSTRAR MATRIZ DE CORRELACION


def factorizar_y_correlacion(df):
    df_factorizado = df.apply(lambda x: pd.factorize(x)[0])
    corr_matrix = df_factorizado.corr()
    print(corr_matrix)

    decision = input(
        "\n¿Quieres ver la matriz de correlacion representada en un mapa de calor? Escribe 'si' o 'no':\n")
    if decision.lower() == "si":
        plt.figure(figsize=(10, 10))
        sns.heatmap(corr_matrix, annot=True, cmap="coolwarm",
                    fmt=".2f", linewidths=.5)
        plt.title("Matriz de Correlacion")
        plt.show()
    else:
        print("Sigamos")

    return df_factorizado, corr_matrix


df_titanic_sub_correl = factorizar_y_correlacion(df_titanic_sub)

# 3.3 OPERACIONES DE AGRUPAMIENTO Y AGREGACION
print("\n------------OPERACIONES DE AGRUPAMIENTO Y AGREGACION:------------\n")

grupo_sexo_clase = df_titanic_sub.groupby(["Sex", "Pclass"])
resumen_sexo_clase = grupo_sexo_clase.agg({
    "Survived": ["mean"],
    "Age": ["mean", "min", "max"],
    "SibSp": ["sum"],
    "Parch": ["sum"]
})

resumen_sexo_clase.columns = [
    "Tasa Supervivencia", "Edad (Promedio)", "Edad (Minima)", "Edad (Maxima)", "Total SibSp", "Total Parch"]

print("\nResumen por sexo y clase:\n",
      resumen_sexo_clase.round(2).head())


# 4.Graficos
# Grafico de barras de tasa de supervivencia


def plot_survival_bar_chart():
    sns.barplot(x=resumen_sexo_clase.index.get_level_values(
        'Sex'), y=resumen_sexo_clase["Tasa Supervivencia"].values * 100,
        hue=resumen_sexo_clase.index.get_level_values('Pclass'))
    plt.title("Tasa de Supervivencia Promedio por Clase y Sexo")
    plt.xlabel("Sexo")
    plt.ylabel("Tasa de Supervivencia Promedio (%)")
    plt.legend(title="Clase")
    plt.show()

# Grafico de cajas de Age por Embarked y Sex


def plot_age_box_chart():
    sns.boxplot(x="Embarked", y="Age", hue="Sex",
                data=df_titanic_sub, palette="Set2")
    plt.title("Age por Embarked y Sex")
    plt.show()

# Histograma de Age por Survived


def plot_age_histogram():
    sns.histplot(data=df_titanic_sub, x='Age', bins=30, hue='Survived',
                 multiple='stack', kde=True, palette='Set1')
    plt.title('Distribución de Edades segun Sobrevivencia')
    plt.xlabel('Edad')
    plt.ylabel('Frecuencia')
    plt.legend(title='Survived', labels=['No Sobrevivió', 'Sobrevivio'])
    plt.show()

# Grafico de barras de numero de pasajeros por Pclass


def plot_passenger_count_bar_chart():
    sns.countplot(x='Pclass', data=df_titanic_sub, palette='Set1')
    plt.title('Distribucion de Pasajeros por Clase')
    plt.xlabel('Clase')
    plt.ylabel('Numero de Pasajeros')
    plt.show()

# Grafico de violin para Age por Pclass


def plot_age_violin_chart():
    sns.violinplot(x='Pclass', y='Age', data=df_titanic_sub,
                   hue='Sex', split=True, palette='pastel')
    plt.title('Distribucion de Edades por Clase y Sexo')
    plt.xlabel('Clase')
    plt.ylabel('Edad')
    plt.show()



# Menu interactivo

while True:
    print("\nSeleccione el grafico que desea visualizar:")
    print("1. Tasa de Supervivencia por Clase y Sexo")
    print("2. Age por Embarked y Sex")
    print("3. Histograma de Age por Sobrevivencia")
    print("4. Distribución de Pasajeros por Clase")
    print("5. Age por Clase y Sexo")
    print("0. Salir")

    opcion = input("Ingrese el numero de la opcion (0-5): ")
    plt.figure(figsize=(12, 6))
    if opcion == "1":
        plot_survival_bar_chart()
    elif opcion == "2":
        plot_age_box_chart()
    elif opcion == "3":
        plot_age_histogram()
    elif opcion == "4":
        plot_passenger_count_bar_chart()
    elif opcion == "5":
        plot_age_violin_chart()
    elif opcion == "0":
        print("Gracias")
        break
    else:
        print("Opción no valida. Por favor, ingrese un numero del 0 al 5.")

