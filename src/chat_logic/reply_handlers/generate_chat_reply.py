from chat_logic.common_handlers.chatbot_wrapper import chatbot_wrapper

def generate_chat_reply(text, state, regenerate=False, _continue=False, loading_message=True, for_ui=False):
    if regenerate or _continue:
        text = ''
        history = state['history']
        if (len(history['visible']) == 1 and not history['visible'][0][0]) or len(history['internal']) == 0:
            yield history
            return

    yield from chatbot_wrapper(
        text,
        state,
        regenerate=regenerate,
        _continue=_continue,
        loading_message=loading_message,
        for_ui=for_ui,
    )

