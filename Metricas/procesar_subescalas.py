import os
import csv
import pandas as pd

# Define subscales and their corresponding questions
SUBCALES = {
    'Auto-amabilidad': [5, 12, 19, 23, 26],
    'Humanidad_comun': [3, 7, 10, 15],
    'Mindfulness': [9, 14, 17, 22],
    'Auto-juicio': [1, 8, 11, 16, 21],
    'Aislamiento': [4, 13, 18, 25],
    'Sobre-identificacion': [2, 6, 20, 24]
}

# Questions that need to be inverted for global mean calculation
INVERTED_QUESTIONS = [1, 2, 4, 6, 8, 11, 13, 16, 18, 20, 21, 24, 25]

def invert_value(value):
    """Invert a value: 1->5, 2->4, 3->3, 4->2, 5->1"""
    if value == 0:  # Handle missing values
        return 0
    return 6 - value

def calculate_subscale_mean(data, questions):
    """Calculate mean for a specific subscale"""
    values = []
    for q in questions:
        if q in data and data[q] != 0:  # Exclude missing values (0)
            values.append(data[q])
    
    if not values:
        return 0.0
    return sum(values) / len(values)

def calculate_global_mean(data):
    """Calculate global mean with inverted values for specific questions"""
    values = []
    for q in range(1, 27):  # Questions 1-26
        if q in data and data[q] != 0:  # Exclude missing values
            value = data[q]
            if q in INVERTED_QUESTIONS:
                value = invert_value(value)
            values.append(value)
    
    if not values:
        return 0.0
    return sum(values) / len(values)

def process_experience_data(csv_file_path):
    """Process the experience data CSV file using pandas"""
    
    # Read the CSV file with pandas, skipping the first row (FASE 1, FASE 2 headers)
    df = pd.read_csv(csv_file_path, skiprows=1, index_col=0)
    
    # Get participant names from columns
    participants = df.columns.tolist()
    
    # Automatically detect phases by analyzing column names
    phases = []
    phase_participants = {}
    
    # Strategy 1: Check if this is a standard 2-phase format (like Datos_experiencia.csv)
    # In this format, the first half of participants are FASE 1, second half are FASE 2
    if len(participants) >= 2:
        # Split participants into phases
        mid_point = len(participants) // 2
        phases = ["FASE 1", "FASE 2"]
        phase_participants = {
            "FASE 1": participants[:mid_point],
            "FASE 2": participants[mid_point:]
        }
    
    # Strategy 2: Look for patterns like ".1", ".2", etc. (for other formats)
    else:
        participant_counts = {}
        for participant in participants:
            base_name = participant.split('.')[0]  # Remove .1, .2, etc.
            participant_counts[base_name] = participant_counts.get(base_name, 0) + 1
        
        if max(participant_counts.values()) > 1:
            # Multiple phases detected with naming pattern
            unique_base_names = list(participant_counts.keys())
            for i, base_name in enumerate(unique_base_names):
                phase_name = f"FASE {i+1}"
                phases.append(phase_name)
                phase_participants[phase_name] = []
                
                # Find all participants for this phase
                for participant in participants:
                    if participant.startswith(base_name):
                        phase_participants[phase_name].append(participant)
        
        # Strategy 3: Single phase
        else:
            phases = ["FASE 1"]
            phase_participants = {"FASE 1": participants}
    
    # Results storage
    subscale_results = []
    global_results = []
    
    # Process each phase
    for phase in phases:
        for participant in phase_participants[phase]:
            participant_data = {}
            
            # Extract question values for this participant
            for question in range(1, 27):
                if question in df.index:
                    value = df.loc[question, participant]
                    if pd.notna(value):  # Check if value is not NaN
                        participant_data[question] = int(value)
                    else:
                        participant_data[question] = 0
                else:
                    participant_data[question] = 0
            
            # Calculate subscale means
            subscale_means = {}
            for subscale_name, questions in SUBCALES.items():
                mean = calculate_subscale_mean(participant_data, questions)
                subscale_means[subscale_name] = round(mean, 2)
            
            # Calculate global mean
            global_mean = round(calculate_global_mean(participant_data), 2)
            
            # Store results
            subscale_row = {
                'Participante': participant,
                'Fase': phase,
                **subscale_means
            }
            subscale_results.append(subscale_row)
            
            global_row = {
                'Participante': participant,
                'Fase': phase,
                'Media_Global': global_mean
            }
            global_results.append(global_row)
    
    return subscale_results, global_results

