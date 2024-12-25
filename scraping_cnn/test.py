import requests
from lxml import html
from datetime import datetime

headers = {
    'Host': 'www.cnnbrasil.com.br',
    'Sec-Ch-Ua': '"Chromium";v="127", "Not)A;Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Accept-Language': 'pt-BR',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Priority': 'u=0, i',
    'Connection': 'keep-alive',
}

url = 'https://www.cnnbrasil.com.br/'
response = requests.get(url, headers=headers)

html_content = response.content
tree = html.fromstring(html_content)

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
    return "Data nao disponivel"

def print_group(title, xpath):
    print(f"\n{'-' * 40}\n{title}\n{'-' * 40}")
    links = tree.xpath(xpath)
    if not links:
        print("Nenhum link encontrado.")
    else:
        for index, link in enumerate(links, start=1):
            href = link.get('href')
            title = link.text_content().strip() if link.text_content() else "Título não disponível"

            if href:
                date_info = extract_date_from_href(href)
            else:
                date_info = "Data não disponível"

            current_time = datetime.now().strftime("%H:%M:%S")
            portal = 'CNN'
            if href and href.startswith("https"):
                print(f"Item {index}: Href: {href}, Title: {title}, Data: {date_info}, Hora: {current_time}, Portal: {portal}")


print_group("Grupo de Teste", '//a')