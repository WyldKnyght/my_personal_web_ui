import copy
import ast
import html
import time
import variables, arguments
from models.event_handlers.models import clear_torch_cache, load_model
from text_generation.print_prompt import print_prompt
from utils.extension_handler import apply_extensions
from utils.logging_colors import logger
from text_generation.generate_reply_custom import generate_reply_custom
from text_generation.generate_reply_HF import generate_reply_HF
from models.event_handlers.set_manual_seed import set_manual_seed
from models.event_handlers import models
from utils.stopping_event_handler import apply_stopping_strings

def generate_reply(*args, **kwargs):
    if arguments.args.idle_timeout > 0 and variables.model is None and variables.previous_model_name not in [None, 'None']:
        variables.model, variables.tokenizer = load_model(variables.previous_model_name)

    variables.generation_lock.acquire()
    try:
        yield from _generate_reply(*args, **kwargs)
    finally:
        models.last_generation_time = time.time()
        variables.generation_lock.release()


def _generate_reply(question, state, stopping_strings=None, is_chat=False, escape_html=False, for_ui=False):

    # Find the appropriate generation function
    generate_func = apply_extensions('custom_generate_reply')
    if generate_func is None:
        if variables.model_name == 'None' or variables.model is None:
            logger.error("No model is loaded! Select one in the Model tab.")
            yield ''
            return

        if variables.model.__class__.__name__ in ['LlamaCppModel', 'Exllamav2Model', 'TensorRTLLMModel']:
            generate_func = generate_reply_custom
        else:
            generate_func = generate_reply_HF

    if generate_func != generate_reply_HF and arguments.args.verbose:
        logger.info("PROMPT=")
        print_prompt(question)

    # Prepare the input
    original_question = question
    if not is_chat:
        state = apply_extensions('state', state)
        question = apply_extensions('input', question, state)

    # Find the stopping strings
    all_stop_strings = []
    for st in (stopping_strings, state['custom_stopping_strings']):
        if type(st) is str:
            st = ast.literal_eval(f"[{st}]")

        if type(st) is list and len(st) > 0:
            all_stop_strings += st

    variables.stop_everything = False
    clear_torch_cache()
    seed = set_manual_seed(state['seed'])
    last_update = -1
    reply = ''
    is_stream = state['stream']
    if len(all_stop_strings) > 0 and not state['stream']:
        state = copy.deepcopy(state)
        state['stream'] = True

    min_update_interval = 0
    if state.get('max_updates_second', 0) > 0:
        min_update_interval = 1 / state['max_updates_second']

    # Generate
    for reply in generate_func(question, original_question, seed, state, stopping_strings, is_chat=is_chat):
        reply, stop_found = apply_stopping_strings(reply, all_stop_strings)
        if escape_html:
            reply = html.escape(reply)

        if is_stream:
            cur_time = time.time()

            # Limit number of tokens/second to make text readable in real time
            if state['max_tokens_second'] > 0:
                diff = 1 / state['max_tokens_second'] - (cur_time - last_update)
                if diff > 0:
                    time.sleep(diff)

                last_update = time.time()
            else:
                if cur_time - last_update > min_update_interval:
                    last_update = cur_time
                    yield reply

            yield reply

        if stop_found or (state['max_tokens_second'] > 0 and variables.stop_everything):
            break

    if not is_chat:
        reply = apply_extensions('output', reply, state)

    yield reply
