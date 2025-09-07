import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configurar el estilo de matplotlib para mejor visualización
plt.style.use('default')
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 8)

# Leer el archivo CSV
df = pd.read_csv('../Datos_autocompasion/Resultados/Datos_fase2_promedios.csv')

# Filtrar datos PRE y POST
pre_data = df[df['Fase'].str.contains('PRE', na=False)]
post_data = df[df['Fase'].str.contains('POST', na=False)]

# Obtener participantes únicos
participantes = sorted(df['Participante'].unique())

# Configurar el gráfico
fig, ax = plt.subplots(figsize=(14, 8))

# Crear el fondo con colores según los rangos especificados
y_min, y_max = 1.0, 5.0
ax.set_ylim(y_min, y_max)

# Crear las regiones de color de fondo
# Rojo suave: 1.0 a 2.49
ax.axhspan(1.0, 2.49, alpha=0.3, color='red', label='Bajo (1.0-2.49)')
# Amarillo suave: 2.5 a 3.5
ax.axhspan(2.5, 3.5, alpha=0.3, color='yellow', label='Moderado (2.5-3.5)')
# Verde suave: 3.51 a 5.0
ax.axhspan(3.51, 5.0, alpha=0.3, color='green', label='Alto (3.51-5.0)')

# Configurar posiciones de las barras
x = np.arange(len(participantes))
width = 0.35

# Preparar datos para PRE y POST
pre_scores = []
post_scores = []

for participante in participantes:
    pre_score = pre_data[pre_data['Participante'] == participante]['Puntaje_global'].iloc[0]
    post_score = post_data[post_data['Participante'] == participante]['Puntaje_global'].iloc[0]
    
    pre_scores.append(pre_score)
    post_scores.append(post_score)

# Crear las barras
bars1 = ax.bar(x - width/2, pre_scores, width, label='PRE', color='darkgrey', edgecolor='dimgray', alpha=1.0, linewidth=1)
bars2 = ax.bar(x + width/2, post_scores, width, label='POST', color='dimgray', edgecolor='dimgrey', alpha=1.0, linewidth=1)

# Configurar el eje X
ax.set_xlabel('Participantes', fontsize=14, fontweight='bold', labelpad=15)
ax.set_ylabel('Puntaje global EAC', fontsize=14, fontweight='bold', labelpad=15)
ax.set_title('Puntajes globales individuales - PRE vs POST', fontsize=16, fontweight='bold', pad=20)

# Configurar las etiquetas del eje X
ax.set_xticks(x)
ax.set_xticklabels(participantes)

# Configurar el eje Y con separación de 0.5
ax.set_ylim(0.8, 5.3)
ax.set_yticks(np.arange(1.0, 5.5, 0.5))
#ax.grid(axis='y', alpha=0.3, linestyle='--')

# Configurar el tamaño de las etiquetas de los ejes
ax.tick_params(axis='both', which='major', labelsize=12)

# Agregar valores en las barras
def add_value_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=11, fontweight='bold')

add_value_labels(bars1)
add_value_labels(bars2)

# Configurar la leyenda
from matplotlib.patches import Patch

# Crear elementos de leyenda personalizados
legend_elements = [
    Patch(facecolor='darkgrey', alpha=1.0, edgecolor='dimgray', label='PRE'),
    Patch(facecolor='dimgray', alpha=1.0, edgecolor='dimgrey', label='POST'),
    Patch(facecolor='red', alpha=0.3, edgecolor='darkred', label='Bajo (1.0-2.49)'),
    Patch(facecolor='yellow', alpha=0.3, edgecolor='olive', label='Moderado (2.5-3.5)'),
    Patch(facecolor='green', alpha=0.3, edgecolor='darkgreen', label='Alto (3.51-5.0)')
]

ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 1), fontsize=11)

# Ajustar el layout para evitar que se corten las etiquetas
plt.tight_layout()

# Guardar el gráfico
plt.savefig('puntajes_globales_individuales.png', dpi=300, bbox_inches='tight')

print("Gráfico generado exitosamente: puntajes_globales_individuales.png")
