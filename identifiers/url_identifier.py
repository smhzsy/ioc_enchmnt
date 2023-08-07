import re


def check_if_url(input_str: str) -> True | False:
    """
    Checks if the input is a URL or not.
    :param input_str: String to check.
    :return: True or False
    """
    url_pattern = r"^(http[s]?:\/\/)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(\/.*)?$"
    if re.match(url_pattern, input_str):
        return True
    return False
