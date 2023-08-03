from enchmnt_modules.common.alienvault_enchmnt import \
    search_indicator_in_alienvault_async
from enchmnt_modules.common.brandefense_db_lookup import search_in_bd_repo_async
from enchmnt_modules.common.inquest_lookup import get_iq_info_async
from enchmnt_modules.common.location_finder import get_location_async
from enchmnt_modules.common.threatfox_lookup import search_ioc_threatfox_async
from enchmnt_modules.common.whois_lookup import whois_lookup_async
from enchmnt_modules.domain.mg_domain_lookup import mg_domain_lookup_async
from enchmnt_modules.domain.vt_domain_enchmnt import get_virustotal_domain_info_async
from enchmnt_modules.hash.hybrid_analysis_hash_enchmnt import \
    get_hyan_hash_info_async
from enchmnt_modules.hash.threatfox_hash_enchmnt import search_hash_threatfox_async
from enchmnt_modules.hash.vt_hash_enchmnt import get_virustotal_hash_info_async
from enchmnt_modules.hash.yaraify_enchmnt import yara_hash_lookup_async
from enchmnt_modules.ip.mg_ip_lookup import mg_ip_lookup_async
from enchmnt_modules.ip.shodan_ip_lookup import shodan_lookup_async
from enchmnt_modules.ip.vt_ip_enchmnt import get_virustotal_ip_info_async
from enchmnt_modules.url.urlvoid_lookup import search_apivoid_url_async
from enchmnt_modules.url.vt_url_enchmnt import get_virustotal_url_info_async
from enums import InputType
from input_identify import identify_input_type


def router(ioc: str):
    type = identify_input_type(ioc)
    if type == InputType.URL:
        print("url")
        print(search_indicator_in_alienvault_async("url", ioc))
        print(search_in_bd_repo_async(ioc))
        print(get_iq_info_async(ioc))
        print(search_ioc_threatfox_async(ioc))
        print(search_apivoid_url_async(ioc))
        print(whois_lookup_async(ioc))
        print(get_location_async(ioc))
        print(get_virustotal_url_info_async(ioc))
    elif type == InputType.IP:
        print("ip")
        print(search_indicator_in_alienvault_async("IPv4", ioc))
        print(search_in_bd_repo_async(ioc))
        print(get_iq_info_async(ioc))
        print(search_ioc_threatfox_async(ioc))
        print(whois_lookup_async(ioc))
        print(get_virustotal_ip_info_async(ioc))
        print(get_location_async(ioc))
        print(mg_ip_lookup_async(ioc))
        print(shodan_lookup_async(ioc))
    elif type == InputType.MD5_HASH or type == InputType.SHA1_HASH or type == InputType.SHA256_HASH:
        print("hash")
        print(search_indicator_in_alienvault_async("file", ioc))
        print(search_in_bd_repo_async(ioc))
        print(get_iq_info_async(ioc))
        print(search_ioc_threatfox_async(ioc))
        print(get_hyan_hash_info_async(ioc))
        print(search_hash_threatfox_async(ioc))
        print(get_virustotal_hash_info_async(ioc))
        print(yara_hash_lookup_async(ioc))
    elif type == InputType.DOMAIN:
        print("domain")
        print(search_indicator_in_alienvault_async("domain", ioc))
        print(search_in_bd_repo_async(ioc))
        print(get_iq_info_async(ioc))
        print(search_ioc_threatfox_async(ioc))
        print(whois_lookup_async(ioc))
        print(get_location_async(ioc))
        print(get_virustotal_domain_info_async(ioc))
        print(mg_domain_lookup_async(ioc))


router("google.com")
