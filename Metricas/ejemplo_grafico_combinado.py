"""
Ejemplo de uso del gráfico combinado para comparar múltiples métricas.
Este script muestra cómo crear un gráfico que compare varias métricas entre fases.
"""

import matplotlib.pyplot as plt
import numpy as np
from analisis_descriptivo import generate_descriptive_analysis

def create_combined_chart_demo(analysis_results, metrics_to_show=None):
    """
    Create a combined chart showing multiple metrics side by side for demonstration.
    This is for display only, not saving.
    """
    if not metrics_to_show:
        # Get all unique metrics
        metrics_to_show = list(set(r['Metrica_Key'] for r in analysis_results))
    
    # Filter results for selected metrics
    filtered_results = [r for r in analysis_results if r['Metrica_Key'] in metrics_to_show]
    
    if not filtered_results:
        print("No data found for the specified metrics.")
        return
    
    # Get phases
    phases = sorted(set(r['Fase'] for r in filtered_results))
    
    # Create the figure
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Set up the bar positions
    n_metrics = len(metrics_to_show)
    n_phases = len(phases)
    x_pos = np.arange(n_metrics)
    bar_width = 0.35
    
    # Colors for phases
    colors = ['#2E86AB', '#A23B72']
    
    # Create bars for each phase
    for i, phase in enumerate(phases):
        phase_means = []
        phase_std_devs = []
        
        for metric_key in metrics_to_show:
            # Find the result for this metric and phase
            result = next((r for r in filtered_results 
                          if r['Metrica_Key'] == metric_key and r['Fase'] == phase), None)
            
            if result:
                phase_means.append(result['Media'])
                phase_std_devs.append(result['Desv_Estandar'])
            else:
                phase_means.append(0)
                phase_std_devs.append(0)
        
        # Create bars for this phase
        bars = ax.bar(x_pos + i * bar_width, phase_means, bar_width,
                      yerr=phase_std_devs, capsize=5,
                      alpha=0.8, color=colors[i], label=phase)
        
        # Add value labels
        for j, (bar, mean_val) in enumerate(zip(bars, phase_means)):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + phase_std_devs[j] + max(phase_means)*0.02,
                   f'{mean_val:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # Customize the chart
    ax.set_xlabel('Métricas', fontsize=12, fontweight='bold')
    ax.set_ylabel('Valor Promedio', fontsize=12, fontweight='bold')
    ax.set_title('Comparación de Métricas entre Fases', fontsize=14, fontweight='bold', pad=20)
    
    # Set x-axis labels (metric names)
    metric_names = [next(r['Metrica'] for r in filtered_results if r['Metrica_Key'] == mk) 
                   for mk in metrics_to_show]
    ax.set_xticks(x_pos + bar_width / 2)
    ax.set_xticklabels(metric_names, rotation=45, ha='right', fontsize=10)
    
    # Add legend
    ax.legend(fontsize=11)
    
    # Add grid
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    # Adjust layout
    plt.tight_layout()
    
    # Show the plot (not save)
    plt.show()

def main():
    """
    Ejemplo de cómo crear un gráfico combinado para métricas específicas.
    """
    print("Generando gráfico combinado de ejemplo...")
    
    # Obtener los resultados del análisis descriptivo
    analysis_results = generate_descriptive_analysis()
    
    # Ejemplo 1: Gráfico combinado con todas las métricas
    print("\n1. Gráfico combinado con todas las métricas:")
    create_combined_chart_demo(analysis_results)
    
    # Ejemplo 2: Gráfico combinado solo con métricas específicas
    print("\n2. Gráfico combinado con métricas específicas:")
    metrics_to_show = ['collider_entries', 'sound_decrements', 'flower_openings']
    create_combined_chart_demo(analysis_results, metrics_to_show)
    
    print("\n¡Ejemplos completados!")

if __name__ == "__main__":
    main()
