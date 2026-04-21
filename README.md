# Web Scraping Basic

Repository ini berisi latihan dasar web scraping menggunakan 2 pendekatan:
1. Static scraping dengan `requests` + `BeautifulSoup`
2. Dynamic scraping dengan `Selenium` + `BeautifulSoup`

## Tujuan Belajar

1. Mengambil data dari HTML statis dan menyimpannya ke CSV.
2. Mengambil data dari halaman dinamis (render JavaScript) menggunakan Selenium.
3. Menerapkan scraping pagination pada listing multi-halaman.
4. Menyimpan hasil scraping ke format JSON dan CSV.

## Struktur Proyek

```text
web-scraping-basic/
|- simple_scraping.py
|- scraping-dicoding.py
|- scraping-rumah123.py
|- data/
|  |- countries.csv
|  |- dicoding_data.json
|  |- rumah123_data.csv
|- .gitignore
|- README.md
```

## Kebutuhan

1. Python 3.10+ (direkomendasikan 3.11+)
2. Firefox browser
3. Geckodriver untuk Selenium Firefox
4. Dependensi Python:
	- `requests`
	- `beautifulsoup4`
	- `selenium`
	- `trio` (dipakai di script Dicoding)

## Setup Cepat (macOS)

```bash
python3 -m venv venv
source venv/bin/activate
pip install requests beautifulsoup4 selenium trio
```

Jika `geckodriver` belum ada:

```bash
brew install geckodriver
```

## Cara Menjalankan

Aktifkan virtual environment dulu:

```bash
source venv/bin/activate
```

### 1) Scraping Static: Negara dari ScrapethisSite

File: [simple_scraping.py](simple_scraping.py)

```bash
python simple_scraping.py
```

Output:
1. [data/countries.csv](data/countries.csv)
2. Kolom: `name`, `capital`, `population`, `area`

### 2) Scraping Dynamic: Kursus Dicoding

File: [scraping-dicoding.py](scraping-dicoding.py)

```bash
python scraping-dicoding.py
```

Output:
1. [data/dicoding_data.json](data/dicoding_data.json)
2. Contoh field: `Course Name`, `Learning Hour`, `Rating`, `Level`, `Summary`

### 3) Scraping Dynamic + Pagination: Listing Rumah123

File: [scraping-rumah123.py](scraping-rumah123.py)

```bash
python scraping-rumah123.py
```

Fungsi utama `scraper(url, max_pages=5)` akan:
1. Membentuk URL pagination dengan parameter `?page=`.
2. Membaca halaman dari page 1 sampai `max_pages`.
3. Berhenti otomatis jika elemen listing tidak ditemukan.
4. Menarik data listing seperti nama, harga, lokasi, jumlah kamar, dan luas.

Output saat ini disimpan ke:
1. [data/rumah123_data.csv](data/rumah123_data.csv)
2. Kolom: `Nama`, `Harga`, `Lokasi`, `Jumlah Kamar Tidur`, `Jumlah Kamar Mandi`, `Jumlah Carport`, `Luas Tanah`, `Luas Bangunan`

## Ringkasan Teknik Pagination

Pola yang dipakai di script Rumah123:

```python
for page in range(1, max_pages + 1):
	 page_url = f"{url}?page={page}"
	 driver.get(page_url)
	 # parse cards
	 # jika cards kosong -> break
```

Strategi berhenti:
1. Elemen utama listing tidak ditemukan.
2. Jumlah card/listing pada halaman bernilai 0.
3. Tidak ada data valid yang berhasil diparse.

## Troubleshooting

1. Error `geckodriver executable needs to be in PATH`
	- Pastikan `geckodriver` terpasang dan ada di PATH.
2. Timeout Selenium
	- Naikkan `timeout` pada `WebDriverWait` di script.
3. Struktur HTML berubah
	- Periksa ulang selector (`class`, `data-test-id`) yang digunakan.

## Etika Scraping

1. Patuhi robots.txt dan Terms of Service situs target.
2. Jangan melakukan request berlebihan dalam waktu singkat.
3. Gunakan data untuk tujuan belajar dan eksperimen yang legal.

## Pengembangan Lanjutan (Opsional)

1. Tambahkan delay antar halaman agar lebih ramah server.
2. Simpan hasil scraping Rumah123 per kota ke file terpisah.
3. Tambahkan unit test untuk fungsi parser HTML.
4. Tambahkan logging agar proses scraping lebih mudah dipantau.
