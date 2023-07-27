import re


def check_if_domain(input_str: str) -> True | False:
    domain_pattern = r'^([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$'
    if re.match(domain_pattern, input_str):
        return True
    return False

