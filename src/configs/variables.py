# src/configs/variables.py

from pathlib import Path

# Model-related variables
model = None
model_settings = {}
model_config = {}
user_config = {}

# UI-related variables
gradio_variables = {}

# Paths
models_directory = Path('models')
prompts_directory = Path('prompts')
presets_directory = Path('presets')

default_settings = {
    # Llama-cpp-python parameters
    'model_name': "codellama-7b-python.Q4_K_M.gguf",
    'models_directory': 'models',
    'n_gpu_layers': 0,
    'main_gpu': 0,
    'tensor_split': '',
    'use_mmap': True,
    'use_mlock': False,
    'vocab_only': False,
    'n_ctx': 2048,
    'n_batch': 512,
    'n_threads': None,
    'n_threads_batch': None,
    'rope_scaling': None,
    'rope_freq_base': 10000,
    'rope_freq_scale': 1.0,
    'yarn_ext_factor': -1.0,
    'yarn_attn_factor': 1.0,
    'yarn_beta_fast': 32.0,
    'yarn_beta_slow': 1.0,
    'yarn_orig_ctx': 0,
    'logits_all': False,
    'embedding': False,
    'offload_kqv': False,
    'last_n_tokens_size': 64,
    'lora_base': None,
    'lora_path': None,
    'numa': False,
    'chat_format': "llama-2",
    'verbose': True,
    'seed': -1,

    # Additional parameters
    'max_tokens': 200,  # Equivalent to 'max_new_tokens'
    'temperature': 0.7,
    'top_p': 0.95,
    'top_k': 40,
    'repeat_penalty': 1.1,  # Equivalent to 'repetition_penalty'
    'presence_penalty': 0.0,
    'frequency_penalty': 0.0,
    'mirostat_mode': 0,
    'mirostat_tau': 5.0,
    'mirostat_eta': 0.1,
    'stream': True,
    'stop': None,  # Equivalent to 'custom_stopping_strings'
    'tfs_z': 1.0,
    'grammar': None,

    # UI and other settings
    'mode': 'chat',
    'instruction_template': "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{instruction}\n\n### Response:",
    'chat_instruct_template': "Below is a conversation between a user and an AI assistant. Write the next response that appropriately continues the conversation.\n\n{chat_history}\n\nUser: {new_message}\n\nAssistant:",
    'chat_template': "{chat_history}\nUser: {new_message}\nAssistant:",
    'dark_theme': True,
    'instruction_templates_directory': 'instruction-templates',
}

# Settings (initialized with default values)
settings = default_settings.copy()

# Runtime variables
need_restart = False
persistent_interface_state = {}

# Function to update settings
def update_settings(new_settings):
    global settings
    settings.update(new_settings)

# Function to get a setting
def get_setting(key, default=None):
    return settings.get(key, default)