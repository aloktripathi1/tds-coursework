# Q5: Multiple Linear Regression with Excel Data Analysis ToolPak

## Task

Fit a multiple linear regression model on 200 housing records and predict the price for:

| Area_SqFt | Bedrooms | Age_Years | Distance_City_Center_Km |
|-----------|----------|-----------|------------------------|
| 1800 | 3 | 10 | 5 |

---

## Approach

Used `sklearn.linear_model.LinearRegression` (OLS) — identical outputs to Excel ToolPak Regression.

**Coefficients:**
| Variable | Coefficient |
|---|---|
| Intercept | (fitted) |
| Area_SqFt | 184.338 |
| Bedrooms | … |
| Age_Years | … |
| Distance_City_Center_Km | … |

**Prediction formula:**
```
Price = Intercept
      + 184.338 × 1800
      + Coef_Bedrooms × 3
      + Coef_Age × 10
      + Coef_Distance × 5
```

---

## Execution

```bash
python -c "
import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv('housing_data.csv')
X = df[['Area_SqFt', 'Bedrooms', 'Age_Years', 'Distance_City_Center_Km']]
y = df['Price']
model = LinearRegression().fit(X, y)
print(model.predict([[1800, 3, 10, 5]])[0])
"
```

---

## Submission

**Your Answer:**
```
469529.96
```
