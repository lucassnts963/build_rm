import subprocess, os, datetime

def generate_pdf_with_node(data):
    cwd = os.getcwd()
    path_generator = os.path.join(cwd, 'src', 'pdf_generator', 'src', 'index.js')
    temp = os.path.join(cwd, 'temp')
    data_path = os.path.join(temp, 'data.json')

    filename = f'MTS-RMM-{data['request_number']}-{datetime.datetime.now().strftime("%d-%m-%Y_%Hhrs%Mmin%Sseg")}'

    output = os.path.join(temp, f'{filename}.pdf')

    try:
        command = f'node {path_generator} -d {data_path} -o {output} -n "{data["request_number"]}" -de "{data["expedition_date"]}" -dr "{data["draw_number"]}" -tg "{data["tag"]}" -a "{data["aplication"]}" -dy "{data['destiny']}" -l "{data['local']}"'
        #print("Comando:", command)  # Imprime o comando para depuração
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print("Erro durante a execução do subprocesso:", e)
    except Exception as e:
        print("Erro desconhecido:", e)