# Análisis del rendimiento académico

Proyecto de análisis exploratorio de datos desarrollado para la práctica
**"Git, GitHub y reproducibilidad de proyectos de datos"** (asignatura Big
Data). El objetivo es analizar el desempeño de un grupo de estudiantes en
tres áreas (matemáticas, lectura y escritura) para identificar patrones
relacionados con sus resultados académicos.

## Dataset

- **Nombre:** Students Performance in Exams
- **Fuente:** [Kaggle - spscientist/students-performance-in-exams](https://www.kaggle.com/datasets/spscientist/students-performance-in-exams)
- **Descripción breve:** contiene 1000 registros de estudiantes con datos
  demográficos (género, grupo étnico, nivel educativo de los padres, tipo de
  almuerzo, si completaron un curso de preparación) y sus calificaciones en
  matemáticas, lectura y escritura (0-100).

## Objetivo

Realizar un análisis exploratorio del dataset para identificar patrones
relacionados con el rendimiento académico de los estudiantes: comparar las
tres áreas evaluadas, evaluar el efecto del curso de preparación y del nivel
educativo de los padres, y clasificar a los estudiantes según su desempeño
general.

## Requisitos

- Python 3.10 o superior
- Las dependencias incluidas en `requirements.txt` (pandas, matplotlib,
  numpy)

## Instalación

Clonar el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
```

Entrar al proyecto:

```bash
cd academic-performance-analysis
```

Crear el entorno virtual:

```bash
python -m venv .venv
```

Activarlo:

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python src/analysis.py
```

El script imprime todo el proceso en consola y además guarda los resultados
en `outputs/resultados/`:

- `resultados.txt`: reporte completo de la exploración, el análisis y las
  conclusiones.
- `dataset_procesado.csv`: dataset final con las variables `average_score`
  y `performance_level` ya calculadas.
- 5 gráficas en formato `.png`.

## Análisis realizados

1. **Exploración inicial:** número de registros y columnas, tipos de datos,
   valores faltantes, duplicados y estadísticas descriptivas.
2. **Limpieza y preprocesamiento:** normalización de nombres de columnas a
   snake_case y verificación de valores faltantes/duplicados (el dataset no
   presentó ninguno).
3. **Variable `average_score`:** promedio de `math_score`, `reading_score`
   y `writing_score`.
4. **Clasificación del rendimiento** (`performance_level`) en tres
   categorías, según el `average_score`:
   - `Bajo`: menor a 60
   - `Medio`: entre 60 y 80
   - `Alto`: mayor o igual a 80
5. **Análisis realizados** (más del mínimo de 4 solicitado):
   - ¿Cuál de las tres áreas tiene el promedio más alto?
   - ¿Los estudiantes que completaron el curso de preparación obtienen
     mejores resultados?
   - ¿Existen diferencias según el nivel educativo de los padres?
   - ¿Qué porcentaje de estudiantes alcanza cada categoría de rendimiento?
   - ¿Qué grupos étnicos presentan los promedios más altos y más bajos?
   - ¿Existen diferencias de rendimiento por área entre géneros?
6. **Visualizaciones** (más del mínimo de 3 solicitado):
   - Histograma de `average_score`
   - Promedio según curso de preparación
   - Promedio según nivel educativo de los padres
   - Boxplot comparando las tres áreas
   - Número de estudiantes por nivel de rendimiento

## Resultados y conclusiones

- El área con mejor promedio es lectura, aunque las tres áreas presentan
  resultados bastante homogéneos entre sí.
- Haber completado el curso de preparación se asocia con un promedio
  general más alto (~7.6 puntos de diferencia).
- A mayor nivel educativo de los padres, mayor tiende a ser el promedio de
  los estudiantes.
- Poco más de la mitad de los estudiantes (51.7%) se ubica en la categoría
  de rendimiento "Medio", el 19.8% en "Alto" y el 28.5% en "Bajo".
- Existen diferencias de rendimiento entre los distintos grupos étnicos del
  dataset, lo que sugiere la influencia de factores socioeconómicos u otras
  variables no incluidas explícitamente en los datos.

El reporte completo con todos los valores numéricos se encuentra en
`outputs/resultados/resultados.txt` tras ejecutar el script.
