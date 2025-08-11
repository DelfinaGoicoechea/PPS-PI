import os
import csv
import statistics
from collections import defaultdict
from procesar_metricas import process_all_files, METRICS

def calculate_descriptive_stats(values):
    """
    Calculate descriptive statistics for a list of numeric values.
    Returns a dictionary with mean, std_dev, min, max.
    """
    if not values:
        return {"mean": 0, "std_dev": 0, "min": 0, "max": 0}
    
    try:
        return {
            "mean": statistics.mean(values),
            "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
            "min": min(values),
            "max": max(values)
        }
    except statistics.StatisticsError:
        return {"mean": 0, "std_dev": 0, "min": 0, "max": 0}

def collect_metric_values_by_phase(person_results):
    """
    Collect all values for each metric in each phase across all participants.
    Returns: {phase: {metric: [values]}}
    """
    metric_values = defaultdict(lambda: defaultdict(list))
    
    # Get all metric keys from METRICS
    metric_keys = list(METRICS.keys())
    
    for person, phases in person_results.items():
        for phase, summary in phases.items():
            for metric_key in metric_keys:
                if metric_key in summary:
                    metric_values[phase][metric_key].append(summary[metric_key])
    
    return metric_values

def generate_descriptive_analysis():
    """
    Generate descriptive analysis for all metrics across all phases.
    Returns a list of dictionaries with the analysis results.
    """
    # Process all files to get the data
    person_results = process_all_files()
    
    # Collect values by phase and metric
    metric_values = collect_metric_values_by_phase(person_results)
    
    # Calculate descriptive statistics
    analysis_results = []
    
    for phase in sorted(metric_values.keys()):
        for metric_key in sorted(metric_values[phase].keys()):
            values = metric_values[phase][metric_key]
            stats = calculate_descriptive_stats(values)
            
            # Get the Spanish name for the metric
            metric_name = METRICS[metric_key]
            
            result = {
                "Fase": phase,
                "Metrica": metric_name,
                "Metrica_Key": metric_key,
                "N_Participantes": len(values),
                "Media": round(stats["mean"], 2),
                "Desv_Estandar": round(stats["std_dev"], 2),
                "Minimo": stats["min"],
                "Maximo": stats["max"]
            }
            analysis_results.append(result)
    
    return analysis_results

def save_to_csv(analysis_results, filename="analisis_descriptivo.csv"):
    """
    Save the descriptive analysis results to a CSV file.
    """
    if not analysis_results:
        print("No hay datos para guardar.")
        return
    
    # Get the script directory for saving the file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    fieldnames = [
        "Fase", "Metrica", "Metrica_Key", "N_Participantes", 
        "Media", "Desv_Estandar", "Minimo", "Maximo"
    ]
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(analysis_results)
    
    print(f"Analisis descriptivo guardado en: {filepath}")

def print_summary_table(analysis_results):
    """
    Print a formatted summary table of the descriptive analysis.
    """
    if not analysis_results:
        print("No hay datos para mostrar.")
        return
    
    print("\n" + "="*100)
    print("ANALISIS DESCRIPTIVO DE METRICAS")
    print("="*100)
    
    # Group by phase for better readability
    phases = sorted(set(result["Fase"] for result in analysis_results))
    
    for phase in phases:
        print(f"\n{phase.upper()}")
        print("-" * 80)
        print(f"{'Metrica':<35} {'N':<3} {'Media':<8} {'Desv.Est':<8} {'Min':<6} {'Max':<6}")
        print("-" * 80)
        
        phase_results = [r for r in analysis_results if r["Fase"] == phase]
        for result in phase_results:
            print(f"{result['Metrica']:<35} {result['N_Participantes']:<3} "
                  f"{result['Media']:<8.2f} {result['Desv_Estandar']:<8.2f} "
                  f"{result['Minimo']:<6.1f} {result['Maximo']:<6.1f}")
    
    print("\n" + "="*100)

def main():
    """
    Main function to run the descriptive analysis.
    """
    try:
        print("Generando analisis descriptivo...")
        
        # Generate the analysis
        analysis_results = generate_descriptive_analysis()
        
        if not analysis_results:
            print("No se encontraron datos para analizar.")
            return
        
        # Print summary table
        print_summary_table(analysis_results)
        
        # Save to CSV
        save_to_csv(analysis_results)
        
        print(f"\n¡Analisis completado! Se procesaron {len(analysis_results)} metricas.")
        
    except Exception as e:
        print(f"Error durante el analisis: {e}")

if __name__ == "__main__":
    main()
