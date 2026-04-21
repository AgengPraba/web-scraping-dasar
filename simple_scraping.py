from pathlib import Path
import requests
from bs4 import BeautifulSoup
import csv

response = requests.get('https://www.scrapethissite.com/pages/simple/')
soup = BeautifulSoup(response.text, 'html.parser')

country_blocks = soup.find_all('div', class_='country')

print(f'Found {len(country_blocks)} country blocks.')
print('First country block:')
print(country_blocks[0])

results = []

for block in country_blocks:
    country_name = block.find('h3', class_='country-name').text.strip()
    capital = block.find('span', class_='country-capital').text.strip()
    population = block.find('span', class_='country-population').text.strip()
    area = block.find('span', class_='country-area').text.strip()
    
    results.append({
        'name': country_name,
        'capital': capital,
        'population': population,
        'area': area
    })

# buat folder jika belum ada
Path("data").mkdir(parents=True, exist_ok=True)

with open('data/countries.csv', 'w', newline='', encoding='utf-8') as csv_file:
    fieldnames = ['name', 'capital', 'population', 'area']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for country in results:
        writer.writerow(country)