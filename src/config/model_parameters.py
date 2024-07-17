from pathlib import Path

# Model variables
model = None
tokenizer = None
model_settings = {}
model_config = {}
user_config = {}


MODELS_DIR = Path('models')
TEMPLATES_DIR = Path('instruction-templates')

KEY_MAP = {
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

    # LLM settings
    'attention_sink_size': 0,
    'cache_capacity': 0,
    'm_lock': False,
    'mul_mat_q': True,
    'cache_4bit': False,
    'cache_8bit': False,
    'use_cpu': True,
    'tensorcores': False,
    'streaming_llm': False,
}

DEFAULT_INSTRUCTION_TEMPLATE = "Below is an instruction that describes a task. Write a response that appropriately completes the request.\n\n### Instruction:\n{instruction}\n\n### Response:"

# Function to update settings
def update_settings(new_settings):
    global model_settings
    model_settings.update(new_settings)

# Function to get a setting
def get_setting(key, default=None):
    return model_settings.get(key, default)
