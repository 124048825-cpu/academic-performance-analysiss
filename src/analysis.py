"""
Proyecto 1 - Análisis del rendimiento académico
Dataset: Students Performance in Exams (Kaggle)
Asignatura: Big Data - Práctica Git, GitHub y reproducibilidad

Este script realiza:
1. Carga del dataset
2. Exploración inicial
3. Limpieza y preprocesamiento
4. Creación de la variable average_score
5. Clasificación del rendimiento académico (Bajo / Medio / Alto)
6. Análisis (mínimo 4)
7. Visualizaciones (mínimo 3)
8. Conclusiones

Todos los resultados de texto se guardan en outputs/resultados/resultados.txt
y las gráficas se guardan como imágenes .png en outputs/resultados/.
"""

import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # evita necesitar una interfaz gráfica al ejecutar el script
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Configuración de rutas
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "students_performance.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs", "resultados")
os.makedirs(OUTPUT_DIR, exist_ok=True)

RESULTS_LINES = []  # aquí se van acumulando todas las líneas del reporte de texto


def log(texto=""):
    """Imprime el texto en consola y lo guarda para el reporte final."""
    print(texto)
    RESULTS_LINES.append(str(texto))


def seccion(titulo):
    log("\n" + "=" * 70)
    log(titulo)
    log("=" * 70)


# ---------------------------------------------------------------------------
# 1. Carga del dataset
# ---------------------------------------------------------------------------
seccion("1. CARGA DEL DATASET")
df = pd.read_csv(DATA_PATH)
log(f"Dataset cargado desde: {DATA_PATH}")

# ---------------------------------------------------------------------------
# 2. Exploración inicial
# ---------------------------------------------------------------------------
seccion("2. EXPLORACIÓN INICIAL")

log(f"Número de registros: {df.shape[0]}")
log(f"Número de columnas: {df.shape[1]}")

log("\nNombre de las variables:")
for col in df.columns:
    log(f" - {col}")

log("\nTipos de datos:")
log(df.dtypes.to_string())

log("\nValores faltantes por columna:")
log(df.isnull().sum().to_string())

n_duplicados = df.duplicated().sum()
log(f"\nRegistros duplicados: {n_duplicados}")

log("\nEstadísticas descriptivas (variables numéricas):")
log(df.describe().to_string())

# ---------------------------------------------------------------------------
# 3. Limpieza y preprocesamiento
# ---------------------------------------------------------------------------
seccion("3. LIMPIEZA Y PREPROCESAMIENTO")

# Renombramos las columnas a un formato snake_case, más cómodo para trabajar
# en Python (evita espacios y caracteres especiales como "/").
df = df.rename(columns={
    "gender": "gender",
    "race/ethnicity": "race_ethnicity",
    "parental level of education": "parental_education",
    "lunch": "lunch",
    "test preparation course": "test_preparation",
    "math score": "math_score",
    "reading score": "reading_score",
    "writing score": "writing_score",
})
log("Se renombraron las columnas a formato snake_case (sin espacios ni '/').")

# El dataset no presenta valores faltantes ni duplicados (confirmado en el
# paso anterior), por lo que no fue necesario imputar ni eliminar registros.
# Aun así, se deja el código preparado por si en otra ejecución aparecieran:
if df.isnull().sum().sum() > 0:
    df = df.dropna()
    log("Se eliminaron filas con valores faltantes.")
else:
    log("No se encontraron valores faltantes: no fue necesario imputar nada.")

if n_duplicados > 0:
    df = df.drop_duplicates()
    log(f"Se eliminaron {n_duplicados} registros duplicados.")
else:
    log("No se encontraron registros duplicados.")

# Verificamos que las columnas categóricas no tengan inconsistencias de
# capitalización o espacios extra.
cat_cols = ["gender", "race_ethnicity", "parental_education", "lunch", "test_preparation"]
for c in cat_cols:
    df[c] = df[c].str.strip()

# ---------------------------------------------------------------------------
# 4. Creación de la variable average_score
# ---------------------------------------------------------------------------
seccion("4. VARIABLE average_score")

df["average_score"] = (df["math_score"] + df["reading_score"] + df["writing_score"]) / 3
df["average_score"] = df["average_score"].round(2)
log("Se creó la variable 'average_score' como el promedio de math_score, "
    "reading_score y writing_score.")
log(df["average_score"].describe().to_string())

# ---------------------------------------------------------------------------
# 5. Clasificación del rendimiento académico
# ---------------------------------------------------------------------------
seccion("5. CLASIFICACIÓN DEL RENDIMIENTO ACADÉMICO")

