import requests
from eth_account import Account
import json
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def create_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=3,  # jumlah maksimal retry
        backoff_factor=1,  # waktu tunggu antar retry
        status_forcelist=[500, 502, 503, 504, 429]  # status code yang akan di-retry
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def get_address_from_pk(pk):
    try:
        account = Account.from_key(pk)
        return account.address
    except Exception as e:
        print(f"Error converting private key: {str(e)}")
        return None

def check_eligibility(address):
    if not address:
        return False
        
    try:
        time.sleep(3)  # delay 3 detik antar pengecekan
        session = create_session()
        url = f"https://candyapi.inichain.com/airdrop/v1/user/snapshotInfo?address={address}"
        
        try:
            response = session.get(url, timeout=10)
            response.raise_for_status()  # raise exception untuk status code error
            response_data = response.json()
            
            if response_data.get("status") and response_data.get("data", {}).get("enter"):
                print(f"[ELIGIBLE] {address}")
                return True
            else:
                print(f"[NOT ELIGIBLE] {address}")
                with open("no_elig.txt", "a") as f:
                    f.write(f"{address}\n")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"Network error checking {address}: {str(e)}")
            return False
        except json.JSONDecodeError as e:
            print(f"JSON decode error for {address}: {str(e)}")
            return False
            
    except Exception as e:
        print(f"Unexpected error checking {address}: {str(e)}")
        return False
    finally:
        session.close()

def main():
    try:
        # Baca private keys
        try:
            with open("privatekey.txt", "r") as f:
                private_keys = [pk.strip() for pk in f.readlines() if pk.strip()]
        except FileNotFoundError:
            print("Error: File privatekey.txt tidak ditemukan!")
            return
        except Exception as e:
            print(f"Error membaca file privatekey.txt: {str(e)}")
            return
            
        if not private_keys:
            print("Error: File privatekey.txt kosong!")
            return
            
        print(f"\nTotal akun yang akan dicek: {len(private_keys)}")
        print("="*50)
        
        # Convert private keys to addresses
        addresses = [get_address_from_pk(pk) for pk in private_keys]
        valid_addresses = [addr for addr in addresses if addr]
        
        if not valid_addresses:
            print("Error: Tidak ada address valid yang bisa dicek!")
            return
            
        # Check eligibility satu per satu
        results = []
        for i, address in enumerate(valid_addresses, 1):
            print(f"\nMengecek address {i} dari {len(valid_addresses)}...")
            result = check_eligibility(address)
            results.append(result)
        
        eligible_count = sum(results)
        print("\n" + "="*50)
        print(f"Total Eligible: {eligible_count}")
        print(f"Total Not Eligible: {len(valid_addresses) - eligible_count}")
        print(f"Total Invalid Addresses: {len(addresses) - len(valid_addresses)}")
        print("="*50)
        
    except Exception as e:
        print(f"Error dalam proses utama: {str(e)}")

if __name__ == "__main__":
    main() 