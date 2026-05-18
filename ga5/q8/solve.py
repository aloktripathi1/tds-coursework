import pandas as pd

df = pd.read_csv("stock_prices.csv")

df["EMA_21"] = df.groupby("Ticker")["Close_Price"].transform(
    lambda x: x.ewm(span=21, adjust=False).mean()
)

last_date = df["Date"].max()
last_day  = df[df["Date"] == last_date]
winner    = last_day.loc[last_day["EMA_21"].idxmax(), "Ticker"]
ema_val   = last_day["EMA_21"].max()

print(f"{ema_val:.2f}, {winner}")
