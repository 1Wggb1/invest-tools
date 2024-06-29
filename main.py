from src.invest.investidor10_invest import Investidor10Invest
import os

if __name__ == "__main__":
    ticker = os.environ['TICKER']
    ticker_diff = os.environ['TICKER_DIFF']
    days_ago = os.environ['DAYS_AGO']

    Investidor10Invest(ticker, float(ticker_diff), days_ago).find_ticker_with_diff()
