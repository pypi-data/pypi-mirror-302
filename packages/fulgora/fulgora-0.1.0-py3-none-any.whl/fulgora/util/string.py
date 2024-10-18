def trailing_newline(func):
    def wrapper(*args, **kwargs):
        return f"{func(*args, **kwargs)}\n"

    return wrapper


def leading_newline(func):
    def wrapper(*args, **kwargs):
        return f"\n{func(*args, **kwargs)}"

    return wrapper


def trailing_space(func):
    def wrapper(*args, **kwargs):
        return f"{func(*args, **kwargs)} "

    return wrapper
