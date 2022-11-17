import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from tabulate import tabulate
import warnings

# warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)

BTC_USD = yf.download('BTC-USD', start='1985-01-01', end='2022-10-30')
BTC_USD.head()

daily_returns = BTC_USD['Adj Close'].pct_change()
daily_volatility = daily_returns.std()

trading_days = 252
# trading_days = 504
# trading_days = 1008
count = 0
price_list = []
last_price = BTC_USD['Adj Close'][-1]

price = last_price * (1 + np.random.normal(0, daily_volatility))
price_list.append(price)

simulations = 100
df = pd.DataFrame()
last_price_list = []
for x in range(simulations):
    count = 0
    price_list = []
    price = last_price * (1 + np.random.normal(0, daily_volatility))
    price_list.append(price)

    for y in range(trading_days):
        if count == 251:
        # if count == 503:
        # if count == 1007:
            break
        price = price_list[count] * (1 + np.random.normal(0, daily_volatility))
        price_list.append(price)
        count += 1

    df[x] = price_list
    last_price_list.append(price_list[-1])

fig, ax = plt.subplots(figsize=(8, 4))
ax.spines[['top', 'right']].set_visible(False)
plt.title('Monte Carlo Simulation: BTC_USD')
ax.plot(df, linewidth=2)
plt.xlabel('Day')
plt.ylabel('Price')
plt.show()


mean_simulated_price = round(np.mean(last_price_list),3)
quantile_5 = np.percentile(last_price_list,5)
quantile_95 = np.percentile(last_price_list,95)

print(tabulate(
    [['Mean Simulated Price', mean_simulated_price], ['Quantile (5%)', quantile_5], ['Quantile (95%)', quantile_95]],
    headers=['BTC_USD', 'Stock Price (USD)'], tablefmt='fancy_grid', stralign='center', numalign='center', floatfmt=".2f"))
