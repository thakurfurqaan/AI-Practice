import requests
import json


def get_ip_address():
    response = requests.get("https://checkip.amazonaws.com")
    ip_address = response.text.strip()
    return ip_address


def scrape(job_site_url):
    response = requests.get(job_site_url)
    html_content = response.text
    return html_content


def lambda_handler(event, context):
    job_site_url = event.get("url", None)
    if not job_site_url:
        job_site_url = event.get("queryStringParameters", None).get("url")

    if job_site_url:
        html_content = scrape(job_site_url)
    else:
        html_content = "No job site url supplied!"

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "html_content": html_content,
                "ip_address": get_ip_address(),
            }
        ),
        "headers": {"Content-Type": "application/json"},
    }
