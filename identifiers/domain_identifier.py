import re


def check_if_domain(input_str: str) -> True | False:
    """
    Checks if the input is a domain or not.
    :param input_str: String to check.
    :return: True or False
    """
    domain_pattern = r"^([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$"
    if re.match(domain_pattern, input_str):
        return True
    return False
