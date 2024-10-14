import requests


def lambda_handler(event, context):
    job_site_url = event.get("url", None)
    print(event)
    response = requests.get(job_site_url)
    html_content = response.text
    response = requests.get("https://checkip.amazonaws.com")
    ip_address = response.text.strip()
    print(f"Outbound IP: {ip_address}")

    return {
        "html_content": html_content,
        "ip_address": ip_address,
    }