log(
    "Criterios utilizados para clasificar 'average_score' en tres categorías:\n"
    "  - Bajo:  average_score < 60\n"
    "  - Medio: 60 <= average_score < 80\n"
    "  - Alto:  average_score >= 80\n\n"
    "Justificación: se utiliza 60 como umbral típico de aprobación/desempeño "
    "mínimo aceptable y 80 como umbral de desempeño sobresaliente, en línea "
    "con escalas de calificación de 0 a 100 usadas habitualmente en contextos "
    "educativos."
)


def clasificar(promedio):
    if promedio < 60:
        return "Bajo"
    elif promedio < 80:
        return "Medio"
    else:
        return "Alto"


df["performance_level"] = df["average_score"].apply(clasificar)

log("\nDistribución de estudiantes por categoría de rendimiento:")
log(df["performance_level"].value_counts().to_string())

# ---------------------------------------------------------------------------
# 6. Análisis (mínimo 4)
# ---------------------------------------------------------------------------
seccion("6. ANÁLISIS")

# --- Análisis 1: ¿Cuál de las tres áreas tiene el promedio más alto? -------
log("\n--- Análisis 1: ¿Cuál de las tres áreas tiene el promedio más alto? ---")
promedios_area = {
    "math_score": df["math_score"].mean(),
    "reading_score": df["reading_score"].mean(),
    "writing_score": df["writing_score"].mean(),
}
for area, valor in promedios_area.items():
    log(f"Promedio en {area}: {valor:.2f}")
area_top = max(promedios_area, key=promedios_area.get)
log(f"El área con el promedio más alto es: {area_top}")

# --- Análisis 2: curso de preparación vs resultados -------------------------
log("\n--- Análisis 2: ¿Los estudiantes que realizaron el curso de "
    "preparación presentan mejores resultados? ---")
prep_group = df.groupby("test_preparation")["average_score"].mean()
log(prep_group.to_string())
diferencia_prep = prep_group.get("completed", 0) - prep_group.get("none", 0)
log(f"Diferencia (completed - none): {diferencia_prep:.2f} puntos")

# --- Análisis 3: nivel educativo de los padres ------------------------------
log("\n--- Análisis 3: ¿Existen diferencias en el rendimiento según el "
    "nivel educativo de los padres? ---")
parental_group = df.groupby("parental_education")["average_score"].mean().sort_values(ascending=False)
log(parental_group.to_string())

# --- Análisis 4: porcentaje de estudiantes por categoría de rendimiento ----
log("\n--- Análisis 4: ¿Qué porcentaje de estudiantes alcanza cada "
    "categoría de rendimiento? ---")
porcentaje_categoria = (df["performance_level"].value_counts(normalize=True) * 100).round(2)
log(porcentaje_categoria.to_string())

# --- Análisis 5 (adicional): grupos con promedios más altos y más bajos ----
log("\n--- Análisis 5 (adicional): ¿Qué grupos (race/ethnicity) presentan "
    "los promedios más altos y más bajos? ---")
grupo_promedio = df.groupby("race_ethnicity")["average_score"].mean().sort_values(ascending=False)
log(grupo_promedio.to_string())
log(f"Grupo con promedio más alto: {grupo_promedio.idxmax()} "
    f"({grupo_promedio.max():.2f})")
log(f"Grupo con promedio más bajo: {grupo_promedio.idxmin()} "
    f"({grupo_promedio.min():.2f})")

# --- Análisis 6 (adicional): diferencia por género --------------------------
log("\n--- Análisis 6 (adicional): ¿Existen diferencias de rendimiento "
    "entre géneros por área? ---")
genero_area = df.groupby("gender")[["math_score", "reading_score", "writing_score"]].mean()
log(genero_area.to_string())

# ---------------------------------------------------------------------------
# 7. Visualizaciones (mínimo 3)
# ---------------------------------------------------------------------------
seccion("7. VISUALIZACIONES")

# --- Visualización 1: histograma de average_score ---------------------------
plt.figure(figsize=(8, 5))
plt.hist(df["average_score"], bins=20, color="#4C72B0", edgecolor="white")
plt.title("Distribución del promedio general (average_score)")
plt.xlabel("Promedio general")
plt.ylabel("Número de estudiantes")
plt.tight_layout()
ruta1 = os.path.join(OUTPUT_DIR, "01_histograma_average_score.png")
plt.savefig(ruta1, dpi=150)
plt.close()
log(f"Guardada: {ruta1}")

# --- Visualización 2: promedio por curso de preparación ---------------------
plt.figure(figsize=(6, 5))
prep_group.plot(kind="bar", color=["#DD8452", "#4C72B0"])
plt.title("Promedio general según curso de preparación")
plt.xlabel("Curso de preparación")
plt.ylabel("Promedio general")
plt.xticks(rotation=0)
plt.tight_layout()
ruta2 = os.path.join(OUTPUT_DIR, "02_promedio_por_test_preparation.png")
plt.savefig(ruta2, dpi=150)
plt.close()
log(f"Guardada: {ruta2}")

