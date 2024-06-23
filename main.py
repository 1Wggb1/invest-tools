from src.invest.investidor10_invest import Investidor10Invest
import os

if __name__ == "__main__":
    ticker = os.environ['TICKER']
    days_ago = os.environ['DAYS_AGO']
    
    Investidor10Invest().cotation(ticker, days_ago)