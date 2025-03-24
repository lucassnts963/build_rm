import subprocess, os

import utils

def get_path_node():
    nodepath = os.path.join(os.getcwd(), 'node', 'node.exe')

    return nodepath

def generate_pdf_with_node(project='CALDEIRAS'):
    nodepath = get_path_node()
    cwd = os.getcwd()
    path_generator = os.path.join(cwd, 'pdf_generator', 'src', 'index.js')
    temp = utils.get_temp_folder(project=project)
    data_path = os.path.join(temp, 'data.json')

    output = temp

    try:
        command = f'{nodepath} {path_generator} -d {data_path} -o {output}'
        #print("Comando:", command)  # Imprime o comando para depuração
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Erro durante a execução do subprocesso:", e)
    except Exception as e:
        print("Erro desconhecido:", e)