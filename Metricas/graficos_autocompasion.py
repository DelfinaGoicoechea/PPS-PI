import os
import matplotlib.pyplot as plt
from procesar_subescalas import process_experience_data, select_csv_file

# Etiquetas de subescalas (deben coincidir con las del script procesar_subescalas.py)
SUBSCALES = [
    'Auto-amabilidad',
    'Humanidad_comun',
    'Mindfulness',
    'Auto-juicio',
    'Aislamiento',
    'Sobre-identificacion'
]

def ensure_output_dir():
    """Crear y devolver el directorio de salida para los gráficos de autocompasión"""
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graficos_autocompasion')
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def plot_autocompasion_person(participant, phases_data, global_data, output_dir):
    """
    Generar gráfico comparativo de subescalas para un participante en distintas fases,
    mostrando también su media global.
    """
    fases = sorted(phases_data.keys())
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
    
        # Media global de esa fase
        if fase in global_data and global_data[fase] > 0:
            media = global_data[fase]
            ax.axhline(media, color=bars[0].get_facecolor(), linestyle='--', linewidth=1.5,
                       label=f"{fase} - Media Global: {media:.2f}")
    
    ax.set_ylim(0, 5.2)
    ax.set_yticks([i/2 for i in range(0, 11)])
    ax.set_xticks(list(x))
    ax.set_xticklabels(SUBSCALES, rotation=20, ha='right')
    ax.set_xlabel("Subescalas", fontweight='bold')
    ax.set_ylabel("Valor", fontweight='bold')
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
    """Generar gráficos de autocompasión para todos los participantes"""
    subscale_results, global_results = process_experience_data(csv_file)
    
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
    
    output_dir = ensure_output_dir()
    
    for participant, phases_data in participants.items():
        global_data = globals_participants.get(participant, {})
        plot_autocompasion_person(participant, phases_data, global_data, output_dir)

def main():
    """Función principal para generar gráficos"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, 'Datos')
        
        # Dejar que el usuario elija archivo (igual que en procesar_subescalas.py)
        selected_file = select_csv_file(data_dir)
        if not selected_file:
            print("No se seleccionó ningún archivo. Saliendo...")
            return
        
        csv_file = os.path.join(data_dir, selected_file)
        print(f"\nGenerando gráficos a partir de: {csv_file}")
        
        generate_all_graphs(csv_file)
        
        output_dir = ensure_output_dir()
        print(f"¡Todos los gráficos han sido generados en {output_dir}!")
    
    except Exception as e:
        print(f"Error al generar los gráficos: {e}")

if __name__ == "__main__":
    main()
