# Q15: Count Crawled HTML Files

## Task

SiteScout crawls and stores HTML files in alphabetized folders. The objective is to estimate the workload by counting how many stored `.html` files begin with letters between `H` and `V` (inclusive) starting from the base URL: `https://sanand0.github.io/tdsdata/crawl_html/`

---

## Requirements

* Crawl the given URL and all its subdirectories recursively.
* Identify all `.html` files discovered across all accessible pages.
* Count the files whose names begin with a letter from `H` to `V` (case-insensitive).
* The final result should be a single integer representing the total count.

---

## Approach

### 1. Recursive Web Crawling
A script was written to recursively fetch the initial webpage and any subsequently discovered pages using Python's `urllib` and parse the HTML content using `BeautifulSoup`. 

### 2. Link Extraction & Navigation
The script iterates through all hyperlink (`<a>`) tags:
- If a link points to a relative path on the same server, the script recursively requests and crawls that URL, maintaining a `visited` set to avoid infinite loops.
- All discovered `.html` URLs are added to a `files_found` track set.

### 3. Case-Insensitive Filtering
Once all unique `.html` file paths are collected, the script extracts the actual file name from the URL using `unquote` (to handle any URL-encoded characters). It then checks the first character `file_name[0].upper()` to see if it alphabetically falls between `'H'` and `'V'`. 

---

## Code

**Script:** [`solve.py`](./solve.py)

```python
import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote

base_url = 'https://sanand0.github.io/tdsdata/crawl_html/'
visited = set()
files_found = set()

def crawl(url):
    if url in visited:
        return
    visited.add(url)
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html = response.read()
    except Exception as e:
        print(f'Error fetching {url}: {e}')
        return
        
    soup = BeautifulSoup(html, 'html.parser')

    for a in soup.find_all('a'):
        href = a.get('href')
        if not href or href.startswith('#') or href.startswith('javascript:'):
            continue
        if href == '../' or href == '/': 
            continue
            
        full_url = urljoin(url, href).split('#')[0]

        if not full_url.startswith(base_url):
            continue
        
        if full_url not in visited:
            if full_url.endswith('.html'):
                files_found.add(full_url)
            crawl(full_url)

if __name__ == '__main__':
    crawl(base_url)
    
    count = 0
    for file_url in files_found:
        file_name = unquote(file_url.split('/')[-1])
        if 'H' <= file_name[0].upper() <= 'V':
            count += 1
            
    print(count)
```

---

## Verification

```bash
python solve.py
```

| Metric | Value |
|---|---|
| Total matching HTML files | 67 |

---

## Submission

**Your Answer:**
```
67
```
