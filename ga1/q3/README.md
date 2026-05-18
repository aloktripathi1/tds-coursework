# Q3: POST HTTP requests with uv

## Task
Install `uv` (a fast Python package and project manager) and use it to make a POST HTTP request to httpbin.org with JSON payload containing email and request_id.

### Requirements
- Install uv using the official installation script
- Use HTTPie via uv to POST JSON data to https://httpbin.org/post
- Payload must contain: `email=your-student-id` and `request_id=30e79164`
- Return only the JSON response body (not HTTP headers)

## Approach
1. **Install uv**: Run the official installation script from astral.sh
2. **Use HTTPie**: Leverage uv's ability to run tools without installation using `--with` flag
3. **POST JSON**: Use HTTPie's `--json` flag to send data as JSON
4. **Body Only**: Use `--body` flag to return only the JSON response

## Commands

### Install uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Make POST Request
```bash
uv run --with httpie -- http --json --body POST https://httpbin.org/post email=your-student-id request_id=30e79164
```

## Response
```json
{
    "args": {},
    "data": "{\"email\": \"your-student-id\", \"request_id\": \"30e79164\"}",
    "files": {},
    "form": {},
    "headers": {
        "Accept": "application/json, */*;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Content-Length": "69",
        "Content-Type": "application/json",
        "Host": "httpbin.org",
        "User-Agent": "HTTPie/3.2.4",
        "X-Amzn-Trace-Id": "Root=1-6963ae7a-75f6a95205802c2c11b16328"
    },
    "json": {
        "email": "your-student-id",
        "request_id": "30e79164"
    },
    "origin": "4.240.18.227",
    "url": "https://httpbin.org/post"
}
```

## Implementation Details
- **Tool**: uv (fast Python package and project manager)
- **HTTP Client**: HTTPie (user-friendly HTTP client)
- **Method**: POST with JSON content type
- **Verification**: Server echoes back the payload in the `json` field
- **No Installation**: HTTPie runs via uv without permanent installation
