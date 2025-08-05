import matplotlib.pyplot as plt
from procesar_metricas import process_all_files

# Labels for plotting
METRIC_LABELS = {
    "collider_entries": "Entradas Collider",
    "sound_decrements": "Decrementos Sonido",
    "flower_openings": "Aperturas Flor",
    "time_in_collider": "Tiempo en Collider (s)",
    "time_stationary": "Tiempo Inmóvil (s)",
    "time_flower_open": "Tiempo Flor Abierta (s)"
}

def plot_person_comparison(person, phases):
    """Generate a comparison chart for one person's metrics between phases"""
    metrics = list(METRIC_LABELS.keys())
    labels = [METRIC_LABELS[m] for m in metrics]
    fase1 = [phases.get("Fase1", {}).get(m, 0) for m in metrics]
    fase2 = [phases.get("Fase2", {}).get(m, 0) for m in metrics]
    
    x = range(len(metrics))
    width = 0.35
    
    plt.figure(figsize=(12, 6))
    
    # Create bars
    bars1 = plt.bar([i - width/2 for i in x], fase1, width, label="Fase 1", alpha=0.8)
    bars2 = plt.bar([i + width/2 for i in x], fase2, width, label="Fase 2", alpha=0.8)
    
    # Add value labels on top of each bar
    def add_value_labels(bars, values):
        for bar, value in zip(bars, values):
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + max(values)*0.01,
                    f'{value:.1f}', ha='center', va='bottom', fontsize=9)
    
    add_value_labels(bars1, fase1)
    add_value_labels(bars2, fase2)
    
    plt.xticks(x, labels, rotation=20, ha='right')
    plt.ylabel("Valor")
    plt.title(f"Comparación de métricas: {person.capitalize()}")
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

def generate_all_graphs():
    """Generate comparison graphs for all persons"""
    # Import data from the processing script
    person_results = process_all_files()
    
    print("Generando gráficos individuales...")
    
    for person, phases in person_results.items():
        print(f"Generando gráfico para: {person.capitalize()}")
        plot_person_comparison(person, phases)

def main():
    """Main function to generate all individual graphs"""
    try:
        generate_all_graphs()
        print("¡Todos los gráficos han sido generados!")
    except Exception as e:
        print(f"Error al generar los gráficos: {e}")

if __name__ == "__main__":
    main() 