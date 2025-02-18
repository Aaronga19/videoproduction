import jinja2
import pdfkit
from datetime import datetime

def get_contract(client_name:str,client_address:str,initial_date:datetime, end_date:datetime, total_amount:float, garantee_amount:float,folio:str):

    context = {
        'client_name': client_name,
        'client_address': client_address,
        'initial_date':initial_date,
        'end_date':end_date,
        'total_amount':total_amount,
        'garantee_amount':garantee_amount,
        'folio':folio
        # 'items':items
        }

    template_loader = jinja2.FileSystemLoader('C:/Users/ARCAN/OneDrive/Escritorio/Documentos/Software/VideoProductora/contract/')
    template_env = jinja2.Environment(loader=template_loader)

    html_template = 'contract.html'
    template = template_env.get_template(html_template)
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf='c:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    output_path = 'contract/meta/contract.pdf'
    pdfkit.from_string(output_text, output_path, configuration=config, options={"enable-local-file-access": ""}, css='C:/Users/ARCAN/OneDrive/Escritorio/Documentos/Software/VideoProductora/contract/styles.css')

    return output_path