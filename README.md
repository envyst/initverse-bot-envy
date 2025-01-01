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
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Buat file `.env` dan isi private key:
```
PRIVATE_KEYS=your_private_key1,your_private_key2,...
```
Atau tambahkan satu private key per baris:
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
   - `1`: Daily Check-in
   - `2`: Swap (otomatis memilih arah swap berdasarkan saldo)
   - `3`: Status (cek saldo dan riwayat transaksi)
   - `4`: Keluar

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
