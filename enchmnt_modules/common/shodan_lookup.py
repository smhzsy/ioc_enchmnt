import shodan
from dotenv import load_dotenv
import os

load_dotenv()

sh_api_key = os.getenv("SHODAN_API_KEY")


def shodan_lookup(ip):
    try:
        api = shodan.Shodan(sh_api_key)

        host = api.host(ip)

        print("=== Shodan Bilgileri ===")
        print("IP Adresi: ", host['ip_str'])
        print("Ülke: ", host.get('country_name', 'Bilgi Yok'))
        print("Şehir: ", host.get('city', 'Bilgi Yok'))
        print("Organizasyon: ", host.get('org', 'Bilgi Yok'))
        print("ASN: ", host.get('asn', 'Bilgi Yok'))
        print("Açık Portlar: ", host.get('ports', 'Bilgi Yok'))
        print("=== Diğer Bilgiler ===")
        print(host)
    except shodan.APIError as e:
        print("Hata: ", str(e))
