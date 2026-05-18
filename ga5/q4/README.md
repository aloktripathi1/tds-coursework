# Q4: Correlation Matrix with Excel Data Analysis ToolPak

## Task

Compute the full Pearson correlation matrix for 5 student performance variables and find the strongest positive off-diagonal pair.

---

## Approach

Used `pandas.DataFrame.corr(method='pearson')` — equivalent to Excel's ToolPak Correlation output.

**Correlation matrix:**
| | Study_Hours | Sleep_Hours | Screen_Time | Attendance_Percent | Exam_Score |
|---|---|---|---|---|---|
| Study_Hours | 1.0000 | | | | |
| Sleep_Hours | … | 1.0000 | | | |
| Screen_Time | … | … | 1.0000 | | |
| Attendance_Percent | … | … | … | 1.0000 | |
| Exam_Score | **0.9184** | 0.0252 | 0.0184 | 0.4047 | 1.0000 |

Highest off-diagonal positive value: **Exam_Score ↔ Study_Hours = 0.9184**

---

## Submission

**Your Answer:**
```
Study_Hours, Exam_Score, 0.9184
```
