import os
import matplotlib.pyplot as plt
import numpy as np
from procesar_metricas import process_all_files, METRICS

def ensure_output_dir():
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graficos_grupo')
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def get_grouped_data(person_results, metric_key):
    """
    Returns:
        participants: list of participant names
        phases: list of phase names
        values: dict {phase: [value for each participant in order]}
    """
    # Get all participants and phases
    participants = sorted(person_results.keys())
    all_phases = set()
    for phases in person_results.values():
        all_phases.update(phases.keys())
    phases = sorted(all_phases)

    # Build values dict
    values = {phase: [] for phase in phases}
    for participant in participants:
        for phase in phases:
            val = person_results[participant].get(phase, {}).get(metric_key, 0)
            values[phase].append(val)
    return participants, phases, values

def plot_grouped_bar_chart(participants, phases, values, metric_name, metric_key, output_dir):
    x = np.arange(len(participants))
    width = 0.8 / len(phases)  # total width for all bars per group
    colors = plt.colormaps['tab10']

    fig, ax = plt.subplots(figsize=(max(8, len(participants)*1.2), 6))

    for i, phase in enumerate(phases):
        bar = ax.bar(x + i*width - (width*(len(phases)-1)/2), values[phase], width,
                     label=phase, color=colors(i))
        # Add value labels
        for rect, val in zip(bar, values[phase]):
            ax.text(rect.get_x() + rect.get_width()/2, rect.get_height() + max(values[phase])*0.02,
                    f'{val:.2f}', ha='center', va='bottom', fontsize=9)

    ax.set_xlabel('Participante', fontsize=12, fontweight='bold')
    ax.set_ylabel('Valor', fontsize=12, fontweight='bold')
    ax.set_title(f'Comparación por Participante: {metric_name}', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(participants, rotation=30, ha='right', fontsize=11)
    ax.legend(title='Fase')
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()

    # Save figure
    safe_metric_name = metric_key.replace(' ', '_')
    filename = f'{safe_metric_name}_grupo.png'
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, bbox_inches='tight')
    plt.close(fig)
    print(f'Gráfico guardado: {filepath}')

def main():
    print('Generando gráficos de barras agrupadas por participante...')
    output_dir = ensure_output_dir()
    person_results = process_all_files()
    for metric_key, metric_name in METRICS.items():
        participants, phases, values = get_grouped_data(person_results, metric_key)
        plot_grouped_bar_chart(participants, phases, values, metric_name, metric_key, output_dir)
    print(f'¡Todos los gráficos han sido generados en {output_dir}!')

if __name__ == '__main__':
    main()
