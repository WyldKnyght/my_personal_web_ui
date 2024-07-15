
import importlib
import traceback
import gradio as gr

from functools import partial
from inspect import signature
from pathlib import Path

from arguments import args, extensions
from utils import github
from utils.logging_colors import logger
from utils.natural_keys import natural_keys
from variables import settings, default_settings

state = {}
available_extensions = []
setup_called = set()

def apply_settings(extension, name):
    if not hasattr(extension, 'params'):
        return

    for param in extension.params:
        _id = f"{name}-{param}"
        default_settings[_id] = extension.params[param]
        if _id in settings:
            extension.params[param] = settings[_id]


def load_extensions():
    global state, setup_called
    state = {}
    for i, name in enumerate(args.extensions):
        if name in available_extensions:
            if name != 'api':
                logger.info(f'Loading the extension "{name}"')
            try:
                try:
                    extension = importlib.import_module(f"extensions.{name}.script")
                except ModuleNotFoundError:
                    logger.error(f"Could not import the requirements for '{name}'. Make sure to install the requirements for the extension.\n\n* To install requirements for all available extensions, launch the\n  update_wizard script for your OS and choose the B option.\n\n* To install the requirements for this extension alone, launch the\n  cmd script for your OS and paste the following command in the\n  terminal window that appears:\n\nLinux / Mac:\n\npip install -r extensions/{name}/requirements.txt --upgrade\n\nWindows:\n\npip install -r extensions\\{name}\\requirements.txt --upgrade\n")
                    raise

                # Only run setup() and apply settings from settings.yaml once
                if extension not in setup_called:
                    apply_settings(extension, name)
                    if hasattr(extension, "setup"):
                        extension.setup()

                    setup_called.add(extension)

                state[name] = [True, i]
            except Exception:
                logger.error(f'Failed to load the extension "{name}".')
                traceback.print_exc()

# Extension functions that map string -> string
def _apply_string_extensions(function_name, text, state, is_chat=False):
    for extension, _ in iterator():
        if hasattr(extension, function_name):
            func = getattr(extension, function_name)

            # Handle old extensions without the 'state' arg or
            # the 'is_chat' kwarg
            count = 0
            has_chat = False
            for k in signature(func).parameters:
                if k == 'is_chat':
                    has_chat = True
                else:
                    count += 1

            args = [text, state] if count == 2 else [text]
            kwargs = {'is_chat': is_chat} if has_chat else {}
            text = func(*args, **kwargs)

    return text


# Extension functions that map string -> string
def _apply_chat_input_extensions(text, visible_text, state):
    for extension, _ in iterator():
        if hasattr(extension, 'chat_input_modifier'):
            text, visible_text = extension.chat_input_modifier(text, visible_text, state)

    return text, visible_text


# custom_generate_chat_prompt handling - currently only the first one will work
def _apply_custom_generate_chat_prompt(text, state, **kwargs):
    return next(
        (
            extension.custom_generate_chat_prompt(text, state, **kwargs)
            for extension, _ in iterator()
            if hasattr(extension, 'custom_generate_chat_prompt')
        ),
        None,
    )


# Extension that modifies the input parameters before they are used
def _apply_state_modifier_extensions(state):
    for extension, _ in iterator():
        if hasattr(extension, "state_modifier"):
            state = getattr(extension, "state_modifier")(state)

    return state


# Extension that modifies the chat history before it is used
def _apply_history_modifier_extensions(history):
    for extension, _ in iterator():
        if hasattr(extension, "history_modifier"):
            history = getattr(extension, "history_modifier")(history)

    return history


# Extension functions that override the default tokenizer output - The order of execution is not defined
def _apply_tokenizer_extensions(function_name, state, prompt, input_ids, input_embeds):
    for extension, _ in iterator():
        if hasattr(extension, function_name):
            prompt, input_ids, input_embeds = getattr(extension, function_name)(state, prompt, input_ids, input_embeds)

    return prompt, input_ids, input_embeds


