from pathlib import Path
from configs import variables
from utils.logging_colors import logger

def llamacpp_loader(model_name):
    from model_handlers.llamacpp_model import LlamaCppModel

    model_dir = Path(variables.get_setting('models_directory', 'models'))
    model_path = model_dir / model_name

    logger.info(f"Attempting to load model from: {model_path}")

    if not model_path.exists():
        logger.error(f"Model file does not exist: {model_path}")
        return None

    logger.info(f"llama.cpp weights detected: \"{model_path}\"")
    
    try:
        logger.info("Initializing LlamaCppModel...")
        model = LlamaCppModel.from_pretrained(str(model_path))
        logger.info("LlamaCppModel initialized successfully")
        return model  # Return only the model, not a tuple
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        logger.exception("Detailed traceback:")
        return None