def save_results(subscale_results, global_results, output_dir, input_filename):
    """Save results to CSV files using pandas"""
    
    # Create results directory inside the data directory
    results_dir = os.path.join(output_dir, 'Resultados')
    os.makedirs(results_dir, exist_ok=True)
    
    # Generate output filenames based on input filename
    base_name = os.path.splitext(input_filename)[0]  # Remove .csv extension
    subscale_file = os.path.join(results_dir, f'{base_name}_subescalas.csv')
    global_file = os.path.join(results_dir, f'{base_name}_global.csv')
    
    # Save subscale results
    if subscale_results:
        subscale_df = pd.DataFrame(subscale_results)
        subscale_df.to_csv(subscale_file, index=False, encoding='utf-8')
        print(f"Resultados de subescalas guardados en: {subscale_file}")
    
    # Save global results
    if global_results:
        global_df = pd.DataFrame(global_results)
        global_df.to_csv(global_file, index=False, encoding='utf-8')
        print(f"Resultados de media global guardados en: {global_file}")

def print_summary(subscale_results, global_results):
    """Print a summary of the results"""
    print("\n" + "="*80)
    print("RESUMEN DE RESULTADOS")
    print("="*80)
    
    # Group by participant
    participants = sorted(set(r['Participante'] for r in subscale_results))
    
    for participant in participants:
        print(f"\nParticipante: {participant}")
        print("-" * 60)
        
        # Get all phases for this participant
        participant_phases = sorted(set(r['Fase'] for r in subscale_results if r['Participante'] == participant))
        
        for phase in participant_phases:
            print(f"\n{phase}:")
            
            # Find subscale results for this participant and phase
            subscale_data = next((r for r in subscale_results 
                                 if r['Participante'] == participant and r['Fase'] == phase), None)
            
            if subscale_data:
                for subscale_name in SUBCALES.keys():
                    print(f"  {subscale_name}: {subscale_data[subscale_name]}")
            
            # Find global result for this participant and phase
            global_data = next((r for r in global_results 
                               if r['Participante'] == participant and r['Fase'] == phase), None)
            
            if global_data:
                print(f"  Media Global: {global_data['Media_Global']}")

def list_available_files(data_dir):
    """List all CSV files in the data directory (excluding results folder)"""
    csv_files = []
    if os.path.exists(data_dir):
        for file in os.listdir(data_dir):
            if file.endswith('.csv'):
                csv_files.append(file)
    return sorted(csv_files)

def select_csv_file(data_dir):
    """Let user select which CSV file to process"""
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
                print(f"Por favor ingrese un número entre 1 y {len(csv_files)}")
        except ValueError:
            print("Por favor ingrese un número válido")

def main():
    """Main function to process experience data"""
    try:
        # Define file paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, 'Datos')
        
        # Let user select CSV file
        selected_file = select_csv_file(data_dir)
        if not selected_file:
            print("No se seleccionó ningún archivo. Saliendo...")
            return
        
        csv_file = os.path.join(data_dir, selected_file)
        
        print(f"\nProcesando archivo: {selected_file}")
        
        # Process the data
        subscale_results, global_results = process_experience_data(csv_file)
        
        # Save results
        save_results(subscale_results, global_results, data_dir, selected_file)
        
        # Print summary
        print_summary(subscale_results, global_results)
        
        print(f"\n¡Procesamiento completado! Se procesaron {len(subscale_results)} registros.")
        
    except Exception as e:
        print(f"Error durante el procesamiento: {e}")

if __name__ == "__main__":
    main()
