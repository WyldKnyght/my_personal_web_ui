import re
from config.model_parameters import KEY_MAP
from model.handlers import metadata_gguf
from utils.file_manager import load_instruction_template
from config.model_parameters import MODELS_DIR

def get_model_metadata(model_name):
    model_settings = {}
    metadata = metadata_gguf.load_metadata(model_name)
    model_settings = process_metadata(metadata, model_settings, MODELS_DIR / model_name)

    if model_settings['instruction_template'] != 'Custom (obtained from model metadata)':
        model_settings['instruction_template_str'] = load_instruction_template(model_settings['instruction_template'])

    return model_settings

def process_metadata(metadata, model_settings, model_path):
    for k, v in metadata.items():
        for key, new_key in KEY_MAP.items():
            if k.endswith(key):
                model_settings[new_key] = v if key != 'n_gpu_layers' else v + 1

    if 'tokenizer.chat_template' in metadata:
        _extract_template(metadata['tokenizer.chat_template'], metadata, model_settings)

    model_settings.setdefault('instruction_template', 'Alpaca')
    model_settings['rope_freq_base'] = 10000
    return model_settings

def _extract_template(template, metadata, model_settings):
    if isinstance(template, list):
        template = template[0]['template']

    for token_key in ['eos_token', 'bos_token']:
        if token_key in metadata:
            value = metadata[token_key]
            if isinstance(value, dict):
                value = value['content']
            template = template.replace(token_key, f"'{value}'")

    _process_template(template, model_settings)

def _process_template(template, model_settings):
    template = re.sub(r'raise_exception\([^)]*\)', "''", template)
    template = re.sub(r'{% if add_generation_prompt %}.*', '', template, flags=re.DOTALL)
    model_settings['instruction_template'] = 'Custom (obtained from model metadata)'
    model_settings['instruction_template_str'] = template