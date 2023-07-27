import whois

def whois_lookup(domain):
    try:
        w = whois.whois(domain)
        print("=== WHOIS Bilgileri ===")
        print("Domain Adı: ", w.domain_name)
        print("Sunucu Adı: ", w.name_servers)
        print("Oluşturulma Tarihi: ", w.creation_date)
        print("Son Güncelleme Tarihi: ", w.updated_date)
        print("Bitiş Tarihi: ", w.expiration_date)
        print("Registrar: ", w.registrar)
        print("Sahip (Owner): ", w.name)
        print("Sahip E-posta: ", w.emails)
        print("Sahip Telefon: ", w.phone)
        print("Sahip Adres: ", w.address)
        print("=== Diğer Bilgiler ===")
        print(w)
    except Exception as e:
        print("Hata: ", str(e))