# Q18: FastAPI File Validation Service

A FastAPI service that validates file uploads (type, size, auth) and processes CSV files.

## Endpoint

`POST /upload`

## Validation Rules

1.  **Authentication**: Header `X-Upload-Token-7844: 6johsr3kr8z9t3tq` (401 if missing/wrong)
2.  **File Type**: Only `.csv`, `.json`, `.txt` (400 if invalid)
3.  **File Size**: Max 52KB (413 if exceeded)

## Request

-   Method: `POST`
-   Content-Type: `multipart/form-data`
-   Field: `file`

## Response (Success)

For a valid CSV upload:

```json
{
  "email": "your-student-id",
  "filename": "data.csv",
  "rows": 42,
  "columns": ["id", "name", "value", "category"],
  "totalValue": 19717.28,
  "categoryCounts": {"B":7,"C":10,"D":13,"A":12}
}
```

## Running the Service

```bash
# Install dependencies
pip install -r requirements.txt

# Run server (port 8001 to avoid conflicts)
python main.py
```

## Testing

```bash
python test2.py
```
