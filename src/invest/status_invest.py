from typing import Final

class StatusInvest:
    STATUS_INVEST_URL: Final = f"https://statusinvest.com.br/acao/tickerprice"
    REPOSITORY_FILE_NAME: Final = "/statusInvest/found_results.json"

    def __init__(self):
        super().__init__()
