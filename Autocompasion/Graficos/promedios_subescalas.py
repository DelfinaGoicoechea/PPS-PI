import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configurar el estilo de matplotlib para mejor visualización
plt.style.use('default')
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (12, 8)

# Leer el archivo CSV
df = pd.read_csv('../Datos_autocompasion/Resultados/Datos_fase2_analisis.csv')

# Filtrar solo las filas de Media
media_data = df[df['Medida'] == 'Media']

# Obtener datos pre y post
pre_data = media_data[media_data['Fase'] == '2 - PRE'].iloc[0]
post_data = media_data[media_data['Fase'] == '2 - POST'].iloc[0]

# Definir las subescalas (excluyendo Media_Global)
subescalas = ['Auto-amabilidad', 'Humanidad_comun', 'Mindfulness', 'Auto-juicio', 'Aislamiento', 'Sobre-identificacion']

# Obtener valores pre y post para cada subescala
valores_pre = [pre_data[sub] for sub in subescalas]
valores_post = [post_data[sub] for sub in subescalas]

# Configurar el gráfico
fig, ax = plt.subplots(figsize=(14, 8))

# Crear el fondo con colores según los rangos especificados
y_min, y_max = 1.0, 5.0
ax.set_ylim(y_min, y_max)

# Crear las regiones de color de fondo
# Rojo: 1.0 a 2.49
ax.axhspan(1.0, 2.49, alpha=0.4, color='red', label='Bajo (1.0-2.49)')
# Amarillo: 2.5 a 3.5
ax.axhspan(2.5, 3.5, alpha=0.4, color='yellow', label='Medio (2.5-3.5)')
# Verde: 3.51 a 5.0
ax.axhspan(3.51, 5.0, alpha=0.4, color='green', label='Alto (3.51-5.0)')

# Configurar posiciones de las barras
x = np.arange(len(subescalas))
width = 0.35

# Crear las barras
bars1 = ax.bar(x - width/2, valores_pre, width, label='PRE', color='tab:blue', alpha=1.0, edgecolor='darkblue', linewidth=1)
bars2 = ax.bar(x + width/2, valores_post, width, label='POST', color='navy', alpha=1.0, edgecolor='black', linewidth=1)

# Configurar el eje X
ax.set_xlabel('Subescalas', fontsize=14, fontweight='bold')
ax.set_ylabel('Valor promedio', fontsize=14, fontweight='bold', labelpad=15)
ax.set_title('Promedios de Subescalas - Fase 2: PRE vs POST', fontsize=16, fontweight='bold', pad=20)

# Configurar las etiquetas del eje X
ax.set_xticks(x)
ax.set_xticklabels(subescalas, rotation=45, ha='right')

# Configurar el eje Y
ax.set_ylim(0.8, 5.3)
ax.set_yticks(np.arange(1.0, 5.0, 0.5))
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Configurar el tamaño de las etiquetas de los ejes
ax.tick_params(axis='both', which='major', labelsize=13)  # Tamaño de las etiquetas de los ejes

# Agregar valores en las barras
def add_value_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=12, fontweight='bold')  # Aumentado de 9 a 12

add_value_labels(bars1)
add_value_labels(bars2)

# Configurar la leyenda
# Crear leyenda personalizada que combine las barras y los rangos de color
from matplotlib.patches import Patch

# Crear elementos de leyenda personalizados
legend_elements = [
    Patch(facecolor='tab:blue', alpha=1.0, edgecolor='navy', label='PRE'),
    Patch(facecolor='navy', alpha=1.0, edgecolor='black', label='POST'),
    Patch(facecolor='red', alpha=0.5, label='Bajo (1.0-2.49)'),
    Patch(facecolor='yellow', alpha=0.5, label='Medio (2.5-3.5)'),
    Patch(facecolor='green', alpha=0.5, label='Alto (3.51-5.0)')
]

ax.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1, 1), fontsize=12)

# Ajustar el layout para evitar que se corten las etiquetas
plt.tight_layout()

# Guardar el gráfico
plt.savefig('promedios_subescalas_fase2.png', dpi=300, bbox_inches='tight')

print("Gráfico generado exitosamente: promedios_subescalas_fase2.png")
