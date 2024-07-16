# src/chat_logic/reply_handlers/reply_generation.py

import json
from configs import variables
from chat_logic.prompt_handlers.prompt_generation import prepare_prompt
from chat_logic.common_handlers.update_chat_display import update_chat_display
import html
from utils.logging_colors import logger

def remove_last_message(history):
    if len(history['visible']) > 0 and history['internal'][-1][0] != '<|BEGIN-VISIBLE-CHAT|>':
        last = history['visible'].pop()
        history['internal'].pop()
    else:
        last = ['', '']

    return html.unescape(last[0]), history


def generate_chat_reply(user_input, chat_history_json, mode, chat_style):
    model = variables.model  # Get the model from the variables module
    
    if model is None:
        raise ValueError("Model is not initialized. Please load a model first.")

    try:
        chat_history = json.loads(chat_history_json) if chat_history_json else {"internal": [], "visible": []}
    except json.JSONDecodeError:
        logger.error(f"Failed to parse chat history JSON: {chat_history_json}")
        chat_history = {"internal": [], "visible": []}
    
    # Prepare the prompt
    prompt = prepare_prompt(chat_history, user_input, mode, chat_style)
    
    # Generate the response using llama-cpp-python
    output = model(
        prompt,
        max_tokens=200,  # Allow for up to 200 new tokens
        temperature=0.7,
        top_p=0.95,
        stop=["User:", "\n\n"]  # Add appropriate stop tokens
    )
    
    response = output['choices'][0]['text']
    
    # Update the chat history
    chat_history['internal'].append({"role": "user", "content": user_input})
    chat_history['internal'].append({"role": "assistant", "content": response})
    chat_history['visible'].append([user_input, response])
    
    # Update the chat display
    chat_display = update_chat_display(chat_history)
    
    return chat_display, json.dumps(chat_history)

def continue_generation(chat_history_json, mode, chat_style):
    model = variables.model
    tokenizer = variables.tokenizer

    try:
        chat_history = json.loads(chat_history_json) if chat_history_json else {"internal": [], "visible": []}
    except json.JSONDecodeError:
        logger.error(f"Failed to parse chat history JSON: {chat_history_json}")
        chat_history = {"internal": [], "visible": []}

    if chat_history['internal']:
        last_assistant_message = chat_history['internal'][-1]['content']

        # Prepare the continuation prompt
        continuation_prompt = prepare_prompt(chat_history, "[CONTINUE]", mode, chat_style)

        # Generate the continuation
        input_ids = tokenizer.encode(continuation_prompt, return_tensors="pt")
        output = model.generate(input_ids, max_length=200, num_return_sequences=1, temperature=0.7)
        continuation = tokenizer.decode(output[0], skip_special_tokens=True)

        # Merge the continuation with the last message
        chat_history['internal'][-1]['content'] += f" {continuation}"
        chat_history['visible'][-1][1] += f" {continuation}"

        # Update the chat display
        chat_display = update_chat_display(chat_history)

        return chat_display, json.dumps(chat_history)

    return update_chat_display(chat_history), chat_history_json

def regenerate_response(chat_history_json, mode, chat_style):
    model = variables.model
    tokenizer = variables.tokenizer
    
    try:
        chat_history = json.loads(chat_history_json) if chat_history_json else {"internal": [], "visible": []}
    except json.JSONDecodeError:
        logger.error(f"Failed to parse chat history JSON: {chat_history_json}")
        chat_history = {"internal": [], "visible": []}
    
    if len(chat_history['internal']) >= 2:
        # Remove the last assistant response
        chat_history['internal'].pop()
        chat_history['visible'].pop()
        
        # Get the last user message
        last_user_message = chat_history['internal'][-1]['content']
        
        # Prepare the prompt for regeneration
        prompt = prepare_prompt(chat_history, last_user_message, mode, chat_style)
        
        # Generate a new response
        input_ids = tokenizer.encode(prompt, return_tensors="pt")
        output = model.generate(input_ids, max_length=200, num_return_sequences=1, temperature=0.7)
        new_response = tokenizer.decode(output[0], skip_special_tokens=True)
        
        # Add the new response to the chat history
        chat_history['internal'].append({"role": "assistant", "content": new_response})
        chat_history['visible'].append(["", new_response])
        
        # Update the chat display
        chat_display = update_chat_display(chat_history)
        
        return chat_display, json.dumps(chat_history)
    
    return update_chat_display(chat_history), chat_history_json