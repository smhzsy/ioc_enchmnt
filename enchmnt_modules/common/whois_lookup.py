import whois

from database_files.add import add_data
from database_files.session import create_session


async def whois_lookup_async(input_ioc, table_name):
    try:
        w = whois.whois(input_ioc)
        session = create_session()
        add_data(session, input_ioc, "whois", str(w), table_name)
    except Exception as e:
        print("Hata: ", str(e))
