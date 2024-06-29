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
            "cookie": "suno_checkout_userid=e7405be2-949e-4a33-acdd-dfe40927c6b8; _gcl_au=1.1.1252854532.1718151572; _adasys=a9cf5228-e772-4be0-882f-aa2bc1d86b2f; _ga=GA1.1.1587282974.1718151573; _fbp=fb.2.1718151573397.505485004506150149; messagesUtk=bd6c1874a8c94a6090d46d3ea82f19fc; hubspotutk=1f12b66ebadd5147d1c3c30feaf0846f; _hjSessionUser_1931042=eyJpZCI6ImViZDkzZmE4LTViMTEtNTU3Mi04MDgyLTlkYzUyNGU4YjZmOSIsImNyZWF0ZWQiOjE3MTgxNTE1NzM1MDYsImV4aXN0aW5nIjp0cnVlfQ==; G_ENABLED_IDPS=google; _clck=10epvyr%7C2%7Cfn1%7C0%7C1624; .StatusAdThin=1; __hssrc=1; _cc_id=222506746b5f37107b110adb9e16f450; panoramaId_expiry=1720291090894; panoramaId=122bc3e5e5992d919fda5d0e32c84945a7022beb922f7bc7d02886b489464fb8; panoramaIdType=panoIndiv; _hjSession_1931042=eyJpZCI6IjkwZmJjM2FmLWUyNWUtNDM5Ny04YzNkLWMwMmQ4NDkyODk1ZSIsImMiOjE3MTk2OTIwMzQ0MzgsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjowLCJzcCI6MX0=; cf_clearance=hifK0CyoTfwbvLGQf8ktE4vvu5a7YFQpHcD0POBPpM8-1719692035-1.0.1.1-DTXf2gE12mcLhCtV_e2CDmltika2XSqm56WUXi49e2ETIieAzsNKioRQa_6wEIW6iSl9QnH6oK4m6hqbrwpvMQ; _clsk=fzzgj5%7C1719692035786%7C1%7C0%7Ct.clarity.ms%2Fcollect; __gads=ID=baad7bf25c8213c5:T=1718151583:RT=1719692038:S=ALNI_MbMld40_ogsD0H_ILU7aizn6mIBSA; __gpi=UID=00000a2d037071cf:T=1718151583:RT=1719692038:S=ALNI_MY8zXqOkYgWv2oiHwVRuNbNBOowpg; __eoi=ID=cdc92e4bc2d7c0b0:T=1718151583:RT=1719692038:S=AA-AfjajJjCLn4AVUYML4UeV0eKB; __hstc=176625274.1f12b66ebadd5147d1c3c30feaf0846f.1718151587921.1719686289971.1719692040242.3; __hssc=176625274.1.1719692040242; FCNEC=%5B%5B%22AKsRol-_rmA_vsZWQRdICY86KrJLSbanKnX_gjBG54lgcGTajlijOeZfzPtM_E4ogAsn1mN-_NvNpRj2ck1woxXCdBMGXseZZLRB5NwE8dHS3lgsOEiDBxst5Vo466l2vEjes-7Cz6VyYchy89eBBH3VHY2JxeLkxA%3D%3D%22%5D%5D; _ga_69GS6KP6TJ=GS1.1.1719692033.3.1.1719692048.45.0.0"
        }
        content = requests.get(StatusInvest.STATUS_INVEST_URL, headers=headers, files=form_data).content
        print(f"{content}")
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