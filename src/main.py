# main.py
import sys
import signal
import gradio as gr
from configs import arguments, variables
from utils.logging_colors import logger
from user_interface.ui_chat import create_ui as create_chat_ui
from user_interface.event_handlers.ui_chat_events import setup_event_handlers as setup_chat_event_handlers
#from user_interface.ui_model_menu import create_ui as create_model_menu_ui
#from user_interface.event_handlers.ui_model_menu_events import setup_event_handlers as setup_model_menu_event_handlers
#from user_interface.ui_parameters import create_ui as create_parameters_ui
#from user_interface.event_handlers.ui_paramaters_events import setup_event_handlers as setup_parameters_event_handlers
#from user_interface.ui_settings import create_ui as create_settings_ui
#from user_interface.event_handlers.ui_settings_events import setup_event_handlers as setup_settings_event_handlers
#from user_interface.ui_training import create_ui as create_training_ui
#from user_interface.event_handlers.ui_training_events import setup_event_handlers as setup_training_event_handlers

def signal_handler(sig, frame):
    logger.info("Received Ctrl+C. Shutting down Text generation web UI gracefully.")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def main():
    with gr.Blocks() as demo:
        chat_ui_elements = create_chat_ui()
#        model_menu_ui_elements = create_model_menu_ui()
#        parameters_ui_elements = create_parameters_ui()
#        settings_ui_elements = create_settings_ui()
#        training_ui_elements = create_training_ui()
        
        # Combine all UI elements
        ui_elements = {**chat_ui_elements
                        #**model_menu_ui_elements, 
                        #**parameters_ui_elements, 
                        #**settings_ui_elements, 
                        #**training_ui_elements
                        }
        
        # Set up event handlers
        setup_chat_event_handlers(ui_elements)
 #       setup_model_menu_event_handlers(ui_elements)
 #       setup_parameters_event_handlers(ui_elements)
 #       setup_settings_event_handlers(ui_elements)
 #       setup_training_event_handlers(ui_elements)
    # Force some events to be triggered on page load
    variables.persistent_interface_state.update({
        'loader': arguments.args.loader,
        'mode': variables.settings['mode']
    })

    demo.launch()

if __name__ == "__main__":
    main()
