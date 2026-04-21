from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from pathlib import Path
import json
import pprint
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
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'card-list-section')))
            except Exception:
                print("Element card-list-section tidak ditemukan. Stop pagination.")
                break

            content = driver.page_source
            soup = BeautifulSoup(content, 'html.parser')
            rumah_cards = soup.find_all('div', attrs={'data-test-id': 'card-middle-section'})

            if not rumah_cards:
                print("Tidak ada listing di halaman ini. Stop pagination.")
                break

            page_data = []
            for rumah in rumah_cards:
                try:
                    nama = rumah.find('h2').text.strip() if rumah.find('h2') else ''
                    harga = rumah.find('strong').text.strip() if rumah.find('strong') else ''

                    lokasi_tag = rumah.find('span', recursive=False)
                    lokasi = lokasi_tag.text.strip() if lokasi_tag else ''

                    # Gunakan class 'attribute-text' untuk spesifikasi
                    attribute_texts = rumah.find_all('span', class_='attribute-text')
                    jumlah_kamar_tidur = attribute_texts[0].text.strip() if len(attribute_texts) > 0 else '0'
                    jumlah_kamar_mandi = attribute_texts[1].text.strip() if len(attribute_texts) > 1 else '0'
                    jumlah_carport = attribute_texts[2].text.strip() if len(attribute_texts) > 2 else '0'

                    attribute_infos = rumah.find_all('div', class_='attribute-info')
                    luas_tanah = attribute_infos[0].text.strip() if len(attribute_infos) > 0 else ''
                    luas_bangunan = attribute_infos[1].text.strip() if len(attribute_infos) > 1 else ''

                    page_data.append({
                        'Nama': nama,
                        'Harga': harga,
                        'Lokasi': lokasi,
                        'Jumlah Kamar Tidur': jumlah_kamar_tidur,
                        'Jumlah Kamar Mandi': jumlah_kamar_mandi,
                        'Jumlah Carport': jumlah_carport,
                        'Luas Tanah': luas_tanah,
                        'Luas Bangunan': luas_bangunan,
                        'Page': page,
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
    # Define the URL

    data = [
        'url_rumah_semarang = "https://www.rumah123.com/jual/semarang/rumah/"',
        'url_rumah_jakarta = "https://www.rumah123.com/jual/jakarta/rumah/"',
        'url_rumah_wonogiri = "https://www.rumah123.com/jual/wonogiri/rumah/"',
        'url_rumah_cirebon = "https://www.rumah123.com/jual/cirebon/rumah/"'
    ]
 
    for i in data:
        url = i.split('=')[1].strip().strip('"')
        print(f"Scraping data dari: {url}")
        scraped_data = scraper(url)
        print(f"Jumlah data yang berhasil di-scrape: {len(scraped_data)}")
        print("-" * 50)

    # buat folder jika belum ada
    Path("data").mkdir(parents=True, exist_ok=True)
 
    # Save data to JSON file
    with open('data/rumah123_data.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)