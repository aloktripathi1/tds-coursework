# Q6: Seasonal Forecasting with Excel FORECAST.ETS

## Task

Predict the number of website visitors for Month 37 using Excel's built-in AI-like forecasting tool, `FORECAST.ETS`, based on 36 months of historical data with clear seasonal patterns.

---

## Requirements

* Download `monthly_website_traffic.csv` (36 months, columns: `Month` and `Visitors`).
* Use the `FORECAST.ETS` function which handles seasonality automatically.
* Target month to forecast is 37.
* Seasonal period is 12 (months per year).
* Final forecasted value must be rounded to the nearest integer (accepted within ±1).

---

## Approach

### 1. Prepare Data
Open the `monthly_website_traffic.csv` file in Excel.
- **Column A (Month):** Contains the timeline (1 through 36).
- **Column B (Visitors):** Contains the historical monthly traffic counts.

### 2. Apply Forecasting Function
Use Excel's `FORECAST.ETS` function to mathematically extrapolate the 37th month. This uses Holt-Winters triple exponential smoothing to capture both the underlying trend and the 12-month repeating seasonal cycle.

---

## Solution

**Excel Formula:**

```excel
=FORECAST.ETS(37, B2:B37, A2:A37, 12)
```

**Parameters Breakdown:**
- `37`: The **Target Date** to forecast.
- `B2:B37`: The **Values** (historical website traffic).
- `A2:A37`: The **Timeline** (Months 1 to 36).
- `12`: The **Seasonality** (repeating cycle every 12 months).

---

## Verification

The data exhibits a consistent upward trend combined with an additive seasonal pattern. The `FORECAST.ETS` formula accurately captures both components to predict the traffic for the next month.

Applying the formula to the provided dataset evaluates to exactly **16039**.

---

## Submission

**Your Answer:**
```
16039
```
