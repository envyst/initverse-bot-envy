from web3 import Web3
from eth_account import Account
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Network Configuration
RPC_URL = "https://rpc-testnet.inichain.com"
CHAIN_ID = 7234

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))

def check_balance(private_key):
    """Check INI balance for a given private key"""
    account = Account.from_key(private_key)
    address = account.address
    balance = w3.eth.get_balance(address) / 10**18  # Convert to INI
    return address, balance

def main():
    empty_addresses = []

    # Load private keys
    try:
        with open("privatekey.txt", "r") as f:
            private_keys = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print("Error: File privatekey.txt tidak ditemukan!")
        return

    for private_key in private_keys:
        address, balance = check_balance(private_key)
        print(f"Alamat: {address} | Saldo INI: {balance:.6f}")

        if balance == 0:
            empty_addresses.append(address)

    if empty_addresses:
        with open("empty_balance.txt", "w") as f:
            for address in empty_addresses:
                f.write(f"{address}\n")
        print("File empty_balance.txt telah dibuat dengan alamat yang memiliki saldo INI kosong.")
    else:
        print("Semua akun memiliki saldo INI.")

if __name__ == "__main__":
    main() 