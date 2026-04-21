from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from pathlib import Path
import pprint
import csv
import sys

def dd(data):
    pprint.pprint(data)
    sys.exit()

# Function to scrape data from Rumah123
def scraper(url, max_pages=5):
    # Configure WebDriver to use headless Firefox
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)

    try:
        all_data = []

        for page in range(1, max_pages + 1):
            separator = '&' if '?' in url else '?'
            page_url = f"{url}{separator}page={page}"
            print(f"Scraping page {page}: {page_url}")

            # Load current pagination URL
            driver.get(page_url)

            try:
                wait = WebDriverWait(driver, timeout=8)
                wait.until(EC.presence_of_element_located((By.ID, 'srp-container')))
            except Exception:
                print("Element srp-container tidak ditemukan. Stop pagination.")
                break

            content = driver.page_source
            soup = BeautifulSoup(content, 'html.parser')
            rumah_cards = soup.select('div[data-test-id^="property-card-"]')

            if not rumah_cards:
                print("Tidak ada listing di halaman ini. Stop pagination.")
                break

            page_data = []
            for rumah in rumah_cards:
                try:
                    nama = rumah.find('h2').text.strip() if rumah.find('h2') else ''
                    harga = rumah.find('div', attrs={'data-name': 'price-info'}).text.strip() if rumah.find('div', attrs={'data-name': 'price-info'}) else ''

                    lokasi= rumah.find('p', class_=['text-left', 'font-medium', 'text-greyText', 'text-sm', 'truncate', 'px-4']).text.strip() if rumah.find('p', class_=['text-left', 'font-medium', 'text-greyText', 'text-sm', 'truncate', 'px-4']) else ''

                    # Gunakan class 'attribute-text' untuk spesifikasi
                    spek_container = rumah.find('div', class_=['flex', 'items-center', 'gap-x-2', 'text-accent', 'font-medium', 'text-sm', 'overflow-x-auto', 'no-scrollbar', '[&>*]:flex-shrink-0'])
                    spek = spek_container.find_all('span', class_='flex')

                    jumlah_kamar_tidur = spek[0].text.strip() if len(spek) > 0 else '0'
                    jumlah_kamar_mandi = spek[1].text.strip() if len(spek) > 0 else '0'
                    jumlah_carport = spek[2].text.strip() if len(spek) > 6 else '0'
                    luas_tanah = spek[3].text.strip() if len(spek) > 0 else ''
                    luas_bangunan = spek[4].text.strip() if len(spek) > 0 else ''

                    page_data.append({
                        'Nama': nama,
                        'Harga': harga,
                        'Lokasi': lokasi,
                        'Jumlah Kamar Tidur': jumlah_kamar_tidur,
                        'Jumlah Kamar Mandi': jumlah_kamar_mandi,
                        'Jumlah Carport': jumlah_carport,
                        'Luas Tanah': luas_tanah,
                        'Luas Bangunan': luas_bangunan,
                    })
                except Exception as e:
                    print(f"Skip card karena error: {e}")
                    continue

            if not page_data:
                print("Tidak ada data valid di halaman ini. Stop pagination.")
                break

            all_data.extend(page_data)
            print(f"Berhasil ambil {len(page_data)} data dari halaman {page}")

        return all_data

    except Exception as e:
        # Print the error message
        print('An error occurred: ', e)
        return []

    finally:
        # Close the WebDriver
        driver.quit()


 
if __name__ == '__main__':
    # Define target URLs

    data = [
        'https://www.rumah123.com/jual/rumah/?q=semarang',
        'https://www.rumah123.com/jual/wonogiri/rumah/',
        'https://www.rumah123.com/jual/cirebon/rumah/'
    ]
 
    all_data = []
    for url in data:
        print(f"Scraping data dari: {url}")
        scraped_data = scraper(url)
        all_data.extend(scraped_data)
        print(f"Jumlah data yang berhasil di-scrape: {len(scraped_data)}")
        print("-" * 50)

    # buat folder jika belum ada
    Path("data").mkdir(parents=True, exist_ok=True)

    # Save data to CSV file
    with open('data/rumah123_data.csv', 'w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['Nama', 'Harga', 'Lokasi', 'Jumlah Kamar Tidur', 'Jumlah Kamar Mandi', 'Jumlah Carport', 'Luas Tanah', 'Luas Bangunan']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for data in all_data:
            writer.writerow(data)