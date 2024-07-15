def update_chat_display(chat_history):
    display_text = ""
    for entry in chat_history:
        if entry['role'] == 'user':
            display_text += f"User: {entry['content']}\n\n"
        elif entry['role'] == 'assistant':
            display_text += f"Assistant: {entry['content']}\n\n"
        elif entry['role'] == 'system':
            display_text += f"System: {entry['content']}\n\n"
        # Add more roles if needed
    
    return display_text.strip()