import requests


def find_input_in_domains(input_value):
    url = "https://raw.githubusercontent.com/mertcangokgoz/public-disavow-links/main/disavow-links.txt"
    try:
        response = requests.get(url)
        response.raise_for_status()
        domains = response.text.splitlines()

        for domain in domains:
            if input_value.lower() in domain.lower():
                print(f"Input value '{input_value}' found in domain: {domain}")
                return

        print(f"Input value '{input_value}' not found in any domain.")
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)

input_value = "fr"

find_input_in_domains(input_value)
