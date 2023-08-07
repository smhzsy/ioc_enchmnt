from enum import Enum


class InputType(Enum):
    """
    Enums for IoC types.
    """

    DOMAIN = "Domain"
    URL = "URL"
    IP = "IP"
    MD5_HASH = "MD5 Hash"
    SHA1_HASH = "SHA-1 Hash"
    SHA256_HASH = "SHA-256 Hash"
