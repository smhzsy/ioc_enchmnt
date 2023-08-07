import re


def check_if_ip(input_str: str) -> True | False:
    """
    Checks if the input is a IP or not.
    :param input_str: String to check.
    :return: True or False
    """
    ip_pattern = r"^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    if re.match(ip_pattern, input_str):
        return True
    return False
