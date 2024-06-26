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
    def get_key_or_default(value, field: str):
        if isinstance(value, dict):
            return value.get(field)
        return ""

    @staticmethod
    def parse_results_to_json(results):
        return {} if not results else json.loads(results)

    def find_unit_composition(self, ticker):
        form_data = {
            'ticker': (None, ticker),
            'type': (None, -10000),
        }
        headers = {
            "User-Agent": Invest.FAKE_AGENT_HEADER.get("User-Agent"),
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-fetch-dest": "empty",
            "x-requested-with": "XMLHttpRequest",
            "sec-ch-ua-platform": "Windows",
            "origin": "https://statusinvest.com.br",
        }
        content = requests.post(StatusInvest.STATUS_INVEST_URL, headers=headers, files=form_data).content
        print(f"{content}")
        return Invest.parse_results_to_json(content)

    class UNIT_COMPOSITION(Enum):
        ALUP11 = {"UNIT": "ALUP11", "ON": 1, "PN": 2}
        BRBI11 = {"UNIT": "BRBI11", "ON": 1, "PN": 2}
        BPAC11 = {"UNIT": "BPAC11", "ON": 1, "PN": 2}
        ENGI11 = {"UNIT": "ENGI11", "ON": 1, "PN": 4}
        IGTI11 = {"UNIT": "IGTI11", "ON": 1, "PN": 2}
        KLBN11 = {"UNIT": "KLBN11", "ON": 1, "PN": 4}
        PPLA11 = {"UNIT": "PPLA11", "ON": 1, "PN": 2}
        RNEW11 = {"UNIT": "RNEW11", "ON": 1, "PN": 2}
        RBNS11 = {"UNIT": "RBNS11", "ON": 1, "PN": 2}
        SAPR11 = {"UNIT": "SAPR11", "ON": 1, "PN": 4}
        SANB11 = {"UNIT": "SANB11", "ON": 1, "PN": 1}
        TAEE11 = {"UNIT": "TAEE11", "ON": 1, "PN": 2}

        @classmethod
        def get_value(cls, ticker: str):
            for enum_option in cls.values():
                if enum_option.name == ticker.upper():
                    return enum_option
            return None

        @classmethod
        def values(cls):
            return list(cls)

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
            return list(cls)

        @classmethod
        def values_except(cls, exclusive_value):
            values = cls.values()
            values.remove(exclusive_value)
            return values
