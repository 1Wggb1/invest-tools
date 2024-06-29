import json
import requests
from enum import Enum

from src.invest.status_invest import StatusInvest


class Invest:
    FAKE_AGENT_HEADER = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}

    def __init__(self):
        print("Starting")

    def search(self, site_url):
        content = requests.get(site_url, headers=Invest.FAKE_AGENT_HEADER).content
        return Invest.parse_results_to_json(content)

    @staticmethod
    def parse_results_to_json(results):
        return {} if not results else json.loads(results)

    def find_unit_composition(self, ticker):
        form_data = {
            'ticker': (None, ticker),
            'type': (None, -10000),
        }
        content = requests.get(StatusInvest.STATUS_INVEST_URL, headers=Invest.FAKE_AGENT_HEADER, files=form_data).content
        return Invest.parse_results_to_json(content)

    class AssetType(Enum):
        ON = 3
        PN = 4
        UNIT = 11

        @classmethod
        def extract_ticker_type(cls, ticker: str):
            if not ticker:
                return ""
            digits = [s for s in ticker if s.isdigit()]
            ticker_type = ""
            for digit in digits:
                ticker_type += digit
            return int(ticker_type) if ticker_type else ""

        @classmethod
        def extract_ticker(cls, ticker: str):
            if not ticker:
                return ""
            letters = [s for s in ticker if not s.isdigit()]
            ticker_letters = ""
            for letter in letters:
                ticker_letters += letter
            return ticker_letters

        @classmethod
        def get_value(cls, value: str):
            ticker_type = cls.extract_ticker_type(value)
            for enum_option in cls.values():
                if enum_option.value == ticker_type:
                    return enum_option
            return None

        @classmethod
        def values(cls):
            return [cls.ON, cls.PN, cls.UNIT]

        @classmethod
        def values_except(cls, exclusive_value):
            values = cls.values()
            values.remove(exclusive_value)
            return values
