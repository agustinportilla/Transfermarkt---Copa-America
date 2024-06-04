import urllib
import requests
from bs4 import BeautifulSoup
import pandas as pd

main_url = "https://www.transfermarkt.com/copa-america-2024/teilnehmer/pokalwettbewerb/CAM4/saison_id/2023"

# here we define the headers for the request
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'}

# this request object will integrate your URL and the headers defined above
req = urllib.request.Request(url=main_url, headers=headers)

# calling urlopen this way will automatically handle closing the request
with urllib.request.urlopen(req) as response:
    page_html = response.read()

soup = BeautifulSoup(page_html, 'html.parser')

tbody = soup.find('tbody')
rows = tbody.find_all('tr')
titles = []
link_data = []
for row in rows:
    link_tag = row.find('a', href=True)
    if link_tag and 'title' in link_tag.attrs:
        title = link_tag['title']
        href = link_tag['href']
        link_data.append((title, href))
data = [(club, f"https://www.transfermarkt.com{link}") for club, link in link_data]
df = pd.DataFrame(data, columns=['Club', 'Link'])

data = []
for link in df['Link']:
    my_url = link
    # here we define the headers for the request
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:63.0) Gecko/20100101 Firefox/63.0'}
    # this request object will integrate your URL and the headers defined above
    req = urllib.request.Request(url=my_url, headers=headers)
    # calling urlopen this way will automatically handle closing the request
    with urllib.request.urlopen(req) as response:
        page_html = response.read()
    soup = BeautifulSoup(page_html, 'html.parser')
    tbodies = soup.find_all('tbody')
    second_tbody = tbodies[1]
    rows = second_tbody.find_all('tr')
    # data = []
    for row in rows:
        # Extraer el título (nombre del jugador)
        img_tag = row.find('img', class_='bilderrahmen-fixed lazy lazy')
        if img_tag and 'title' in img_tag.attrs:
            title = img_tag['title']

            # Extraer la posición
            position_tag = row.find('td', class_='hauptlink')
            position = position_tag.find_next('tr').find_next('td').text.strip() if position_tag else 'Unknown'

            # Extraer el valor de mercado
            market_value_tag = row.find('td', class_='rechts hauptlink')
            market_value = market_value_tag.text.strip() if market_value_tag else 'Unknown'

            # Extraer el club
            club_img_tag = row.find_all('img')[-1]  # Asumimos que el último <img> en la fila es el del club
            club = club_img_tag['title'] if club_img_tag and 'title' in club_img_tag.attrs else 'Unknown'

            # Extract Nation
            main = soup.find('main')
            h1 = soup.find('h1', class_="data-header__headline-wrapper data-header__headline-wrapper--oswald")
            country_name = h1.text.strip()

            if market_value != 'Unknown':
                data.append((country_name, title, position, market_value, club))

# Crear un DataFrame con los datos
df = pd.DataFrame(data, columns=['Country', 'Jugador', 'Posición', 'Valor de Mercado', 'Club'])

# Exportar a CSV
df.to_csv('jugadores.csv', index=False)

# Mostrar la tabla
print(df)


