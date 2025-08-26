import os
import pandas as pd
from anonimizador import anonymize_name, save_mapping

# Define subescalas y sus preguntas correspondientes
SUBCALES = {
    'Auto-amabilidad': [5, 12, 19, 23, 26],
    'Humanidad_comun': [3, 7, 10, 15],
    'Mindfulness': [9, 14, 17, 22],
    'Auto-juicio': [1, 8, 11, 16, 21],
    'Aislamiento': [4, 13, 18, 25],
    'Sobre-identificacion': [2, 6, 20, 24]
}

# Preguntas que necesitan ser invertidas para subescalas negativas
INVERTED_QUESTIONS = [1, 2, 4, 6, 8, 11, 13, 16, 18, 20, 21, 24, 25]

# Subescalas negativas que requieren inversión de valores
NEGATIVE_SUBSCALES = ['Auto-juicio', 'Aislamiento', 'Sobre-identificacion']

def invert_value(value):
    """Invertir un valor: 1->5, 2->4, 3->3, 4->2, 5->1"""
    # No se deben poner valores en 0. Todas las preguntas se encuentran respondidas
    return 6 - value

def calculate_subscale_mean(data, questions, subscale_name):
    """Calcular la media para una subescala especifica, invirtiendo valores si es una subescala negativa"""
    values = []
    for q in questions:
        if q in data and data[q] != 0:  # Excluir valores faltantes (0)
            value = data[q]
            # Si es una subescala negativa, invertir los valores de las preguntas invertidas
            if subscale_name in NEGATIVE_SUBSCALES and q in INVERTED_QUESTIONS:
                value = invert_value(value)
            values.append(value)
    
    if not values:
        return 0.0
    return sum(values) / len(values)

def calculate_global_mean(subscale_means):
    """Calcular la media global promediando las medias de las seis subescalas"""
    # Las subescalas negativas ya tienen sus valores invertidos en calculate_subscale_mean
    values = list(subscale_means.values())
    
    if not values:
        return 0.0
    return sum(values) / len(values)

def process_experience_data(csv_file_path):
    """Procesar los datos de la experiencia CSV usando pandas"""
    
    # Leer el archivo CSV con pandas
    df = pd.read_csv(csv_file_path)
    
    # Almacenamiento de resultados
    subscale_results = []
    global_results = []
    
    # Procesar cada fila (cada fila representa una combinacion de participante-fase)
    for row in df.itertuples(index=False, name=None):
        # row es una tupla: (Participante, Fase, 1, 2, 3, ..., 26)
        real_participant = row[0]
        participant = anonymize_name(real_participant)
        phase_value = str(row[1]).strip()
        phase = f"FASE {phase_value}"
        
        # Extraer valores de preguntas para este participante-fase
        participant_data = {}
        for question in range(1, 27):
            value = row[question+1]
            if pd.notna(value):  # Verificar si el valor no es NaN
                participant_data[question] = int(value)
            else:
                participant_data[question] = 0
        
        # Calcular medias de subescalas
        subscale_means = {}
        for subscale_name, questions in SUBCALES.items():
            mean = calculate_subscale_mean(participant_data, questions, subscale_name)
            subscale_means[subscale_name] = round(mean, 2)
        
        # Calcular media global
        global_mean = round(calculate_global_mean(subscale_means), 2)
        
        # Almacenar resultados
        subscale_row = {
            'Participante': participant,
            'Fase': phase,
            **subscale_means,
            'Media_Global': global_mean
        }
        subscale_results.append(subscale_row)
    
    return subscale_results, global_results

def save_results(subscale_results, global_results, output_dir, input_filename):
    """Guardar resultados en archivos CSV usando pandas"""
    
    # Crear directorio de resultados dentro del directorio de datos
    results_dir = os.path.join(output_dir, 'Resultados')
    os.makedirs(results_dir, exist_ok=True)
    
    # Generar nombres de salida basados en el nombre de archivo de entrada
    base_name = os.path.splitext(input_filename)[0]  # Eliminar la extension .csv
    subscale_file = os.path.join(results_dir, f'{base_name}_promedios.csv')
    
    # Guardar resultados combinados (subescalas + Media_Global)
    if subscale_results:
        subscale_df = pd.DataFrame(subscale_results)
        subscale_df.to_csv(subscale_file, index=False, encoding='utf-8')
        print(f"Resultados combinados guardados en: {subscale_file}")

def list_available_files(data_dir):
    """Listar todos los archivos CSV en el directorio de datos (excluyendo el directorio de resultados)"""
    csv_files = []
    if os.path.exists(data_dir):
        for file in os.listdir(data_dir):
            if file.endswith('.csv'):
                csv_files.append(file)
    return sorted(csv_files)

def select_csv_file(data_dir):
    """Permitir al usuario seleccionar que archivo CSV procesar"""
    csv_files = list_available_files(data_dir)
    
    if not csv_files:
        print("No se encontraron archivos CSV en el directorio de datos.")
        return None
    
    print("\nArchivos CSV disponibles:")
    for i, file in enumerate(csv_files, 1):
        print(f"{i}. {file}")
    
    while True:
        try:
            choice = input(f"\nSeleccione un archivo (1-{len(csv_files)}) o 'q' para salir: ").strip()
            
            if choice.lower() == 'q':
                return None
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(csv_files):
                return csv_files[choice_num - 1]
            else:
                print(f"Por favor ingrese un numero entre 1 y {len(csv_files)}")
        except ValueError:
            print("Por favor ingrese un numero valido")

def main():
    """Funcion principal para procesar los datos de la experiencia"""
    try:
        # Definir rutas de archivos
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, 'Datos_autocompasion')
        
        # Permitir al usuario seleccionar el archivo CSV
        selected_file = select_csv_file(data_dir)
        if not selected_file:
            print("No se selecciono ningun archivo. Saliendo...")
            return
        
        csv_file = os.path.join(data_dir, selected_file)
        
        print(f"\nProcesando archivo: {selected_file}")
        
        # Procesar los datos
        subscale_results, global_results = process_experience_data(csv_file)
        
        # Guardar resultados
        save_results(subscale_results, global_results, data_dir, selected_file)

        # Guardar el mapa real -> alias en la carpeta Metricas/ 
        save_mapping()
        
        print(f"\n¡Procesamiento completado! Se procesaron {len(subscale_results)} registros.")
        
    except Exception as e:
        print(f"Error durante el procesamiento: {e}")

if __name__ == "__main__":
    main()
