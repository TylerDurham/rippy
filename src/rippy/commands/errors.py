def E_NO_ARGS():
    return ValueError("Invalid input: no arguments specified.")


def E_INIT_TITLE_WITH_READ():
    return ValueError("Invalid input: title should not be used with read.")


def E_INIT_SEARCH_NO_READ_OR_TITLE():
    return ValueError(
        "Invalid input: `--search` should be used with either `title` or `--read`."
    )
