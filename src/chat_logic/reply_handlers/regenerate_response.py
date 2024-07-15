# src\chat_logic\reply_handlers\regenerate_response.py
from .generate_chat_reply import generate_chat_reply

def regenerate_response(chat_history_json, mode, chat_style):
    # Placeholder for regenerating the last response
    if chat_history_json['internal']:
        last_user_message = chat_history_json['internal'][-2]['content']
        return generate_chat_reply(last_user_message, chat_history_json, mode, chat_style)
    return chat_history_json, chat_history_json['visible']
