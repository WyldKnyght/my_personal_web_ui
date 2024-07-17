import time
from utils.file_manager import get_model_path_and_file
from model.loaders.llamacpp_loader import llamacpp_loader
from model.handlers.metadata_processor import get_model_metadata
from config.model_parameters import MODELS_DIR, KEY_MAP
from utils.logging_colors import logger

def load_model(model_name):
    logger.info(f"Loading GGUF model: \"{model_name}\"")
    t0 = time.time()

    try:
        return _extracted_from_load_model_6(model_name, t0)
    except Exception as e:
        logger.info(f"Loading GGUF model: \"{model_name}\"")
        return None, None


# TODO Rename this here and in `load_model`
def _extracted_from_load_model_6(model_name, t0):
    metadata = get_model_metadata(model_name)
    logger(f"metadata: {metadata}")

    model_path, _ = get_model_path_and_file(model_name, '*.gguf', MODELS_DIR)
    model = llamacpp_loader(model_path)

    if model is None:
        raise ValueError(f"Failed to load model: {model_name}")

    model_settings = {k: v for k, v in metadata.items() if k in KEY_MAP}
    truncation_length = model_settings.get('n_ctx', 2048)
    instruction_template = model_settings.get('instruction_template', 'Default')

    logger(f"Loaded \"{model_name}\" in {(time.time()-t0):.2f} seconds.")
    logger(f"LOADER: \"llama.cpp\"")
    logger(f"TRUNCATION LENGTH: {truncation_length}")
    logger(f"INSTRUCTION TEMPLATE: \"{instruction_template}\"")

    return model, model_settings