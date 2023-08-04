import re


def check_if_md5(input_str: str) -> True | False:
    md5_pattern = r"^[a-fA-F0-9]{32}$"
    if re.match(md5_pattern, input_str):
        return True
    return False
