import time
import json
import re
from pathlib import Path
from configs import variables
from utils.logging_colors import logger
from model_handlers import metadata_gguf
from model_handlers.llamacpp_loader import llamacpp_loader
from chat_logic.common_handlers.load_instuction_templates import load_instruction_template

def get_model_metadata(model_name):
    model_settings = {}

    # Get settings from models/config.yaml and models/config-user.yaml
    settings = variables.model_config
    for pat in settings:
        if re.match(pat.lower(), model_name.lower()):
            model_settings.update(settings[pat])

    # GGUF metadata
    path = Path(variables.models_directory) / model_name
    model_file = next(path.glob('*.gguf'), None)

    if model_file is None:
        logger.error(f"No GGUF file found for model: {model_name}")
        return model_settings

    metadata = metadata_gguf.load_metadata(model_file)
    model_settings = process_metadata(metadata, model_settings, path)

    # Apply user settings from models/config-user.yaml
    user_settings = variables.user_config
    for pat in user_settings:
        if re.match(pat.lower(), model_name.lower()):
            model_settings.update(user_settings[pat])

    # Load instruction template if defined by name rather than by value
    if model_settings['instruction_template'] != 'Custom (obtained from model metadata)':
        model_settings['instruction_template_str'] = load_instruction_template(model_settings['instruction_template'])

    return model_settings

def process_metadata(metadata, model_settings, path):
    for k, v in metadata.items():
        if k.endswith('context_length'):
            model_settings['n_ctx'] = v
        elif k.endswith('rope.freq_base'):
            model_settings['rope_freq_base'] = v
        elif k.endswith('rope.scale_linear') or k.endswith('rope.scaling.factor'):
            model_settings['compress_pos_emb'] = v
        elif k.endswith('block_count'):
            model_settings['n_gpu_layers'] = v + 1

    if 'tokenizer.chat_template' in metadata:
        _extract_chat_template(metadata, model_settings)

    tokenizer_config_path = path / 'tokenizer_config.json'
    if tokenizer_config_path.exists():
        with open(tokenizer_config_path, 'r', encoding='utf-8') as f:
            tokenizer_metadata = json.load(f)
        if 'chat_template' in tokenizer_metadata:
            _extract_instruction_template(tokenizer_metadata, model_settings)

    if 'instruction_template' not in model_settings:
        model_settings['instruction_template'] = 'Alpaca'

    if model_settings.get('rope_freq_base') == 10000:
        model_settings.pop('rope_freq_base', None)

    return model_settings

def _extract_chat_template(metadata, model_settings):
    template = metadata['tokenizer.chat_template']
    eos_token = metadata['tokenizer.ggml.tokens'][metadata['tokenizer.ggml.eos_token_id']]
    bos_token = metadata['tokenizer.ggml.tokens'].get(metadata.get('tokenizer.ggml.bos_token_id', ''), "")

    template = template.replace('eos_token', f"'{eos_token}'")
    template = template.replace('bos_token', f"'{bos_token}'")

    _process_template(template, model_settings)

def _extract_instruction_template(tokenizer_metadata, model_settings):
    template = tokenizer_metadata['chat_template']
    if isinstance(template, list):
        template = template[0]['template']

    for k in ['eos_token', 'bos_token']:
        if k in tokenizer_metadata:
            value = tokenizer_metadata[k]
            if isinstance(value, dict):
                value = value['content']
            template = template.replace(k, f"'{value}'")

    _process_template(template, model_settings)

def _process_template(template, model_settings):
    template = re.sub(r'raise_exception\([^)]*\)', "''", template)
    template = re.sub(r'{% if add_generation_prompt %}.*', '', template, flags=re.DOTALL)
    model_settings['instruction_template'] = 'Custom (obtained from model metadata)'
    model_settings['instruction_template_str'] = template

def load_model(model_name):
    logger.info(f"Loading GGUF model: \"{model_name}\"")
    print(f"Loading GGUF model: \"{model_name}\"")
    t0 = time.time()

    variables.model_name = model_name
    print(f"variables.model_name: {variables.model_name}")

    try:
        metadata = get_model_metadata(model_name)
        print(f"metadata: {metadata}")

        # Always use llama.cpp loader for GGUF models
        loader = 'llama.cpp'
        variables.settings['loader'] = loader
        print(f"variables.settings['loader']: {variables.settings['loader']}")

        model = llamacpp_loader(model_name)  # Expect a single model, not a tuple
        print(f"model: {model}")

        if model is None:
            raise ValueError(f"Failed to load model: {model_name}")

        variables.settings.update({k: v for k, v in metadata.items() if k in variables.settings})
        variables.settings['truncation_length'] = variables.get_setting('n_ctx', 2048)
        print(f"variables.settings['truncation_length']: {variables.settings['truncation_length']}")

        logger.info(f"Loaded \"{model_name}\" in {(time.time()-t0):.2f} seconds.")
        print(f"Loaded \"{model_name}\" in {(time.time()-t0):.2f} seconds.")
        logger.info(f"LOADER: \"{loader}\"")
        print(f"LOADER: \"{loader}\"")
        logger.info(f"TRUNCATION LENGTH: {variables.settings['truncation_length']}")
        print(f"TRUNCATION LENGTH: {variables.settings['truncation_length']}")
        logger.info(f"INSTRUCTION TEMPLATE: \"{variables.get_setting('instruction_template')}\"")
        print(f"INSTRUCTION TEMPLATE: \"{variables.get_setting('instruction_template')}\"")

        variables.model = model
        variables.tokenizer = model  # For llama.cpp, model and tokenizer are the same object
        variables.model_settings = variables.settings.copy()
        print(f"variables.model: {variables.model}, variables.tokenizer: {variables.tokenizer}, variables.model_settings: {variables.model_settings}")

        return model

    except Exception as e:
        logger.error(f"Error loading model {model_name}: {str(e)}")
        print(f"Error loading model {model_name}: {str(e)}")
        return None

def llamacpp_loader(model_name):
    from model_handlers.llamacpp_model import LlamaCppModel

    model_dir = Path(variables.get_setting('models_directory', 'models'))
    model_path = model_dir / model_name

    logger.info(f"Attempting to load model from: {model_path}")

    if not model_path.exists():
        logger.error(f"Model file does not exist: {model_path}")
        return None

    logger.info(f"llama.cpp weights detected: \"{model_path}\"")

    try:
        logger.info("Initializing LlamaCppModel...")
        model = LlamaCppModel.from_pretrained(str(model_path))
        logger.info("LlamaCppModel initialized successfully")
        return model  # Return only the model, not a tuple
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        logger.exception("Detailed traceback:")
        return None
