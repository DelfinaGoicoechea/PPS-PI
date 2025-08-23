import os
import csv
import json
import re
from collections import defaultdict
from anonimizador import anonymize_name, save_mapping

# Directories to process
# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
directories = [os.path.join(script_dir, "Fase1"), os.path.join(script_dir, "Fase2")]

METRICS = {
    "collider_entries": "Metrica Entradas Collider Gorrion",
    "sound_decrements": "Metrica Decremento Sonido",
    "flower_openings": "Metrica Apertura Flor",
    "time_in_collider": "Metrica Tiempo en Collider Gorrion",
    "time_stationary": "Metrica Duracion Inmovilidad",
    "time_flower_open": "Metrica Duracion Flor Abierta"
}

def parse_seconds_from_string(s):
    match = re.search(r"Duracion: ([\d,.]+) segundos", s)
    if match:
        return float(match.group(1).replace(",", "."))
    return 0.0

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    summary = {
        "collider_entries": 0,
        "sound_decrements": 0,
        "flower_openings": 0,
        "time_in_collider": 0.0,
        "time_stationary": 0.0,
        "time_flower_open": 0.0
    }
    
    def count_non_empty(values):
        """Count non-empty values"""
        return sum(1 for v in values if v.strip())
    
    def count_containing_text(values, text):
        """Count values containing specific text"""
        return sum(1 for v in values if text in v)
    
    def sum_parsed_times(values):
        """Sum time durations from metric strings"""
        return sum(parse_seconds_from_string(v) for v in values if v.strip())
    
    metric_handlers = {
        METRICS["collider_entries"]: ("collider_entries", count_non_empty),
        METRICS["sound_decrements"]: ("sound_decrements", count_non_empty),
        METRICS["flower_openings"]: ("flower_openings", lambda values: count_containing_text(values, "Flor abierta")),
        METRICS["time_in_collider"]: ("time_in_collider", sum_parsed_times),
        METRICS["time_stationary"]: ("time_stationary", sum_parsed_times),
        METRICS["time_flower_open"]: ("time_flower_open", sum_parsed_times)
    }
    
    exercises = data.get("ejercicios", [])
    for exercise in exercises:
        metrics = exercise.get("metricas", [])
        for metric in metrics:
            name = metric.get("nombre", "")
            values = metric.get("data", [])
            
            if name in metric_handlers:
                key, handler = metric_handlers[name]
                summary[key] += handler(values)
    
    return summary

def get_person_name(filename):
    # Extracts the name from the filename, e.g., Hugo_1.json -> hugo
    real_name = filename.split('_')[0].upper()
    return anonymize_name(real_name)

def process_all_files():
    """Process all JSON files and return results organized by person and phase"""
    # person_results[person][phase] = summary
    person_results = defaultdict(dict)
    
    for idx, directory in enumerate(directories, 1):
        phase = f"Fase{idx}"
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                person = get_person_name(filename)
                filepath = os.path.join(directory, filename)
                summary = process_file(filepath)
                person_results[person][phase] = summary
    
    return person_results

def save_to_csv(person_results, filename="datos_procesados.csv"):
    """
    Save the processed results to a CSV file.
    """
    if not person_results:
        print("No hay datos para guardar.")
        return
    
    # Get the script directory for saving the file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    
    # Define the fieldnames for the CSV
    fieldnames = [
        "Participante", "Fase", "Entradas_Collider", "Decrementos_Sonido", 
        "Aperturas_Flor", "Tiempo_Collider", "Tiempo_Inmovil", "Tiempo_Flor_Abierta"
    ]
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for person, phases in person_results.items():
            for phase in ["Fase1", "Fase2"]:
                if phase in phases:
                    summary = phases[phase]
                    row = {
                        "Participante": person.capitalize(),
                        "Fase": phase,
                        "Entradas_Collider": summary['collider_entries'],
                        "Decrementos_Sonido": summary['sound_decrements'],
                        "Aperturas_Flor": summary['flower_openings'],
                        "Tiempo_Collider": round(summary['time_in_collider'], 2),
                        "Tiempo_Inmovil": round(summary['time_stationary'], 2),
                        "Tiempo_Flor_Abierta": round(summary['time_flower_open'], 2)
                    }
                    writer.writerow(row)
    
    print(f"Datos procesados guardados en: {filepath}")

def print_summary(person_results):
    """Print a summary of results for each person"""
    for person, phases in person_results.items():
        print(f"\nPersona: {person.capitalize()}")
        for phase in ["Fase1", "Fase2"]:
            if phase in phases:
                summary = phases[phase]
                print(f"  {phase}:")
                print(f"    Entradas Collider: {summary['collider_entries']}")
                print(f"    Decrementos Sonido: {summary['sound_decrements']}")
                print(f"    Aperturas Flor: {summary['flower_openings']}")
                print(f"    Tiempo en Collider: {summary['time_in_collider']:.1f}s")
                print(f"    Tiempo Inmovil: {summary['time_stationary']:.1f}s")
                print(f"    Tiempo Flor Abierta: {summary['time_flower_open']:.1f}s")
            else:
                print(f"  {phase}: No data")

def main():
    # Process all files
    person_results = process_all_files()
    
    # Print summary
    print_summary(person_results)
    
    # Save to CSV
    save_to_csv(person_results)

    # Guardar el mapa real → alias en la carpeta Metricas/
    save_mapping()

if __name__ == "__main__":
     main()