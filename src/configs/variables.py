# variables.py

from pathlib import Path

# Model-related variables
model_name = None
model = None
tokenizer = None
model_settings = {}

# LoRA-related variables
lora_names = []
loras = {}

# UI-related variables
gradio_variables = {}

# Settings
settings = {
    'max_new_tokens': 200,
    'max_new_tokens_min': 1,
    'max_new_tokens_max': 2000,
    'truncation_length': 2048,
    'truncation_length_min': 0,
    'truncation_length_max': 8192,
    'auto_max_new_tokens': False,
    'ban_eos_token': False,
    'add_bos_token': True,
    'skip_special_tokens': True,
    'stream': True,
    'seed': -1,
    'custom_stopping_strings': [],
    'custom_token_bans': None,
    'autoload_model': False,
    'dark_theme': True,
}

# Paths
models_directory = Path('models')
loras_directory = Path('loras')
prompts_directory = Path('prompts')
presets_directory = Path('presets')
training_datasets_directory = Path('training/datasets')
training_formats_directory = Path('training/formats')

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