# --- Visualización 3: promedio por nivel educativo de los padres -----------
plt.figure(figsize=(9, 5))
parental_group.plot(kind="barh", color="#55A868")
plt.title("Promedio general según nivel educativo de los padres")
plt.xlabel("Promedio general")
plt.ylabel("Nivel educativo de los padres")
plt.tight_layout()
ruta3 = os.path.join(OUTPUT_DIR, "03_promedio_por_parental_education.png")
plt.savefig(ruta3, dpi=150)
plt.close()
log(f"Guardada: {ruta3}")

# --- Visualización 4 (adicional): boxplot de las tres áreas -----------------
plt.figure(figsize=(7, 5))
plt.boxplot(
    [df["math_score"], df["reading_score"], df["writing_score"]],
    tick_labels=["math_score", "reading_score", "writing_score"],
)
plt.title("Distribución de calificaciones por área")
plt.ylabel("Calificación")
plt.tight_layout()
ruta4 = os.path.join(OUTPUT_DIR, "04_boxplot_areas.png")
plt.savefig(ruta4, dpi=150)
plt.close()
log(f"Guardada: {ruta4}")

# --- Visualización 5 (adicional): distribución de niveles de rendimiento --
plt.figure(figsize=(6, 5))
df["performance_level"].value_counts().reindex(["Bajo", "Medio", "Alto"]).plot(
    kind="bar", color=["#C44E52", "#DD8452", "#55A868"]
)
plt.title("Número de estudiantes por nivel de rendimiento")
plt.xlabel("Nivel de rendimiento")
plt.ylabel("Número de estudiantes")
plt.xticks(rotation=0)
plt.tight_layout()
ruta5 = os.path.join(OUTPUT_DIR, "05_niveles_de_rendimiento.png")
plt.savefig(ruta5, dpi=150)
plt.close()
log(f"Guardada: {ruta5}")

# ---------------------------------------------------------------------------
# 8. Conclusiones
# ---------------------------------------------------------------------------
seccion("8. CONCLUSIONES")

conclusiones = f"""
1. El área con el promedio más alto es '{area_top}' ({promedios_area[area_top]:.2f}
   puntos), mientras que las otras dos áreas presentan promedios muy
   cercanos entre sí, lo que sugiere que el rendimiento de los estudiantes
   es relativamente consistente entre materias.

2. Los estudiantes que completaron el curso de preparación ('completed')
   obtienen en promedio {diferencia_prep:.2f} puntos más que quienes no lo
   tomaron ('none'). Esto indica una asociación positiva entre haber tomado
   el curso de preparación y un mejor desempeño académico.

3. El nivel educativo de los padres sí está relacionado con el rendimiento:
   el grupo con promedios más altos es '{parental_group.idxmax()}'
   ({parental_group.max():.2f}) y el más bajo es '{parental_group.idxmin()}'
   ({parental_group.min():.2f}), lo que sugiere que un mayor nivel educativo
   de los padres se asocia con mejores resultados de los estudiantes.

4. Según la clasificación de rendimiento definida (Bajo < 60, Medio 60-80,
   Alto >= 80), el {porcentaje_categoria.get('Medio', 0):.2f}% de los
   estudiantes se ubica en la categoría 'Medio', el
   {porcentaje_categoria.get('Alto', 0):.2f}% en 'Alto' y el
   {porcentaje_categoria.get('Bajo', 0):.2f}% en 'Bajo'.

5. El grupo étnico '{grupo_promedio.idxmax()}' presenta el promedio más alto
   y '{grupo_promedio.idxmin()}' el más bajo, lo que muestra diferencias de
   rendimiento entre grupos que podrían estar relacionadas con factores
   socioeconómicos u otras variables no incluidas en el dataset.

En conjunto, los resultados muestran que factores externos como el curso de
preparación y el entorno familiar (nivel educativo de los padres) están
asociados con el rendimiento académico, mientras que el desempeño entre las
tres áreas evaluadas (matemáticas, lectura y escritura) es bastante
homogéneo.
"""
log(conclusiones)

# ---------------------------------------------------------------------------
# Guardar reporte de texto y dataset procesado
# ---------------------------------------------------------------------------
reporte_path = os.path.join(OUTPUT_DIR, "resultados.txt")
with open(reporte_path, "w", encoding="utf-8") as f:
    f.write("\n".join(RESULTS_LINES))

dataset_procesado_path = os.path.join(OUTPUT_DIR, "dataset_procesado.csv")
df.to_csv(dataset_procesado_path, index=False)

print(f"\nReporte de texto guardado en: {reporte_path}")
print(f"Dataset procesado guardado en: {dataset_procesado_path}")
