# Q17: Create a Localtunnel Tunnel

## Task

Create a localtunnel tunnel to a local server that serves `your-student-id`. The tunnel URL should end in `.loca.lt`.

---

## Approach

### Step 1: Local Server

Created a minimal Python HTTP server (`server.py`) on port 3000 that responds to any GET request with the email address in an HTML page:

```python
from http.server import HTTPServer, BaseHTTPRequestHandler

EMAIL = "your-student-id"

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(f"<html><body><h1>{EMAIL}</h1></body></html>".encode("utf-8"))
```

### Step 2: Localtunnel

Exposed the local server via localtunnel:

```powershell
# Terminal 1 — start the server
python server.py

# Terminal 2 — start the tunnel
npx -y localtunnel --port 3000
```

This gives a public URL like `https://free-berries-sin.loca.lt`.

### Step 3: Verifying the Tunnel

Tested the tunnel URL locally with the `bypass-tunnel-reminder` header (which the grader's proxy also sends):

```powershell
Invoke-WebRequest -Uri "https://free-berries-sin.loca.lt" `
  -Headers @{"bypass-tunnel-reminder"="1"} -UseBasicParsing
```

Confirmed — returns HTTP 200 with `aloktripathe@gmail.com` in the body.

---

## Issues & Debugging

### Issue 1: Localtunnel Interstitial (HTTP 511)

Localtunnel's hosted server (`loca.lt`) shows a "Tunnel website ahead!" protection page to new visitors. The grader at `exam.sanand.workers.dev/proxy/` hits this page instead of our content, returning HTTP 511.

**Root cause**: The interstitial is injected by loca.lt's infrastructure (not part of the open-source localtunnel server code). It requires either a cookie or the `bypass-tunnel-reminder` header to skip.

### Issue 2: Grader Proxy Gets Blocked

The grader proxy sends `bypass-tunnel-reminder: 1` as a header. This works **from our machine** but intermittently fails from the grader's Cloudflare Worker. The interstitial protection appears to be applied randomly per subdomain — some tunnel URLs trigger it, some don't.

### Issue 3: Tried Cloudflare Tunnel as Alternative

Set up `cloudflared tunnel --url http://localhost:3000` which created a `.trycloudflare.com` URL with no interstitial. However, the grader **requires** a `.loca.lt` domain and rejects other URLs.

### Issue 4: Tunnel Password

Discovered that the tunnel password is your public IP (fetch from `https://loca.lt/mytunnelpassword`). Submitted it via curl/Python to try unlocking the tunnel globally. The password unlocks access for our IP but the grader uses different IPs (Cloudflare edge network).

---

## Current Status

| Check | Status |
|-------|--------|
| Server running on `localhost:3000` | ✅ |
| Localtunnel URL created | ✅ |
| Email visible in browser | ✅ |
| `bypass-tunnel-reminder` header works from our machine | ✅ |
| Grader proxy consistently bypasses interstitial | ⚠️ Intermittent |

---

## Workaround (per TA guidance)

The interstitial protection is applied **randomly per subdomain**. The fix is to keep restarting the tunnel until you get a "clean" URL:

```powershell
# Restart tunnel for a new URL
npx -y localtunnel --port 3000
# Copy the new .loca.lt URL
# Submit immediately while both terminals are running
```

Test from a different network (e.g. mobile data) before submitting. If the email shows without the protection page, submit right away.

> **Note**: This is a known localtunnel behavior issue, not an implementation problem. The TA confirmed the question is correct and that some URLs randomly trigger abuse protection.

---

## Files

- `server.py` — Python HTTP server serving the email address
- `README.md` — This file
