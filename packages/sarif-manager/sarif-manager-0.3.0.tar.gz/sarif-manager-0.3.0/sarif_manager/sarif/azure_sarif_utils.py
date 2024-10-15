import sys
import re
import markdown
import requests
from bs4 import BeautifulSoup


def trim_uuid(input_string: str) -> str:
    # Regex pattern to match a UUID (with or without hyphens)
    uuid_pattern = r'[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'

    # Replace the first occurrence of the UUID and the following hyphen with an empty string
    trimmed_string = re.sub(uuid_pattern + r'-?', '', input_string, count=1)

    return trimmed_string.strip()


def create_work_item(
        rule_id: str, issue_title: str, issue_description: str, api_url: str, headers: dict
):
    """
    Create a single work item in Azure DevOps with URLs converted to HTML links.

    Reference: https://learn.microsoft.com/en-us/rest/api/azure/devops/?view=azure-devops-rest-7.2&viewFallbackFrom=azure-devops-rest-5.1

    """
    # Convert Markdown to HTML
    html_description = markdown.markdown(issue_description)

    # Convert URLs into clickable links
    url_pattern = re.compile(
        r'https?://[^\s<>"]+|www\.[^\s<>"]+'
    )
    html_description = url_pattern.sub(
        lambda x: f'<a href="{x.group(0)}">{x.group(0)}</a>', html_description
    )

    soup = BeautifulSoup(html_description, 'html.parser')
    formatted_description = soup.prettify()

    json_data = [
        {"op": "add", "path": "/fields/System.Title", "value": issue_title},
        {"op": "add", "path": "/fields/System.Description", "value": formatted_description},
        {"op": "add", "path": "/fields/System.Tags", "value": "Security Vulnerability"}
    ]
    response = requests.post(api_url, headers=headers, json=json_data)
    if response.status_code == 200:
        response_data = response.json()
        html_url = response_data['_links']['html']['href']
        print(f"Work item created - {rule_id}: {html_url}")
    else:
        print(f"Failed to create work item: {rule_id}")
        sys.exit(1)
