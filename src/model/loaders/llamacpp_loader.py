from utils.logging_colors import logger
from model.llamacpp_model import LlamaCppModel

def llamacpp_loader(model_path):
    logger(f"llama.cpp weights detected: \"{model_path}\"")

    try:
        logger("Initializing LlamaCppModel...")
        model = LlamaCppModel.from_pretrained(str(model_path))
        logger("LlamaCppModel initialized successfully")
        return model
    except Exception as e:
        logger(f"Error loading model: {str(e)}")
        logger("Detailed traceback:")
        return None