# IniChain/Initverse Bot ( Incentive / TGE 2025 )

Bot otomatis untuk melakukan daily check-in dan swap token di IniChain/Initverse Testnet.
<br><br> Go to : https://candy.inichain.com/?invite=JPIYMKFEYYCK63LOT7VJ5YBW1
- Connect Wallet, Click Register until Registered
- Go to TASK and do all social task

## Fitur
- Daily Check-in otomatis
- Swap otomatis INI ⟷ USDT dengan strategi:
  - INI ke USDT: 10-25% dari saldo aman
  - USDT ke INI: 80-90% dari saldo USDT
- Create Token dengan parameter yang dioptimalkan
- Auto cycle swap setiap 10 menit
- Monitoring status akun dan riwayat transaksi
- Support multiple accounts
- Gas optimization dan slippage protection

## Persyaratan
- Python 3.11 atau lebih rendah
- pip (Python package installer)
- Faucet : https://faucet-testnet.inichain.com/

## Instalasi
1. Clone repository ini
2. Setup Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Buat file `privatekey.txt` dan tambahkan private key (satu key per baris):
```
0x123...abc
0x456...def
```

## Penggunaan
1. Jalankan bot:
```bash
python bot.py
```

2. Pilih menu yang tersedia:
   - `1`: Check Status
   - `2`: Daily Check-in
   - `3`: Swap INI-USDT
   - `4`: Create Token
   - `5`: Exit

3. Saran Step yang dilakukan : Create Token -> Daily Checkin -> Swap

## Troubleshooting
1. Error `pkg_resources`:
```bash
pip install setuptools
```

2. Error `web3`:
```bash
pip install web3
```

3. Error `python-dotenv`:
```bash
pip install python-dotenv
```

4. Error `insufficient funds`:
- Pastikan saldo INI cukup untuk gas
- Bot akan otomatis swap USDT ke INI jika saldo INI tidak cukup

5. Error `replacement transaction underpriced`:
- Bot menggunakan gas price yang lebih tinggi untuk approve (1.5x)
- Tunggu transaksi sebelumnya selesai

## Catatan Penting
- Pastikan selalu ada saldo INI untuk gas
- Bot akan otomatis memilih arah swap berdasarkan saldo
- Delay 5 detik antar transaksi untuk stabilitas
- Auto cycle swap setiap 10 menit
- Monitor riwayat transaksi melalui menu Status
- Bot memvalidasi format private key (0x... dan 66 karakter) 
