import tkinter.messagebox as mg

import math, os, shutil, subprocess

def get_temp_folder(foldername = 'temp'):
    temp = os.path.join(os.getcwd(), foldername)

    try:
        if not os.path.exists(temp):
            os.makedirs(temp)
    except Exception as e:
        mg.showerror('Error', f'Erro ao tentar criar pasta temp! {e}')
    return temp

def round_to_nearest_multiple_of_6(number):
    return math.ceil(number / 6) * 6

def get_request_number(file_path=os.path.join(get_temp_folder(), 'request_counter.txt')):
    
    try:
        if not os.path.exists(file_path):
            with open(file_path, 'w') as file:
                # Initialize the counter if the file doesn't exist
                file.write('0')
                return 0

        with open(file_path, 'r+') as file:
            counter = int(file.read())
            return counter
        
    except Exception as e:
        mg.showerror('Error', f'Erro ao acessar o arquivo {file_path}! [{e}]')

def increment_request_number(file_path=os.path.join(get_temp_folder(), 'request_counter.txt')):
    # Read the current counter value
    counter = get_request_number(file_path)
    
    # Increment the counter
    counter += 1
    
    # Write the updated counter value back to the file
    try:
        with open(file_path, 'w') as file:
            file.write(str(counter))
    except Exception as e:
        mg.showerror('Error', f'Erro ao atualizar número da requisição no arquivo {file_path}! [{e}]')
        return
    
    return counter

def copy_and_rename_file(src_file, dest_folder, new_filename):
    """Copies a file and renames it.

    Args:
        src_file (str): Full path to the source file.
        dest_folder (str): Full path to the destination folder.
        new_filename (str): The new name for the copied file (with extension).
    """

    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # Create the destination folder if it doesn't exist

    dest_path = os.path.join(dest_folder, new_filename)

    try:
        shutil.copy(src_file, dest_path)
        print(f"File copied and renamed to {dest_path}")
    except shutil.Error as e:
        print(f"An error occurred: {e}")

def get_data_path(filename = '04 - Controle de Materiais_Flavio.xlsx', project = 'CALDEIRAS'):
    UTILIDADES =  os.path.join(
        'C:\\', 
        'Users', 
        'lucas.santos', 
        'Montisol Construcao e Manutencao', 
        'Suleima Caldas - CT_4600011662_Utilidades',
        '01.QUALIDADE',
        '5.Recebimento de materiais', 
        'BI - Controle de Materiais atualizada 2024.xlsx')
    
    CALDEIRAS = os.path.join(
        'C:\\', 
        'Users', 
        'lucas.santos', 
        'Montisol Construcao e Manutencao', 
        'Suleima Caldas - CT_ 4600011605_Caldeiras',
        '01.QUALIDADE',
        '5.Recebimento de materiais', 
        filename)
    
    if project == 'UTILIDADES':
        return UTILIDADES
    
    if project == 'CALDEIRAS':
        return CALDEIRAS

def get_project_path(filename = '02 - Acompanhamento de projetos_Lucas.xlsx', project = 'CALDEIRAS'):
    UTILIDADES =  os.path.join(
        'C:\\', 
        'Users', 
        'lucas.santos', 
        'Montisol Construcao e Manutencao', 
        'Suleima Caldas - CT_4600011662_Utilidades',
        '01.QUALIDADE',
        '5.Recebimento de materiais', 
        'BI - Controle de Materiais atualizada 2024.xlsx')
    
    CALDEIRAS = os.path.join(
        'C:\\', 
        'Users', 
        'lucas.santos', 
        'Montisol Construcao e Manutencao', 
        'Suleima Caldas - CT_ 4600011605_Caldeiras',
        '01.QUALIDADE',
        '4.PROJETOS', 
        filename)
    
    if project == 'UTILIDADES':
        return UTILIDADES
    
    if project == 'CALDEIRAS':
        return CALDEIRAS

def put_zero_in_front(number):
    if number < 9 and number > 0:
        return f'0{number}'
    else:
        return f'{number}'

def open_file(filepath):
        try:
            command = f'start "" {filepath}'
            print("Comando:", command)  # Imprime o comando para depuração
            subprocess.run(command, check=True, shell=True)
        except subprocess.CalledProcessError as e:
            print("Erro durante a execução do subprocesso:", e)
        except Exception as e:
            print("Erro desconhecido:", e)