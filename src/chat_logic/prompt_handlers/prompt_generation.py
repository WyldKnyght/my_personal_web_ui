# src/chat_logic/prompt_handlers/prompt_generation.py

from configs import variables

def prepare_prompt(chat_history, new_message, mode, chat_style):
    if mode == 'instruct':
        return prepare_instruct_prompt(new_message)
    elif mode == 'chat-instruct':
        return prepare_chat_instruct_prompt(chat_history, new_message, chat_style)
    else:  # default to 'chat' mode
        return prepare_chat_prompt(chat_history, new_message, chat_style)

def prepare_instruct_prompt(message):
    instruction_template = variables.settings.get('instruction_template', "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{instruction}\n\n### Response:")
    return instruction_template.format(instruction=message)

def prepare_chat_instruct_prompt(chat_history, new_message, chat_style):
    chat_instruct_template = variables.settings.get('chat_instruct_template', "Below is a conversation between a user and an AI assistant. Write the next response that appropriately continues the conversation.\n\n{chat_history}\n\nUser: {new_message}\n\nAssistant:")
    
    chat_history_str = format_chat_history(chat_history, chat_style)
    return chat_instruct_template.format(chat_history=chat_history_str, new_message=new_message)

def prepare_chat_prompt(chat_history, new_message, chat_style):
    chat_template = variables.settings.get('chat_template', "{chat_history}\nUser: {new_message}\nAssistant:")
    
    chat_history_str = format_chat_history(chat_history, chat_style)
    return chat_template.format(chat_history=chat_history_str, new_message=new_message)

def format_chat_history(chat_history, chat_style):
    formatted_history = ""
    for message in chat_history['internal']:
        if chat_style == 'default':
            formatted_history += f"{message['role'].capitalize()}: {message['content']}\n"
        elif chat_style == 'concise':
            prefix = 'U: ' if message['role'] == 'user' else 'A: '
            formatted_history += f"{prefix}{message['content']}\n"
        elif chat_style == 'descriptive':
            if message['role'] == 'user':
                formatted_history += f"The user says: \"{message['content']}\"\n"
            else:
                formatted_history += f"The AI assistant responds: \"{message['content']}\"\n"
        # Add more chat styles as needed
    return formatted_history.strip()

def get_generation_prompt(renderer, impersonate=False, strip_trailing_spaces=True):
    '''
    Given a Jinja template, reverse-engineers the prefix and the suffix for
    an assistant message (if impersonate=False) or an user message
    (if impersonate=True)
    '''

    if impersonate:
        messages = [
            {"role": "user", "content": "<<|user-message-1|>>"},
            {"role": "user", "content": "<<|user-message-2|>>"},
        ]
    else:
        messages = [
            {"role": "assistant", "content": "<<|user-message-1|>>"},
            {"role": "assistant", "content": "<<|user-message-2|>>"},
        ]

    prompt = renderer(messages=messages)

    suffix_plus_prefix = prompt.split("<<|user-message-1|>>")[1].split("<<|user-message-2|>>")[0]
    suffix = prompt.split("<<|user-message-2|>>")[1]
    prefix = suffix_plus_prefix[len(suffix):]

    if strip_trailing_spaces:
        prefix = prefix.rstrip(' ')

    return prefix, suffix
