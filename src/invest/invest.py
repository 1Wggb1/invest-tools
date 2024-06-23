import json

import requests


class Invest:
    FAKE_AGENT_HEADER = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}
    
    def __init__(self):
        print("Starting")

    def search(self, site_url):
        content = requests.get(site_url, headers=Invest.FAKE_AGENT_HEADER).content
        return Invest.__parse_results_to_json(content)

    @staticmethod
    def __parse_results_to_json(results):
        return json.loads(results)