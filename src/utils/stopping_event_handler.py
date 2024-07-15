import pprint

from functools import partial
from jinja2.sandbox import ImmutableSandboxedEnvironment
from chat_logic.prompt_handlers.get_generation_prompt import get_generation_prompt
from utils.logging_colors import logger
from configs import variables, arguments

# Copied from the Transformers library
jinja_env = ImmutableSandboxedEnvironment(trim_blocks=True, lstrip_blocks=True)

def stop_everything_event():
    variables.stop_everything = True

def get_stopping_strings(state):
    stopping_strings = []
    renderers = []

    if state['mode'] in ['instruct', 'chat-instruct']:
        template = jinja_env.from_string(state['instruction_template_str'])
        renderer = partial(template.render, add_generation_prompt=False)
        renderers.append(renderer)

    if state['mode'] in ['chat', 'chat-instruct']:
        template = jinja_env.from_string(state['chat_template_str'])
        renderer = partial(template.render, add_generation_prompt=False, name1=state['name1'], name2=state['name2'])
        renderers.append(renderer)

    for renderer in renderers:
        prefix_bot, suffix_bot = get_generation_prompt(renderer, impersonate=False)
        prefix_user, suffix_user = get_generation_prompt(renderer, impersonate=True)

        stopping_strings += [
            suffix_user + prefix_bot,
            suffix_user + prefix_user,
            suffix_bot + prefix_bot,
            suffix_bot + prefix_user,
        ]

    # Try to find the EOT token
    for item in stopping_strings.copy():
        item = item.strip()
        if item.startswith("<") and ">" in item:
            stopping_strings.append(item.split(">")[0] + ">")
        elif item.startswith("[") and "]" in item:
            stopping_strings.append(item.split("]")[0] + "]")

    if 'stopping_strings' in state and isinstance(state['stopping_strings'], list):
        stopping_strings += state.pop('stopping_strings')

    # Remove redundant items that start with another item
    result = [item for item in stopping_strings if not any(item.startswith(other) and item != other for other in stopping_strings)]
    result = list(set(result))

    if arguments.args.verbose:
        logger.info("STOPPING_STRINGS=")
        pprint.PrettyPrinter(indent=4, sort_dicts=False).pprint(result)
        print()

    return result


def apply_stopping_strings(reply, all_stop_strings):
    stop_found = False
    for string in all_stop_strings:
        idx = reply.find(string)
        if idx != -1:
            reply = reply[:idx]
            stop_found = True
            break

    if not stop_found:
        # If something like "\nYo" is generated just before "\nYou:"
        # is completed, trim it
        for string in all_stop_strings:
            for j in range(len(string) - 1, 0, -1):
                if reply[-j:] == string[:j]:
                    reply = reply[:-j]
                    break
            else:
                continue

            break

    return reply, stop_found
