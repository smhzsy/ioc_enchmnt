import re


def check_if_md5(input_str: str) -> True | False:
    """
    Checks if the input is a MD5 or not.
    :param input_str: String to check.
    :return: True or False
    """
    md5_pattern = r"^[a-fA-F0-9]{32}$"
    if re.match(md5_pattern, input_str):
        return True
    return False
