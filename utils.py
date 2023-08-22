import json
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

import requests
from requests.exceptions import ReadTimeout

load_dotenv()
browserless_api_key = os.getenv("BROWSERLESS_API_KEY")
serper_api_key = os.getenv("SERPER_API_KEY")


def search(query, max_article_count):
    url = "https://google.serper.dev/news"

    payload = json.dumps({"q": query})
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    results = json.loads(response.text)["news"]
    title_url_collection = []
    result_len = min(max_article_count, len(results))
    for i in range(result_len):
        title_url_collection.append(
            {
                "title": results[i]["title"],
                "link": results[i]["link"],
            }
        )

    return title_url_collection


def extract_article(url):
    headers = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/json",
    }
    data = {
        "url": url,
    }
    data_json = json.dumps(data)

    post_url = (
        f"https://chrome.browserless.io/content?token={browserless_api_key}"  # noqa
    )

    try:
        response = requests.post(
            post_url,
            headers=headers,
            data=data_json,
            timeout=2,
        )
    except ReadTimeout:
        return "This link failed to provide an article. You can ignore this in your newsletter."

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()

        return text

    else:
        return f"this link failed with status code {response.status_code}. You can ignore this in your newsletter."
