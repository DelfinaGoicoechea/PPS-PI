import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, ListedColormap, BoundaryNorm
import matplotlib.patches as mpatches

# Configurar el estilo de matplotlib para mejor visualización
plt.style.use('default')
sns.set_palette("husl")

def create_autocompasion_heatmap():
    """
    Crea un heatmap de autocompasión con colores discretos por rangos de valores.
    """
    
    # Leer los datos
    data_path = '../Datos_autocompasion/Resultados/Datos_fase2_promedios.csv'
    df = pd.read_csv(data_path)
    
    # Renombrar columnas para mejor visualización
    df = df.rename(columns={
        'Media_Global': 'Puntaje global',
    })
    
    # Extraer etapa PRE/POST y ordenar por participante y etapa (PRE primero)
    df['Etapa'] = df['Fase'].str.replace('FASE 2 ', '', regex=False)
    etapa_order = {'PRE': 0, 'POST': 1}
    df['Etapa_ord'] = df['Etapa'].map(etapa_order).fillna(9).astype(int)
    df = df.sort_values(['Participante', 'Etapa_ord'], kind='stable')
    
    # Crear etiqueta final para filas
    df['Participante_Fase'] = df['Participante'] + ' - ' + df['Etapa']
    
    # Seleccionar las columnas para el heatmap
    columns_to_plot = [
        'Auto-amabilidad', 'Humanidad_comun', 'Mindfulness', 
        'Auto-juicio', 'Aislamiento', 'Sobre-identificacion', 'Puntaje global'
    ]
    
    # Crear la matriz de datos para el heatmap (respetando el orden definido)
    heatmap_data = df.set_index('Participante_Fase')[columns_to_plot]
    
    # Colores discretos por rangos:
    # rojo (1.0-2.49), amarillo (2.5-3.5), verde (3.51-5.0)
    colors = ['#E06666', '#FFD966', '#93C47D']  # rojo, amarillo, verde (suaves)
    cmap = ListedColormap(colors)
    # Definir límites de los bins. El último límite se extiende un poco para incluir 5.0
    boundaries = [1.0, 2.5, 3.51, 5.01]
    norm = BoundaryNorm(boundaries, cmap.N)
    
    # Configurar la figura
    plt.figure(figsize=(14, 8))
    
    # Crear el heatmap con colores discretos
    ax = sns.heatmap(
        heatmap_data,
        annot=True,
        fmt='.2f',
        annot_kws={'size': 12},
        cmap=cmap,
        norm=norm,
        vmin=1.0,
        vmax=5.0,
        cbar=True,
        cbar_kws={'shrink': 0.6, 'aspect': 20},
        linewidths=0.5,
        linecolor='white',
        square=False,
        xticklabels=True,
        yticklabels=True
    )
    
    # Personalizar el colorbar (mostrar etiquetas de rangos)
    cbar = ax.collections[0].colorbar
    cbar.set_ticks([1.0, 2.5, 3.5, 5.0])
    cbar.set_ticklabels(['1.0', '2.5', '3.5', '5.0'])
    cbar.ax.tick_params(labelsize=12)
    cbar.ax.set_ylabel('Puntaje', fontsize=14, fontweight='bold', labelpad=10)
    
    # Configurar etiquetas y título
    plt.title('Heatmap de Autocompasión - Fase 2 (Pre y Post)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Subescalas', fontsize=14, fontweight='bold')
    plt.ylabel('Participantes', fontsize=14, fontweight='bold', labelpad=15)
    
    # Rotar etiquetas del eje X para mejor legibilidad
    plt.xticks(rotation=45, ha='right', fontsize=12)  # Tamaño de las etiquetas del eje X
    plt.yticks(rotation=0, fontsize=12)  # Tamaño de las etiquetas del eje Y
    
    # Ajustar el layout para evitar cortes y dar espacio al colorbar
    plt.subplots_adjust(right=0.85)
    
    # Crear leyenda personalizada
    legend_elements = [
        mpatches.Patch(color=colors[0], label='Bajo (1.0 - 2.49)'),
        mpatches.Patch(color=colors[1], label='Medio (2.5 - 3.5)'),
        mpatches.Patch(color=colors[2], label='Alto (3.51 - 5.0)')
    ]
    
    plt.legend(handles=legend_elements, 
              loc='upper right', 
              bbox_to_anchor=(1.30, 1.07),
              title='Nivel autocompasión',
              title_fontsize=14,
              fontsize=12)
    
    # Guardar el gráfico
    output_path = 'heatmap_autocompasion.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Heatmap guardado como: {output_path}")
    
    # Cerrar la figura para liberar memoria
    plt.close()
    
    return heatmap_data

if __name__ == "__main__":
    # Crear el heatmap
    heatmap_data = create_autocompasion_heatmap()
