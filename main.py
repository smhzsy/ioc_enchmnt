import logger_config
from database_files.table_creator import create_tables
from enchmnt_modules.common.alienvault_enchmnt import (
    search_indicator_in_alienvault_async,
)
from enchmnt_modules.common.brandefense_db_lookup import search_in_bd_repo_async
from enchmnt_modules.common.inquest_lookup import get_iq_info_async
from enchmnt_modules.common.location_finder import get_location_async
from enchmnt_modules.common.threatfox_lookup import search_ioc_threatfox_async
from enchmnt_modules.common.urlscan_enchmnt import get_urlscan_info_async
from enchmnt_modules.common.whois_lookup import whois_lookup_async
from enchmnt_modules.domain.mg_domain_lookup import mg_domain_lookup_async
from enchmnt_modules.domain.vt_domain_enchmnt import get_virustotal_domain_info_async
from enchmnt_modules.hash.hybrid_analysis_hash_enchmnt import get_hyan_hash_info_async
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

logger_config.configure_logging()
logger = logger_config.get_logger()


async def router(ioc: str):
    create_tables()
    type = identify_input_type(ioc)
    if type == InputType.URL:
        await search_indicator_in_alienvault_async("url", ioc, "url_table")
        await search_in_bd_repo_async(ioc, "url_table")
        await get_iq_info_async(ioc, "url_table")
        await search_ioc_threatfox_async(ioc, "url_table")
        await search_apivoid_url_async(ioc)
        await whois_lookup_async(ioc, "url_table")
        await get_location_async(ioc, "url_table")
        await get_virustotal_url_info_async(ioc)
    elif type == InputType.IP:
        await search_indicator_in_alienvault_async("IPv4", ioc, "ip_table")
        await search_in_bd_repo_async(ioc, "ip_table")
        await get_iq_info_async(ioc, "ip_table")
        await search_ioc_threatfox_async(ioc, "ip_table")
        await whois_lookup_async(ioc, "ip_table")
        await get_virustotal_ip_info_async(ioc)
        await get_location_async(ioc, "ip_table")
        await mg_ip_lookup_async(ioc)
        await shodan_lookup_async(ioc)
        await get_urlscan_info_async("ip", ioc, "ip_table")
    elif (
        type == InputType.MD5_HASH
        or type == InputType.SHA1_HASH
        or type == InputType.SHA256_HASH
    ):
        await search_indicator_in_alienvault_async("file", ioc, "hash_table")
        await search_in_bd_repo_async(ioc, "hash_table")
        await get_iq_info_async(ioc, "hash_table")
        await search_ioc_threatfox_async(ioc, "hash_table")
        await get_hyan_hash_info_async(ioc)
        await search_hash_threatfox_async(ioc)
        await get_virustotal_hash_info_async(ioc)
        await yara_hash_lookup_async(ioc)
    elif type == InputType.DOMAIN:
        await search_indicator_in_alienvault_async("domain", ioc, "domain_table")
        await search_in_bd_repo_async(ioc, "domain_table")
        await get_iq_info_async(ioc, "domain_table")
        await search_ioc_threatfox_async(ioc, "domain_table")
        await whois_lookup_async(ioc, "domain_table")
        await get_location_async(ioc, "domain_table")
        await get_virustotal_domain_info_async(ioc)
        await mg_domain_lookup_async(ioc)
        await get_urlscan_info_async("domain", ioc, "domain_table")
    else:
        logger.info("IoC Input Type Incorrect.")


async def main(ioc: str):
    await router(ioc)
