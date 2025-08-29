import os
import re
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from procesar_subescalas import process_experience_data, select_csv_file
from analisis_subescalas import calcular_estadisticas_por_fase, _prepare_dataframe

# Etiquetas de subescalas (deben coincidir con las del script procesar_subescalas.py)
SUBSCALES = [
    'Auto-amabilidad',
    'Humanidad_comun',
    'Mindfulness',
    'Auto-juicio',
    'Aislamiento',
    'Sobre-identificacion'
]

def ensure_output_dir(filename=None):
    """Crear y devolver el directorio de salida para los gráficos de autocompasión"""
    base_output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graficos_autocompasion')
    os.makedirs(base_output_dir, exist_ok=True)
    
    if filename:
        # Crear subdirectorio con el nombre del archivo (sin extensión)
        file_name_without_ext = os.path.splitext(os.path.basename(filename))[0]
        output_dir = os.path.join(base_output_dir, file_name_without_ext)
        os.makedirs(output_dir, exist_ok=True)
        return output_dir
    else:
        return base_output_dir

def plot_individual_overall_scores(df, output_dir):
    """
    Gráfico de puntajes globales individuales:
    x-axis: participantes
    y-axis: overall EAC score
    one bar for pre and one for post
    """
    # Filtrar solo datos PRE y POST
    df_filtered = df[df['Fase'].str.contains('PRE|POST', flags=re.IGNORECASE, na=False)].copy()
    
    # Extraer información de fase y etapa
    df_filtered['Fase_Numero'] = df_filtered['Fase'].str.extract(r'FASE (\d+)').astype(int)
    df_filtered['Etapa'] = df_filtered['Fase'].str.extract(r'(PRE|POST)', flags=re.IGNORECASE)
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Obtener participantes únicos
    participants = sorted(df_filtered['Participante'].unique())
    x = np.arange(len(participants))
    width = 0.35
    
    # Preparar datos para PRE y POST
    pre_scores = []
    post_scores = []
    
    for participant in participants:
        pre_data = df_filtered[(df_filtered['Participante'] == participant) & 
                              (df_filtered['Etapa'] == 'PRE')]
        post_data = df_filtered[(df_filtered['Participante'] == participant) & 
                               (df_filtered['Etapa'] == 'POST')]
        
        pre_score = pre_data['Media_Global'].mean() if not pre_data.empty else 0
        post_score = post_data['Media_Global'].mean() if not post_data.empty else 0
        
        pre_scores.append(pre_score)
        post_scores.append(post_score)
    
    # Crear barras
    bars1 = ax.bar(x - width/2, pre_scores, width, label='PRE', alpha=0.8, color='skyblue')
    bars2 = ax.bar(x + width/2, post_scores, width, label='POST', alpha=0.8, color='lightcoral')
    
    # Añadir valores en las barras
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                        f'{height:.2f}', ha='center', va='bottom', fontsize=9)
    
    ax.set_xlabel('Participantes', fontweight='bold')
    ax.set_ylabel('Puntaje Global EAC', fontweight='bold')
    ax.set_title('Puntajes Globales Individuales - PRE vs POST', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(participants)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    
    # Guardar figura
    filepath = os.path.join(output_dir, 'puntajes_globales_individuales.png')
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f'Gráfico guardado: {filepath}')

