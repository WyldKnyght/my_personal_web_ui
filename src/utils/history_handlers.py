import gradio as gr
import pathlib as Path
import json

from utils.file_manager import get_paths
from utils.logging_colors import logger
from utils.file_manager import delete_file
from chat_logic.common_handlers.chat_utils import start_new_chat

def rename_chat(old_id, new_id, mode):
    if not new_id.strip():
        return gr.update(), "Error: New name cannot be empty."

    if new_id := "".join(
        c for c in new_id if c.isalnum() or c in (' ', '_', '-')
    ).strip():
        return rename_history(old_id, new_id, mode)
    else:
        return gr.update(), "Error: Invalid new name. Please use only letters, numbers, spaces, underscores, or hyphens."
    
def rename_history(old_id, new_id, mode):
    old_p = get_history_file_path(old_id, mode)
    new_p = get_history_file_path(new_id, mode)

    if new_p.parent != old_p.parent:
        logger.error(f"The following path is not allowed: \"{new_p}\".")
    elif new_p == old_p:
        logger.info("The provided path is identical to the old one.")
    elif new_p.exists():
        logger.error(f"The new path already exists and will not be overwritten: \"{new_p}\".")
    else:
        logger.info(f"Renaming \"{old_p}\" to \"{new_p}\"")
        old_p.rename(new_p)

def get_history_file_path(unique_id, mode):
    valid_modes = ['chat', 'chat-instruct', 'instruct']
    if mode not in valid_modes:
        raise ValueError(f"Invalid mode: {mode}. Must be one of {valid_modes}")
    return Path(f'logs/{mode}/{unique_id}.json')

def delete_history(unique_id, mode):
    p = get_history_file_path(unique_id, mode)
    delete_file(p)

def load_latest_history(state):
    histories = find_all_histories(state)
    if len(histories) > 0:
        return load_history(histories[0], state['mode'])
    history, unique_id = start_new_chat(state)
    save_history(history, unique_id, state['mode'])
    return history

def find_all_histories(state):
    mode = validate_mode(state['mode'])
    paths = get_paths(state, mode=mode)
    histories = sorted(paths, key=lambda x: x.stat().st_mtime, reverse=True)
    return [path.stem for path in histories]

def load_history(unique_id, mode):
    p = get_history_file_path(unique_id, mode)
    f = json.loads(open(p, 'rb').read())
    return (
        f
        if 'internal' in f and 'visible' in f
        else {'internal': f['data'], 'visible': f['data_visible']}
    )

def save_history(history, unique_id, mode):
    p = get_history_file_path(unique_id, mode)

    if not p.parent.is_dir():
        p.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

    with open(p, 'w', encoding='utf-8') as f:
        f.write(json.dumps(history, indent=4, ensure_ascii=False))

def validate_mode(mode):
    valid_modes = ['chat', 'chat-instruct', 'instruct']
    if mode not in valid_modes:
        raise ValueError(f"Invalid mode: {mode}. Must be one of {valid_modes}")
    return mode
