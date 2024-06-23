import json
from typing import Final

from src.invest.invest import Invest
from src.invest.repository.file_repository import FileResultRepository
from src.invest.repository.file_writter import FileWritter


class Investidor10Invest(Invest):
    INVESTIDOR_10_URL: Final = f"https://investidor10.com.br/api/cotacoes/acao/chart"
    REPOSITORY_FILE_NAME: Final = "/investidor10/found_results.json"
    
    def __init__(self):
        self.repository = FileResultRepository(Investidor10Invest.REPOSITORY_FILE_NAME, FileWritter())
        
    def cotation(self, ticker, cotation_days_ago):
        result = self.search(Investidor10Invest.INVESTIDOR_10_URL + f"/{ticker}/{cotation_days_ago}/true/real")
        real_money_cotation = result["real"]
        self.repository.persist_all(json.dumps(real_money_cotation))