from enums import InputType
from identifiers import domain_identifier, ip_identifier, url_identifier
from identifiers.hash_types import md5_identifier, sha1_identifier, sha256_identifier


def identify_input_type(input_str: str) -> InputType | None:
    if domain_identifier.check_if_domain(input_str):
        return InputType.DOMAIN
    elif url_identifier.check_if_url(input_str):
        return InputType.URL
    elif ip_identifier.check_if_ip(input_str):
        return InputType.IP
    elif md5_identifier.check_if_md5(input_str):
        return InputType.MD5_HASH
    elif sha1_identifier.check_if_sha1(input_str):
        return InputType.SHA1_HASH
    elif sha256_identifier.check_if_sha256(input_str):
        return InputType.SHA256_HASH

    return None
