import requests
from lxml import html
from datetime import datetime

headers = {
    'Host': 'www.r7.com',
    'Sec-Ch-Ua': '"Chromium";v="131", "Not_A Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Accept-Language': 'pt-BR,pt;q=0.9',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Priority': 'u=0, i',
    'Connection': 'keep-alive',
}

def extract_date_from_href(href):
    parts = href.split('/')
    if len(parts) >= 5:
        year = parts[-4]
        month = parts[-3]
        day = parts[-2]

        if not year.isdigit():
            year = parts[-3]
            month = parts[-2]
            day = '00'

        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            today = datetime.now()
            year = str(today.year)
            month = str(today.month).zfill(2)
            day = str(today.day).zfill(2)
        return f"{day}-{month}-{year}"

    today = datetime.now()
    year = str(today.year)
    month = str(today.month).zfill(2)
    day = str(today.day).zfill(2)
    return f"{day}-{month}-{year}"

def scrape():
    url = 'https://www.r7.com/'
    response = requests.get(url, headers=headers)

    html_content = response.content
    tree = html.fromstring(html_content)

    noticias = []
    links = tree.xpath('//a')
    for a in links:
        href = a.get('href')
        title = a.get('title')
        date_info = extract_date_from_href(href)
        current_time = datetime.now().strftime("%H:%M:%S")
        portal = 'R7'

        if href and title and href.startswith("https"):
            noticias.append({
                "titulo": title,
                "link": href,
                "data": date_info,
                "hora": current_time,
                "portal": portal,
            })
    return noticias