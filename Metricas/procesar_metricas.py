import os
import json
import re
from collections import defaultdict

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
    
    # General strategy functions that can be parameterized
    def count_non_empty(values):
        """Count non-empty values"""
        return sum(1 for v in values if v.strip())
    
    def count_containing_text(values, text):
        """Count values containing specific text"""
        return sum(1 for v in values if text in v)
    
    def sum_parsed_times(values):
        """Sum time durations from metric strings"""
        return sum(parse_seconds_from_string(v) for v in values if v.strip())
    
    # Strategy dictionary with parameterized strategies
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
    return filename.split('_')[0].lower()

def process_all_files():
    """Process all JSON files and return results organized by person and phase"""
    # person_results[person][phase] = summary
    person_results = defaultdict(dict)
    
    for idx, directory in enumerate(directories, 1):
        phase = f"Fase{idx}"
        # Extract just the directory name for the person name extraction
        dir_name = os.path.basename(directory)
        for filename in os.listdir(directory):
            if filename.endswith('.json'):
                person = get_person_name(filename)
                filepath = os.path.join(directory, filename)
                summary = process_file(filepath)
                person_results[person][phase] = summary
    
    return person_results

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

if __name__ == "__main__":
    # Process all files
    person_results = process_all_files()
    
    # Print summary
    print_summary(person_results) 