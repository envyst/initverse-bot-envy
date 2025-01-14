***Forked from https://github.com/Aethereal-Collective***

# IniChain/Initverse Bot ( Incentive / TGE 2025 )

Bot otomatis untuk melakukan daily check-in dan swap token di IniChain/Initverse Testnet.
<br><br> Go to : [Initchain Genesis Testnet](https://candy.inichain.com?invite=0S5DVUTY7X53WF6TL9TDON25B)
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
- Git (optional)
- Bash (optional)
- Python 3.11 atau lebih rendah
- pip (Python package installer)
- Faucet : [FAUCET](https://faucet-testnet.inichain.com/)

## Instalasi
1. Clone repository ini atau download zip
```bash
# SKIP if download zip
git clone https://github.com/envyst/initverse-bot-envy.git
```
## Automate Create File `privatekey.txt` (Optional)
2. Run bash script
```bash
# WINDOWS POWERSHELL
bash ./initial.sh
```
```bash
# LINUX / MAC
chmod +x initial.sh
./initial.sh
```
3. Setup Virtual Environment
```bash
# WINDOWS POWERSHELL
python -m venv venv
.\venv\Scripts\activate
```
```bash
# LINUX / MAC
python3 -m venv venv
source venv/bin/activate
```
4. Install dependencies:
```bash
pip install -r requirements.txt
```
5. Buat file `privatekey.txt` dan tambahkan private key (satu key per baris): 
- *Note: Di semua folder yang mau dijalankan*
```
0x123...abc
0x456...def
```

## Penggunaan
1. Jalankan bot:
- *MAIN BOT*
```bash
python bot.py
```
- *balance_checker BOT*
```bash
cd balance_checker/
python balance_checker.py
```
- *CHECK IN BOT*
```bash
cd checkin_only/
python checkin.py
```
- *Check S2 Eligibility BOT*
```bash
# 1 time only
pip install -r S2-Elig-Checker/requirements.txt
```
```bash
cd S2-Elig-Checker/
python check_elig.py
```
2. Pilih menu yang tersedia:
   - `1`: Check Status
   - `2`: Daily Check-in
   - `3`: Swap INI-USDT
   - `4`: Create Token
   - `5`: Auto (Daily & Swap & Send INI to Self)
   - `6`: Send INI to Self
   - `7`: Exit

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