def plot_group_averages_subscales(df, output_dir):
    """
    Gráfico de promedios grupales de subescalas:
    x-axis: subescalas
    y-axis: group average
    one bar for pre and one for post
    """
    # Preparar datos usando la función de análisis_subescalas
    df_prepared = _prepare_dataframe(df)
    medias, desvios = calcular_estadisticas_por_fase(df_prepared)
    
    # Filtrar solo medias (no desviaciones)
    medias_only = medias[medias['Medida'] == 'Media'].copy()
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(14, 8))
    
    x = np.arange(len(SUBSCALES))
    width = 0.35
    
    # Preparar datos para PRE y POST
    pre_means = []
    post_means = []
    
    for subscale in SUBSCALES:
        pre_data = medias_only[medias_only['Fase'].str.contains('PRE', flags=re.IGNORECASE)]
        post_data = medias_only[medias_only['Fase'].str.contains('POST', flags=re.IGNORECASE)]
        
        pre_mean = pre_data[subscale].mean() if not pre_data.empty else 0
        post_mean = post_data[subscale].mean() if not post_data.empty else 0
        
        pre_means.append(pre_mean)
        post_means.append(post_mean)
    
    # Crear barras
    bars1 = ax.bar(x - width/2, pre_means, width, label='PRE', alpha=0.8, color='skyblue')
    bars2 = ax.bar(x + width/2, post_means, width, label='POST', alpha=0.8, color='lightcoral')
    
    # Añadir valores en las barras
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                        f'{height:.2f}', ha='center', va='bottom', fontsize=9)
    
    ax.set_xlabel('Subescalas', fontweight='bold')
    ax.set_ylabel('Promedio Grupal', fontweight='bold')
    ax.set_title('Promedios Grupales de Subescalas - PRE vs POST', fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(SUBSCALES, rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    
    # Guardar figura
    filepath = os.path.join(output_dir, 'promedios_grupales_subescalas.png')
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f'Gráfico guardado: {filepath}')

def plot_boxplot_overall_scores(df, output_dir):
    """
    Boxplot de puntajes globales:
    two boxes (one for PRE and one for POST)
    """
    # Filtrar solo datos PRE y POST
    df_filtered = df[df['Fase'].str.contains('PRE|POST', flags=re.IGNORECASE, na=False)].copy()
    
    # Extraer información de etapa y fase
    df_filtered['Etapa'] = df_filtered['Fase'].str.extract(r'(PRE|POST)', flags=re.IGNORECASE)
    
    # Extraer el número de fase
    #######fase_numbers = df_filtered['Fase'].str.extract(r'(\d+)').dropna()
    '''
    if not fase_numbers.empty:
        fase_num = str(fase_numbers.iloc[0])
    else:
        fase_num = "X"
    '''
    # Preparar datos para boxplot
    pre_scores = df_filtered[df_filtered['Etapa'] == 'PRE']['Media_Global'].dropna()
    post_scores = df_filtered[df_filtered['Etapa'] == 'POST']['Media_Global'].dropna()
    
    # Crear figura
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Crear boxplot
    data = [pre_scores, post_scores]
    labels = ['PRE', 'POST']
    colors = ['skyblue', 'lightcoral']
    
    bp = ax.boxplot(data, tick_labels=labels, patch_artist=True)
    
    # Colorear las cajas
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    ax.set_ylabel('Puntaje Global EAC', fontweight='bold')
    ax.set_title(f'Distribución de Puntajes Globales - Fase ', fontweight='bold')
    ax.grid(axis='y', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    
    # Guardar figura
    filepath = os.path.join(output_dir, 'boxplot_puntajes_globales.png')
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f'Gráfico guardado: {filepath}')

def plot_autocompasion_person(participant, phases_data, global_data, output_dir):
    """
    Generar grafico comparativo de subescalas para un participante en distintas fases,
    mostrando tambien su media global.
    """
    fases = list(phases_data.keys())
    num_fases = len(fases)
    x = range(len(SUBSCALES))
    width = 0.8 / num_fases  # ancho dinamico segun cantidad de fases
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Graficar cada fase
    for i, fase in enumerate(fases):
        valores = [phases_data[fase].get(s, 0) for s in SUBSCALES]
        bars = ax.bar([j - 0.4 + i*width + width/2 for j in x], valores, width, label=fase, alpha=0.8)
        
        # Etiquetas de valores
        for bar, value in zip(bars, valores):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                    f'{value:.2f}', ha='center', va='bottom', fontsize=8)
    
    ax.set_ylim(0, 5.2)
    ax.set_yticks([i/2 for i in range(0, 11)])
    ax.set_xticks(list(x))
    ax.set_xticklabels(SUBSCALES, rotation=20, ha='right')
    ax.set_xlabel("Subescalas", fontweight='bold')
    ax.set_ylabel("Valor EAC", fontweight='bold')
    ax.set_title(f"Autocompasión - {participant}", fontweight='bold')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    
    # Guardar figura
    safe_person_name = participant.replace(' ', '_')
    filename = f'{safe_person_name}_autocompasion.png'
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    plt.close(fig)
    print(f'Gráfico guardado: {filepath}')

def generate_all_graphs(csv_file):
    """Generar todos los gráficos de autocompasión"""
    # Procesar datos
    subscale_results, global_results = process_experience_data(csv_file)
    
    # Convertir a DataFrame para facilitar el procesamiento
    df = pd.DataFrame(subscale_results)
    
    # Crear directorio de salida con el nombre del archivo
    output_dir = ensure_output_dir(csv_file)
    
    # 1. Gráfico de puntajes globales individuales
    plot_individual_overall_scores(df, output_dir)
    
    # 2. Gráfico de promedios grupales de subescalas
    plot_group_averages_subscales(df, output_dir)
    
    # 3. Boxplot de puntajes globales
    plot_boxplot_overall_scores(df, output_dir)
    
    # 4. Gráficos individuales por participante (existente)
    # Reorganizar resultados por persona y fase
    participants = {}
    globals_participants = {}
    
    for row in subscale_results:
        p = row['Participante']
        f = row['Fase']
        participants.setdefault(p, {})[f] = {s: row[s] for s in SUBSCALES}
    
    for row in global_results:
        p = row['Participante']
        f = row['Fase']
        globals_participants.setdefault(p, {})[f] = row['Media_Global']
    
    for participant, phases_data in participants.items():
        global_data = globals_participants.get(participant, {})
        plot_autocompasion_person(participant, phases_data, global_data, output_dir)

def main():
    """Funcion principal para generar graficos"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, 'Datos_autocompasion')
        
        # Dejar que el usuario elija archivo (igual que en procesar_subescalas.py)
        selected_file = select_csv_file(data_dir)
        if not selected_file:
            print("No se selecciono ningun archivo. Saliendo...")
            return
        
        csv_file = os.path.join(data_dir, selected_file)
        print(f"\nGenerando graficos a partir de: {csv_file}")
        
        generate_all_graphs(csv_file)
        
        # Obtener el directorio de salida para el mensaje final
        output_dir = ensure_output_dir(csv_file)
        print(f"¡Todos los graficos han sido generados en {output_dir}!")
    
    except Exception as e:
        print(f"Error al generar los graficos: {e}")

if __name__ == "__main__":
    main()
