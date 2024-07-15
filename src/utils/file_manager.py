import os

from datetime import datetime
from pathlib import Path

from utils.logging_colors import logger
from utils.history_handlers import get_history_file_path

def get_paths(state):
    if state['mode'] == 'instruct':
        return Path('logs/instruct').glob('*.json')
    character = state['character_menu']

    # Handle obsolete filenames and paths
    old_p = Path(f'logs/{character}_persistent.json')
    new_p = Path(f'logs/persistent_{character}.json')
    if old_p.exists():
        logger.warning(f"Renaming \"{old_p}\" to \"{new_p}\"")
        old_p.rename(new_p)

    if new_p.exists():
        unique_id = datetime.now().strftime('%Y%m%d-%H-%M-%S')
        p = get_history_file_path(unique_id, character, state['mode'])
        logger.warning(f"Moving \"{new_p}\" to \"{p}\"")
        p.parent.mkdir(exist_ok=True)
        new_p.rename(p)

    return Path(f'logs/chat/{character}').glob('*.json')


def save_file(fname, contents):
    if fname == '':
        logger.error('File name is empty!')
        return

    root_folder = Path(__file__).resolve().parent.parent
    abs_path_str = os.path.abspath(fname)
    rel_path_str = os.path.relpath(abs_path_str, root_folder)
    rel_path = Path(rel_path_str)
    if rel_path.parts[0] == '..':
        logger.error(f'Invalid file path: \"{fname}\"')
        return

    with open(abs_path_str, 'w', encoding='utf-8') as f:
        f.write(contents)

    logger.info(f'Saved \"{abs_path_str}\".')


def delete_file(fname):
    if fname == '':
        logger.error('File name is empty!')
        return

    root_folder = Path(__file__).resolve().parent.parent
    abs_path_str = os.path.abspath(fname)
    rel_path_str = os.path.relpath(abs_path_str, root_folder)
    rel_path = Path(rel_path_str)
    if rel_path.parts[0] == '..':
        logger.error(f'Invalid file path: \"{fname}\"')
        return

    if rel_path.exists():
        rel_path.unlink()
        logger.info(f'Deleted \"{fname}\".')

