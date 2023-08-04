import re


def check_if_sha1(input_str: str) -> True | False:
    sha1_pattern = r"^[a-fA-F0-9]{40}$"
    if re.match(sha1_pattern, input_str):
        return True
    return False
