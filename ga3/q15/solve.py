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
        # check if name starts with H to V inclusive
        if 'H' <= file_name[0].upper() <= 'V':
            count += 1
            
    print(count)
