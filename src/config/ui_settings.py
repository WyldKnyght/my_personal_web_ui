# src/config/ui_settings.py
import pathlib as Path

# UI-related variables
gradio_variables = {}
prompts_directory = Path.Path('prompts')
presets_directory = Path.Path('presets')
need_restart = False
persistent_interface_state = {}

# Generation variables
stop_everything = False
generation_lock = None
processing_message = '*Is typing...*'

# UI settings
mode = "chat"
instruction_template = "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{instruction}\n\n### Response:"
chat_instruct_template = "Below is a conversation between a user and an AI assistant. Write the next response that appropriately continues the conversation.\n\n{chat_history}\n\nUser: {new_message}\n\nAssistant:"
chat_template = "{chat_history}\nUser: {new_message}\nAssistant:"
dark_theme = True
instruction_templates_directory = 'instruction-templates'
