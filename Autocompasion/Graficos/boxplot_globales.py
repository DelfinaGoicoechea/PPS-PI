import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configurar el estilo de matplotlib para mejor visualización
plt.rcParams['font.size'] = 10
plt.rcParams['figure.figsize'] = (10, 8)

# Leer el archivo CSV con los promedios ya calculados
df = pd.read_csv('../Datos_autocompasion/Resultados/Datos_fase2_promedios.csv')

# Extraer los puntajes globales para PRE y POST
puntajes_pre = df[df['Fase'] == 'FASE 2 PRE']['Media_Global'].tolist()
puntajes_post = df[df['Fase'] == 'FASE 2 POST']['Media_Global'].tolist()

# Configurar el gráfico
fig, ax = plt.subplots(figsize=(10, 8))

# Crear el boxplot
box_data = [puntajes_pre, puntajes_post]
box_colors = ['skyblue', 'lightcoral']
box_labels = ['PRE', 'POST']

# Crear el boxplot
bp = ax.boxplot(box_data, tick_labels=box_labels, patch_artist=True, 
                boxprops=dict(facecolor='white', alpha=0.8),
                medianprops=dict(color='black', linewidth=2),
                flierprops=dict(marker='o', markerfacecolor='red', markersize=8))

# Colorear las cajas
for patch, color in zip(bp['boxes'], box_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

# Configurar el eje Y
ax.set_ylabel('Puntaje global EAC', fontsize=14, fontweight='bold', labelpad=15)
ax.set_title('Puntajes Globales de Autocompasión - Fase 2: PRE vs POST', 
             fontsize=16, fontweight='bold', pad=20)

# Configurar el eje X
ax.set_xlabel('Etapa', fontsize=14, fontweight='bold', labelpad=15)

# Configurar el tamaño de las etiquetas de los ejes
ax.tick_params(axis='both', which='major', labelsize=12)

# Agregar grid
ax.grid(axis='y', alpha=0.3, linestyle='--')

# Agregar estadísticas descriptivas como texto
stats_text = f"""
PRE:  Mediana={np.median(puntajes_pre):.2f}
POST: Mediana={np.median(puntajes_post):.2f}
"""
ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

# Ajustar el layout
plt.tight_layout()

# Guardar el gráfico
plt.savefig('boxplot_globales_fase2.png', dpi=300, bbox_inches='tight')

print("Boxplot generado exitosamente: boxplot_globales_fase2.png")