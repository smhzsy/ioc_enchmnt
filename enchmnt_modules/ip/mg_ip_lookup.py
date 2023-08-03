import requests


def mg_ip_lookup(ip_address):
    try:
        url = f"https://check.mertcan.dev/check.php?ip={ip_address}"
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        return json_data
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)
        return None
    except ValueError as e:
        print("Error parsing JSON response:", e)
        return None


json_response = mg_ip_lookup("8.8.8.8")
if json_response:
    print(json_response)
