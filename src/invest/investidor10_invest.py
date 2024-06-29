import datetime
import json
import math
from typing import Final

from src.invest.invest import Invest
from src.invest.repository.file_repository import FileResultRepository
from src.invest.repository.file_writter import FileWritter


class Investidor10Invest(Invest):
    INVESTIDOR_10_URL: Final = f"https://investidor10.com.br/api/cotacoes/acao/chart"
    REPOSITORY_FILE_NAME: Final = "/investidor10/found_results.json"

    def __init__(self, ticker, ticker_diff, days_ago):
        self.ticker = ticker
        self.tickets_diff = ticker_diff
        self.days_ago = days_ago
        self.repository = FileResultRepository(Investidor10Invest.REPOSITORY_FILE_NAME, FileWritter())

    def find_ticker_with_diff(self):
        ticker_type = Invest.AssetType.get_value(self.ticker)
        tickets_except_main_ticker = Invest.AssetType.values_except(ticker_type)

        final_result = {}
        final_result[self.ticker] = self.__create_result(self.__find_quote(self.ticker))
        main_ticker_result = final_result[self.ticker]["result"]
        for enum_option in tickets_except_main_ticker:
            other_ticket = f"{Invest.AssetType.extract_ticker(self.ticker)}{enum_option.value}"
            quote = self.__find_quote(other_ticket)
            if quote:
                final_result[other_ticket] = self.__create_result(quote)
                other_ticket_result = final_result[other_ticket]["result"]
                final_result[f"{other_ticket} minus {self.ticker} greater than equals {self.tickets_diff}"] = self.do_find_diff(main_ticker_result, self.ticker, other_ticket_result, other_ticket)

        self.repository.persist_all(json.dumps(final_result))

    def do_find_diff(self, main_result, main_ticker, other_result, other_ticker):
        main_size = len(main_result)
        other_size = len(other_result)
        if main_size != other_size:
            raise Investidor10Invest.InvalidStateException()
        final_result = {}
        for i in range(main_size):
            main_ticker_price = main_result[i]["price"]
            other_ticker_price = other_result[i]["price"]
            price_diff = other_ticker_price - main_ticker_price
            if price_diff >= self.tickets_diff:
                final_result[main_result[i]["created_at"]] = {
                    "price_diff": price_diff,
                    main_ticker: main_result[i],
                    other_ticker: other_result[i],
                }
        return final_result

    class InvalidStateException(Exception):
        pass

    def __find_quote(self, ticker):
        return self.search(Investidor10Invest.INVESTIDOR_10_URL + f"/{ticker}/{self.days_ago}/true/real")

    def __create_result(self, result):
        return {
            "request_date_time": Investidor10Invest.get_formatted_datetime(),
            "quote_days_ago": self.days_ago,
            "result": result["real"]
        }

    @staticmethod
    def get_formatted_datetime():
        now = datetime.datetime.now()
        return now.strftime("%d/%m/%Y %H:%M")
