import csv
import os

ANONYMIZED_MAP = {}
_counter = 1

script_dir = os.path.dirname(os.path.abspath(__file__))
mapping_file = os.path.join(script_dir, "mapa_participantes.csv")

def _load_existing_mapping():
    """Carga el mapa de participantes existente si ya hay un archivo"""
    global ANONYMIZED_MAP, _counter
    if os.path.exists(mapping_file):
        with open(mapping_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row["Nombre_Real"].strip().upper()
                ANONYMIZED_MAP[name] = row["Alias"]

        # Ajustar el contador al último número usado
        if ANONYMIZED_MAP:
            max_num = max(int(alias.replace("Part", "")) for alias in ANONYMIZED_MAP.values())
            _counter = max_num + 1

# Cargar el mapa existente apenas se importa el modulo
_load_existing_mapping()

def anonymize_name(real_name):
    """Devuelve un alias (Part_1, Part_2, ...) para un participante real (case-insensitive)"""
    global _counter
    name = real_name.strip().upper()
    if name not in ANONYMIZED_MAP:
        ANONYMIZED_MAP[name] = f"Part{_counter}"
        _counter += 1
    return ANONYMIZED_MAP[name]

def save_mapping():
    """Guarda o actualiza el mapa real->alias en un CSV"""
    with open(mapping_file, "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Nombre_Real", "Alias"])
        for real, alias in ANONYMIZED_MAP.items():
            writer.writerow([real, alias])

    print(f"Mapa de participantes actualizado en: {mapping_file}")
