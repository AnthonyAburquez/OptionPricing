import yfinance as yf
import numpy as np
import math
from scipy.stats import norm

def get_stock_price(ticker):
    stock = yf.Ticker(ticker)
    return stock.history(period='3mo')['Close'][0]

def calculate_annualized_volatility(ticker):
    stock = yf.Ticker(ticker)
    closing_prices = stock.history(period='1Y')['Close']
    log_returns = np.log(closing_prices / closing_prices.shift(1)).dropna()
    
    # Calculate the standard deviation of log returns
    std_dev = log_returns.std()
    
    # Annualize the standard deviation
    annualized_volatility = std_dev * np.sqrt(252)
    
    return annualized_volatility

def BSM(ticker, cur_price, strike, risk_free, T, div) -> int:
    volatility = calculate_annualized_volatility(ticker)
    T = T / 252  # Convert days to years
    d1 = (np.log(cur_price / strike) + (risk_free - div + 0.5 * volatility ** 2) * T) / (volatility * np.sqrt(T))
    d2 = d1 - volatility * np.sqrt(T)
    call_price = cur_price * np.exp(-div * T) * norm.cdf(d1) - strike * np.exp(-risk_free * T) * norm.cdf(d2)
    call_price = round(call_price, 2)
    put_price = strike * np.exp(-risk_free * T) * norm.cdf(-d2) - cur_price * np.exp(-div * T) * norm.cdf(-d1)
    put_price = round(put_price, 2)

    return call_price, put_price
def display(tickers: list):
    for ticker in tickers:
        call_price, put_price = BSM(ticker[0], ticker[1], ticker[2], ticker[3], ticker[4], ticker[5])
        call_price_CAD = round(call_price*ticker[6]*100, 2)
        put_price_CAD = round(put_price**ticker[6]*100, 2)

        print(f"Ticker: {ticker[0]}")
        if(ticker[1] > ticker[2]):
            print("In the Moneny")
        elif (ticker[1] < ticker[2]):
            print("In the Moneny")
        else:  
            print("At the Moneny")

        print(f"Call price: {call_price}")
        print(f"Put price: {put_price}")
        print(f"Total USD (1 Contract) Call: {call_price * 100}")
        print(f"Total USD (1 Contract) Put: {put_price * 100}")
        print(f"Total CAD (1 Contract) Call: {call_price_CAD }")
        print(f"Total CAD (1 Contract) Put: {put_price_CAD }")

        print("------------------------------------------------")



def main():
    # Stock= [ticker, exp_sell_price, strike price, risk free rate, days to expiration, dividend yield]
    tickers = [
        ["AMD", 170, 150, 0.0448, 74, 0, 1.33],
        ["NVDA", 124, 107, 0.0448, 64, 0, 1.33]
    ]

    display(tickers)


if __name__ == "__main__":
    main()