import re


def check_if_sha256(input_str: str) -> True | False:
    sha256_pattern = r"^[a-fA-F0-9]{64}$"
    if re.match(sha256_pattern, input_str):
        return True
    return False
