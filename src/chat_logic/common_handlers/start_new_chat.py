# src/chat_logic/common_handlers/start_new_chat.py

from chat_logic.common_handlers.chat_utils import start_new_chat as utils_start_new_chat
from utils.history_handlers import save_history

def start_new_chat(state):
    history, unique_id = utils_start_new_chat(state)
    save_history(history, unique_id, state['mode'])
    return history