# Allow extensions to add their own logits processors to the stack being run.
# Each extension would call `processor_list.append({their LogitsProcessor}())`.
def _apply_logits_processor_extensions(function_name, processor_list, input_ids):
    for extension, _ in iterator():
        if hasattr(extension, function_name):
            result = getattr(extension, function_name)(processor_list, input_ids)
            if type(result) is list:
                processor_list = result

    return processor_list


# Get prompt length in tokens after applying extension functions which override the default tokenizer output
# currently only the first one will work
def _apply_custom_tokenized_length(prompt):
    return next(
        (
            getattr(extension, 'custom_tokenized_length')(prompt)
            for extension, _ in iterator()
            if hasattr(extension, 'custom_tokenized_length')
        ),
        None,
    )


# Custom generate reply handling - currently only the first one will work
def _apply_custom_generate_reply():
    return next(
        (
            getattr(extension, 'custom_generate_reply')
            for extension, _ in iterator()
            if hasattr(extension, 'custom_generate_reply')
        ),
        None,
    )


def _apply_custom_css():
    return ''.join(
        getattr(extension, 'custom_css')()
        for extension, _ in iterator()
        if hasattr(extension, 'custom_css')
    )


def _apply_custom_js():
    return ''.join(
        getattr(extension, 'custom_js')()
        for extension, _ in iterator()
        if hasattr(extension, 'custom_js')
    )

def create_extensions_block():
    if to_display := [
        (extension, name)
        for extension, name in iterator()
        if hasattr(extension, "ui")
        and not (
            hasattr(extension, 'params')
            and extension.params.get('is_tab', False)
        )
    ]:
        with gr.Column(elem_id="extensions"):
            for row in to_display:
                extension, _ = row
                extension.ui()

def create_extensions_tabs():
    for extension, name in iterator():
        if hasattr(extension, "ui") and (hasattr(extension, 'params') and extension.params.get('is_tab', False)):
            display_name = getattr(extension, 'params', {}).get('display_name', name)
            with gr.Tab(display_name, elem_classes="extension-tab"):
                extension.ui()

EXTENSION_MAP = {
    "input": partial(_apply_string_extensions, "input_modifier"),
    "output": partial(_apply_string_extensions, "output_modifier"),
    "chat_input": _apply_chat_input_extensions,
    "state": _apply_state_modifier_extensions,
    "history": _apply_history_modifier_extensions,
    "bot_prefix": partial(_apply_string_extensions, "bot_prefix_modifier"),
    "tokenizer": partial(_apply_tokenizer_extensions, "tokenizer_modifier"),
    'logits_processor': partial(_apply_logits_processor_extensions, 'logits_processor_modifier'),
    "custom_generate_chat_prompt": _apply_custom_generate_chat_prompt,
    "custom_generate_reply": _apply_custom_generate_reply,
    "tokenized_length": _apply_custom_tokenized_length,
    "css": _apply_custom_css,
    "js": _apply_custom_js
}

def apply_extensions(typ, *args, **kwargs):
    if typ not in EXTENSION_MAP:
        raise ValueError(f"Invalid extension type {typ}")

    return EXTENSION_MAP[typ](*args, **kwargs)

def get_available_extensions():
    extensions = sorted(set(map(lambda x: x.parts[1], Path('extensions').glob('*/script.py'))), key=natural_keys)
    extensions = [v for v in extensions if v not in github.new_extensions]
    return extensions

def add_extension(name, last=False):
    if args.extensions is None:
        args.extensions = [name]
    elif last:
        args.extensions = [x for x in args.extensions if x != name]
        args.extensions.append(name)
    elif name not in args.extensions:
        args.extensions.append(name)

# This iterator returns the extensions in the order specified in the command-line
def iterator():
    for name in sorted(state, key=lambda x: state[x][1]):
        if state[name][0]:
            yield getattr(extensions, name).script, name

