# InitVerse NFT Eligibility Checker

Script Python untuk mengecek eligibilitas NFT InitVerse Season 2 berdasarkan wallet address.

## Fitur

- Support multi akun (membaca dari privatekey.txt)
- Menyimpan address yang tidak eligible ke no_elig.txt
- Delay 3 detik antar pengecekan
- Error handling dan retry mechanism
- Progress indicator

## Cara Penggunaan

### Setup Environment

1. Buat virtual environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

### Persiapan

1. Buat file `privatekey.txt`
2. Masukkan private key yang ingin dicek (satu private key per baris)
```
private_key_1
private_key_2
private_key_3
```

### Menjalankan Script

```bash
python check_elig.py
```

### Output

- Script akan menampilkan status eligibility setiap address
- Address yang tidak eligible akan disimpan di `no_elig.txt`
- Di akhir akan ditampilkan ringkasan:
  - Total address yang eligible
  - Total address yang tidak eligible
  - Total address yang invalid

## Catatan

- Pastikan private key yang dimasukkan valid
- Jangan share private key Anda dengan siapapun
- Gunakan virtual environment untuk menghindari konflik dependency
- Pastikan koneksi internet stabil saat menjalankan script 
