import os
import matplotlib.pyplot as plt
from procesar_metricas import process_all_files

# Labels for plotting
METRIC_LABELS = {
    "collider_entries": "Entradasc collider",
    "sound_decrements": "Decrementos sonido",
    "flower_openings": "Aperturas flor",
    "time_in_collider": "Tiempo en collider (s)",
    "time_stationary": "Tiempo inmovil (s)",
    "time_flower_open": "Tiempo flor abierta (s)"
}

def ensure_output_dir():
    """Create and return the output directory for individual charts"""
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graficos_individuales')
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def plot_person_comparison(person, phases, output_dir):
    """Generate a comparison chart for one person's metrics between phases"""
    metrics = [
        "flower_openings",
        "time_flower_open",
        "collider_entries",
        "time_in_collider",
        "sound_decrements",
        "time_stationary",
    ]
    labels = [METRIC_LABELS[m] for m in metrics]
    fase1 = [phases.get("Fase1", {}).get(m, 0) for m in metrics]
    fase2 = [phases.get("Fase2", {}).get(m, 0) for m in metrics]
    
    x = range(len(metrics))
    width = 0.35
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create bars
    bars1 = ax.bar([i - width/2 for i in x], fase1, width, label="Fase 1", alpha=0.8)
    bars2 = ax.bar([i + width/2 for i in x], fase2, width, label="Fase 2", alpha=0.8)
    
    # Add value labels on top of each bar
    def add_value_labels(bars, values):
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.01,
                    f'{value:.1f}', ha='center', va='bottom', fontsize=9)
    
    add_value_labels(bars1, fase1)
    add_value_labels(bars2, fase2)
    
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=20, ha='right')
    ax.set_xlabel("Metricas", fontweight='bold', labelpad=10)
    ax.set_ylabel("Valor", fontweight='bold', labelpad=15)
    ax.set_title(f"Comparacion de metricas: {person.capitalize()}", fontweight='bold')
    ax.legend()
    #ax.grid(axis='y', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    
    # Save figure
    safe_person_name = person.replace(' ', '_')
    filename = f'{safe_person_name}_individual.png'
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    plt.close(fig)
    #print(f'Grafico guardado: {filepath}')

def generate_all_graphs():
    """Generate comparison graphs for all persons"""
    # Import data from the processing script
    person_results = process_all_files()
    
    print("Generando graficos individuales...")
    
    # Create output directory
    output_dir = ensure_output_dir()
    
    for person, phases in person_results.items():
        #print(f"Generando grafico para: {person.capitalize()}")
        plot_person_comparison(person, phases, output_dir)

def main():
    """Main function to generate all individual graphs"""
    try:
        generate_all_graphs()
        output_dir = ensure_output_dir()
        print(f"¡Todos los graficos han sido generados en {output_dir}!")
    except Exception as e:
        print(f"Error al generar los graficos: {e}")

if __name__ == "__main__":
    main() 