import re
import gradio as gr
import html
import json
from pathlib import Path

from configs import arguments
from utils.logging_colors import logger
from chat_logic.common_handlers.start_new_chat import start_new_chat
from utils.file_manager import get_paths, delete_file

def validate_mode(mode):
    valid_modes = ['chat', 'chat-instruct', 'instruct']
    if mode not in valid_modes:
        raise ValueError(f"Invalid mode: {mode}. Must be one of {valid_modes}")
    return mode

def get_history_file_path(unique_id, mode):
    mode = validate_mode(mode)
    return Path(f'logs/{mode}/{unique_id}.json')

def rename_history(old_id, new_id, mode):
    if arguments.args.multi_user:
        return

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

def save_history(history, unique_id, mode):
    if arguments.args.multi_user:
        return

    p = get_history_file_path(unique_id, mode)
    if not p.parent.is_dir():
        p.parent.mkdir(parents=True)

    with open(p, 'w', encoding='utf-8') as f:
        f.write(json.dumps(history, indent=4, ensure_ascii=False))

def find_all_histories(state):
    if arguments.args.multi_user:
        return ['']

    mode = validate_mode(state['mode'])
    paths = get_paths(state, mode=mode)
    histories = sorted(paths, key=lambda x: x.stat().st_mtime, reverse=True)
    return [path.stem for path in histories]

def find_all_histories_with_first_prompts(state):
    if arguments.args.multi_user:
        return []

    paths = get_paths(state)
    histories = sorted(paths, key=lambda x: x.stat().st_mtime, reverse=True)

    result = []
    for i, path in enumerate(histories):
        filename = path.stem
        if re.match(r'^[0-9]{8}-[0-9]{2}-[0-9]{2}-[0-9]{2}$', filename):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)

                first_prompt = ""
                if data and 'visible' in data and len(data['visible']) > 0:
                    if data['internal'][0][0] == '<|BEGIN-VISIBLE-CHAT|>':
                        if len(data['visible']) > 1:
                            first_prompt = html.unescape(data['visible'][1][0])
                        elif i == 0:
                            first_prompt = "New chat"
                    else:
                        first_prompt = html.unescape(data['visible'][0][0])
                elif i == 0:
                    first_prompt = "New chat"
        else:
            first_prompt = filename

        first_prompt = first_prompt.strip()

        if len(first_prompt) > 32:
            first_prompt = f'{first_prompt[:29]}...'

        result.append((first_prompt, filename))

    return result

def load_latest_history(state):
    if arguments.args.multi_user:
        return start_new_chat(state)

    histories = find_all_histories(state)

    return (
        load_history(histories[0], state['mode'])
        if len(histories) > 0
        else start_new_chat(state)
    )

def load_history_after_deletion(state, idx):
    if arguments.args.multi_user:
        return start_new_chat(state)

    histories = find_all_histories_with_first_prompts(state)
    idx = min(int(idx), len(histories) - 1)
    idx = max(0, idx)

    if len(histories) > 0:
        history = load_history(histories[idx][1], state['mode'])
    else:
        history = start_new_chat(state)
        histories = find_all_histories_with_first_prompts(state)

    return history, gr.update(choices=histories, value=histories[idx][1])

def load_history(unique_id, mode):
    p = get_history_file_path(unique_id, mode)

    f = json.loads(open(p, 'rb').read())
    return (
        f
        if 'internal' in f and 'visible' in f
        else {'internal': f['data'], 'visible': f['data_visible']}
    )

def load_history_json(file, history):
    try:
        file = file.decode('utf-8')
        f = json.loads(file)
        if 'internal' in f and 'visible' in f:
            history = f
        else:
            history = {
                'internal': f['data'],
                'visible': f['data_visible']
            }

        return history
    except Exception:
        return history

def delete_history(unique_id, mode):
    p = get_history_file_path(unique_id, mode)
    delete_file(p)