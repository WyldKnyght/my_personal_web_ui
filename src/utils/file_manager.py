# src/utils/file_manager.py
import os
import json
from pathlib import Path
from utils.logging_colors import logger
import yaml
from config.model_parameters import TEMPLATES_DIR

def load_instruction_template(template):
    template_path = Path(TEMPLATES_DIR) / f'{template}.yaml'
    if template == 'None' or not template_path.exists():
        return ''
    data = load_yaml_file(template_path)
    return data.get('instruction_template', '')

def get_model_path_and_file(model_name, file_pattern, models_dir):
    model_path = models_dir / model_name
    model_file = next(model_path.glob(file_pattern), None)
    return model_path, model_file

def load_yaml_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)
    
def get_history_file_path(unique_id, mode):
    valid_modes = ['chat', 'chat-instruct', 'instruct']
    if mode not in valid_modes:
        raise ValueError(f"Invalid mode: {mode}. Must be one of {valid_modes}")
    return Path(f'logs/{mode}/{unique_id}.json')

def get_paths(state):
    mode = state['mode']
    if mode == 'instruct':
        return Path('logs/instruct').glob('*.json')
    elif mode in ['chat', 'chat-instruct']:
        return Path(f'logs/{mode}').glob('*.json')
    else:
        logger.error(f"Invalid mode: {mode}")
        return []

def save_history(history, unique_id, mode):
    p = get_history_file_path(unique_id, mode)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=4, ensure_ascii=False)
    logger.info(f"Saved history to {p}")

def save_file(fname, contents):
    if fname == '':
        logger.error('File name is empty!')
        return

    root_folder = Path(__file__).resolve().parent.parent
    abs_path_str = os.path.abspath(fname)
    rel_path_str = os.path.relpath(abs_path_str, root_folder)
    rel_path = Path(rel_path_str)
    if rel_path.parts[0] == '..':
        logger.error(f'Invalid file path: "{fname}"')
        return

    with open(abs_path_str, 'w', encoding='utf-8') as f:
        f.write(contents)

    logger.info(f'Saved "{abs_path_str}".')

def delete_file(fname):
    if fname == '':
        logger.error('File name is empty!')
        return

    root_folder = Path(__file__).resolve().parent.parent
    abs_path_str = os.path.abspath(fname)
    rel_path_str = os.path.relpath(abs_path_str, root_folder)
    rel_path = Path(rel_path_str)
    if rel_path.parts[0] == '..':
        logger.error(f'Invalid file path: "{fname}"')
        return

    if rel_path.exists():
        rel_path.unlink()
        logger.info(f'Deleted "{fname}".')