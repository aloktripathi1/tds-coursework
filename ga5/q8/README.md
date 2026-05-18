# Q8: 21-Day Exponential Moving Average (EMA)

## Task
Given ~126 trading days of daily closing prices for 5 tickers (`AAPL`, `MSFT`, `GOOGL`, `AMZN`, `META`), compute the **21-day EMA** for each ticker and identify which ticker has the **highest EMA value on the last date** in the dataset.

---

## Requirements
* Use `ewm(span=21, adjust=False)` — matches the standard recursive textbook EMA formula
* Compute EMA **per ticker** independently (groupby)
* Report EMA value rounded to 2 decimal places and the ticker symbol
* EMA value accepted within ±5%

---

## Approach

### 1. Load Data
Read `stock_prices.csv` — long format with columns `Date`, `Ticker`, `Close_Price`.

### 2. Compute EMA Per Ticker
Use `groupby("Ticker").transform()` so each ticker's EMA is calculated independently and written back into the original DataFrame as a new column.

### 3. Isolate Last Date
Filter to only the rows where `Date == df["Date"].max()` — one row per ticker on the final trading day.

### 4. Find the Winner
Use `idxmax()` to locate the row with the highest `EMA_21` and retrieve its ticker symbol.

---

## Code

**Script:** [`solve.py`](./solve.py)

```python
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
```

---

## Verification

```bash
python solve.py
```

| Ticker | EMA_21 (last day) |
|--------|-------------------|
| **AAPL** | **318.20** ← highest |
| META | 250.99 |
| MSFT | 231.48 |
| AMZN | 216.87 |
| GOOGL | 133.49 |

| Metric | Value |
|--------|-------|
| Last date in dataset | 2025-06-25 |
| Winning ticker | AAPL |
| EMA value | 318.20 |

---

## Submission

**Your Answer:**
```
318.20, AAPL
```
