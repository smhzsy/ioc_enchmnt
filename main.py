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
from enchmnt_modules.hash.hybrid_analysis_hash_enchmnt import get_hyan_hash_info_async
from enchmnt_modules.hash.threatfox_hash_enchmnt import search_hash_threatfox_async
from enchmnt_modules.common.vt_comm_enchmnt import get_virustotal_info_async
from enchmnt_modules.hash.yaraify_enchmnt import yara_hash_lookup_async
from enchmnt_modules.ip.mg_ip_lookup import mg_ip_lookup_async
from enchmnt_modules.ip.shodan_ip_lookup import shodan_lookup_async
from enchmnt_modules.url.urlvoid_lookup import search_apivoid_url_async
from enchmnt_modules.url.vt_url_enchmnt import get_virustotal_url_info_async
from enums import InputType
from input_identify import identify_input_type

logger_config.configure_logging()
logger = logger_config.get_logger()


async def router(ioc: str):
    """
    BU YAPIYI DİNAMİK HALE GETİR.
    :param ioc:
    :return:
    """
    create_tables()
    type = identify_input_type(ioc)
    result_list = []
    info_list = []
    if type == InputType.URL:
        await search_indicator_in_alienvault_async(type, ioc, result_list)
        await search_in_bd_repo_async(ioc, result_list)
        await get_iq_info_async(ioc, result_list)
        await search_ioc_threatfox_async(ioc, result_list)
        await search_apivoid_url_async(ioc, result_list)
        await get_virustotal_url_info_async(ioc, result_list)
        await whois_lookup_async(ioc, info_list)
        await get_location_async(ioc, info_list)

    elif type == InputType.IP:
        await search_indicator_in_alienvault_async(type, ioc, result_list)
        await search_in_bd_repo_async(ioc, result_list)
        await get_iq_info_async(ioc, result_list)
        await search_ioc_threatfox_async(ioc, result_list)
        await whois_lookup_async(ioc, info_list)
        await get_virustotal_info_async(type, ioc, result_list)
        await get_location_async(ioc, info_list)
        await mg_ip_lookup_async(ioc, result_list)
        await shodan_lookup_async(ioc, result_list)
        await get_urlscan_info_async(type, ioc, result_list)
    elif (
            type == InputType.MD5_HASH
            or type == InputType.SHA1_HASH
            or type == InputType.SHA256_HASH
    ):
        await search_indicator_in_alienvault_async(type, ioc, result_list)
        await search_in_bd_repo_async(ioc, result_list)
        await get_iq_info_async(ioc, result_list)
        await search_ioc_threatfox_async(ioc, result_list)
        await get_hyan_hash_info_async(ioc, result_list)
        await search_hash_threatfox_async(ioc, result_list)
        await get_virustotal_info_async(type, ioc, result_list)
        await yara_hash_lookup_async(ioc, result_list)
    elif type == InputType.DOMAIN:
        await search_indicator_in_alienvault_async(type, ioc, result_list)
        await search_in_bd_repo_async(ioc, result_list)
        await get_iq_info_async(ioc, result_list)
        await search_ioc_threatfox_async(ioc, result_list)
        await whois_lookup_async(ioc, info_list)
        await get_location_async(ioc, info_list)
        await get_virustotal_info_async(type, ioc, result_list)
        await mg_domain_lookup_async(ioc, result_list)
        await get_urlscan_info_async(type, ioc, result_list)
    else:
        logger.info("IoC Input Type Incorrect.")


async def main(ioc: str):
    await router(ioc)
