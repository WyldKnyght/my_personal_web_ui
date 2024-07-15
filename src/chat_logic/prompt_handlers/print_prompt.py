
def print_prompt(prompt, max_chars=2000):
    if len(prompt) > max_chars:
        half_chars = max_chars // 2
        hidden_len = len(prompt[half_chars:-half_chars])
        DARK_YELLOW = "\033[38;5;3m"
        RESET = "\033[0m"

        hidden_msg = f"{DARK_YELLOW}[...{hidden_len} characters hidden...]{RESET}"
        print(prompt[:half_chars] + hidden_msg + prompt[-half_chars:])
    else:
        print(prompt)

    print()
