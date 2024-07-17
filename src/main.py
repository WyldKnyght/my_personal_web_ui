# src/main.py
import sys
import signal
import gradio as gr

import accelerate  # This early import makes Intel GPUs happy

from user_interface.ui_chat import create_ui
from user_interface.event_handlers.ui_chat_events import setup_event_handlers
from model.loaders.model_loader import load_model
from config import model_parameters
from config.model_parameters import model_settings
from utils.logging_colors import logger

def signal_handler(sig, frame):
    logger.info("Received Ctrl+C. Shutting down Text generation web UI gracefully.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():
    try:
        # Load the GGUF model
        model_name = model_parameters.get_setting('model_name')
        model = load_model(model_name)
        
        if model is None:
            raise ValueError(f"Failed to load model: {model_name}")

        model_parameters.model = model
        model_parameters.model_settings = model_settings

        logger.info("Creating UI elements...")
        with gr.Blocks() as demo:
            try:
                chat_ui_elements = create_ui()
            except Exception as e:
                logger.error(f"Error creating UI elements: {str(e)}")
                raise
            
            logger.info("Setting up event handlers...")
            try:
                setup_event_handlers(chat_ui_elements)
            except Exception as e:
                logger.error(f"Error setting up event handlers: {str(e)}")
                raise

        # Launch the Gradio interface
        server_name = '0.0.0.0'
        server_port = 7860
        share = False

        logger.info(f"Launching Gradio interface on {server_name}:{server_port}")
        demo.launch(
            server_name=server_name,
            server_port=server_port,
            share=share,
            inbrowser=True,
        )

    except Exception as e:
        logger.error(f"Failed to initialize the application: {str(e)}")
        logger.exception("Detailed traceback:")
        sys.exit(1)

if __name__ == "__main__":
    main()