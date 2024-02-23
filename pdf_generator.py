from weasyprint import HTML, CSS
from jinja2 import Environment, FileSystemLoader
import os

def generate_pdf(data):
    print('Gerando PDF ...')
    file_loader = FileSystemLoader(os.getcwd())
    env = Environment(loader=file_loader)

    template = env.get_template('template.html')

    html = template.render(data)

    css = CSS(filename='styles.css')

    pdf = HTML(string=html).write_pdf(stylesheets=[css])
    open('sample_rm.pdf', 'wb').write(pdf)
    print('PDF Gerado!')