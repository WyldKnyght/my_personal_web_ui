# src\chat_logic\common_handlers\update_chat_display.py

def update_chat_display(history):
    display = ""
    for exchange in history['visible']:
        if len(exchange) == 2:
            user_message, assistant_message = exchange
            display += f"<div class='user-message'><strong>User:</strong> {user_message}</div>"
            display += f"<div class='assistant-message'><strong>Assistant:</strong> {assistant_message}</div>"
    
    return display