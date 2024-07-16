# src/utils/template_handlers.py

from pathlib import Path
import yaml
from configs import variables

def load_instruction_template(template):
    if template == 'None':
        return ''

    templates_dir = variables.get_setting('instruction_templates_directory', 'instruction-templates')
    
    filepath = Path(f'{templates_dir}/{template}.yaml')
    if not filepath.exists():
        return ''

    with open(filepath, 'r', encoding='utf-8') as file:
        file_contents = file.read()
    
    data = yaml.safe_load(file_contents)
    return data.get('instruction_template', '')