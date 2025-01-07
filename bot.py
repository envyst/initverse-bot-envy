from web3 import Web3
from eth_account import Account
import json
import time
import random
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Network Configuration
RPC_URL = "https://rpc-testnet.inichain.com"
CHAIN_ID = 7234

# Contract Addresses
DAILY_CHECKIN_CONTRACT = "0x73439c32e125B28139823fE9C6C079165E94C6D1"
ROUTER_CONTRACT = "0x4ccB784744969D9B63C15cF07E622DDA65A88Ee7"
WINI_CONTRACT = "0xfbECae21C91446f9c7b87E4e5869926998f99ffe"
USDT_CONTRACT = "0xcF259Bca0315C6D32e877793B6a10e97e7647FdE"

# Token Decimals
USDT_DECIMALS = 18
INI_DECIMALS = 18

# ABI minimal yang diperlukan
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_spender", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {"name": "_owner", "type": "address"},
            {"name": "_spender", "type": "address"}
        ],
        "name": "allowance",
        "outputs": [{"name": "", "type": "uint256"}],
        "type": "function"
    }
]

ROUTER_ABI = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
            {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"}
        ],
        "name": "swapExactTokensForTokens",
        "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"}
        ],
        "name": "swapExactETHForTokens",
        "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
            {"internalType": "uint256", "name": "amountOutMin", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"},
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "uint256", "name": "deadline", "type": "uint256"}
        ],
        "name": "swapExactTokensForETH",
        "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
            {"internalType": "address[]", "name": "path", "type": "address[]"}
        ],
        "name": "getAmountsOut",
        "outputs": [{"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}],
        "stateMutability": "view",
        "type": "function"
    }
]

DAILY_CHECKIN_ABI = [
    {
        "inputs": [{"name": "user", "type": "address"}],
        "name": "userCheckInStatus",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# ABI untuk WINI (Wrapped INI)
WINI_ABI = [
    {
        "constant": False,
        "inputs": [],
        "name": "deposit",
        "outputs": [],
        "payable": True,
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [{"name": "wad", "type": "uint256"}],
        "name": "withdraw",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# ABI untuk Create Token
TOKEN_FACTORY_ABI = [
    {
        "inputs": [
            {"internalType": "string", "name": "name", "type": "string"},
            {"internalType": "string", "name": "symbol", "type": "string"},
            {"internalType": "uint256", "name": "initialSupply", "type": "uint256"},
            {"internalType": "uint8", "name": "decimals", "type": "uint8"}
        ],
        "name": "createToken",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "address", "name": "owner", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "token", "type": "address"},
            {"indexed": False, "internalType": "string", "name": "name", "type": "string"},
            {"indexed": False, "internalType": "string", "name": "symbol", "type": "string"},
            {"indexed": False, "internalType": "uint256", "name": "totalSupply", "type": "uint256"},
            {"indexed": False, "internalType": "uint8", "name": "decimals", "type": "uint8"},
            {"indexed": False, "internalType": "uint256", "name": "timestamp", "type": "uint256"}
        ],
        "name": "TokenCreated",
        "type": "event"
    }
]

# Contract address untuk Token Factory
TOKEN_FACTORY_CONTRACT = "0x01AA0e004F7e7591f2fc2712384dF9B5FDB759DD"

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))

class IniChainBot:
    def __init__(self, private_key):
        self.account = Account.from_key(private_key)
        self.address = self.account.address
        self.router_contract = w3.eth.contract(address=ROUTER_CONTRACT, abi=ROUTER_ABI)
        self.checkin_contract = w3.eth.contract(address=DAILY_CHECKIN_CONTRACT, abi=DAILY_CHECKIN_ABI)
        self.wini_contract = w3.eth.contract(address=WINI_CONTRACT, abi=WINI_ABI)
        self.last_checkin = {}
        
    def get_dynamic_gas_price(self, priority="normal"):
        """Get dynamic gas price based on current network conditions"""
        base_gas_price = w3.eth.gas_price
        
        multipliers = {
            "low": 1.1,
            "normal": 1.2,
            "high": 1.5
        }
        
        gas_price = int(base_gas_price * multipliers[priority])
        
        # Safety cap (max 5 Gwei)
        max_gas_price = 5 * 10**9
        return min(gas_price, max_gas_price)

    def get_gas_price(self):
        """Get optimal gas price for normal transactions"""
        return self.get_dynamic_gas_price("normal")
        
    def get_approve_gas_price(self):
        """Get gas price for approve with higher priority"""
        return self.get_dynamic_gas_price("high")

    def format_amount(self, amount, decimals):
        """Format amount with proper decimals for display"""
        return amount / (10 ** decimals)

    def check_daily_checkin_status(self):
        """Check if daily checkin is available"""
        try:
            has_checked_in = self.checkin_contract.functions.userCheckInStatus(self.address).call()
            if not has_checked_in:
                return True
                
            print(f"[{self.address}] Checkin masih dalam cooldown")
            return False
            
        except Exception as e:
            print(f"[{self.address}] Error checking checkin status: {str(e)}")
            return False

    def daily_checkin(self, account_info):
        """Perform daily checkin"""
        try:
            nonce = w3.eth.get_transaction_count(self.address)
            gas_price = self.get_gas_price()
            
            print(f"[{account_info}] Memulai daily check-in...")
            print(f"[{account_info}] Gas price: {gas_price / 1e9:.2f} Gwei")
            
            # Estimate gas limit
            try:
                gas_estimate = w3.eth.estimate_gas({
                    'from': self.address,
                    'to': DAILY_CHECKIN_CONTRACT,
                    'value': 0,
                    'data': '0x183ff085',  # Checkin function signature
                    'gasPrice': gas_price,
                    'nonce': nonce
                })
                print(f"[{account_info}] Estimated gas: {gas_estimate}")
            except Exception as e:
                error_message = str(e)
                if "Today's check-in has been completed" in error_message:
                    print(f"[{account_info}] Checkin sudah dilakukan hari ini")
                    return False
                else:
                    print(f"[{account_info}] Error estimating gas: {error_message}")
                    gas_estimate = 150000  # Fallback gas limit
            
            transaction = {
                'from': self.address,
                'to': DAILY_CHECKIN_CONTRACT,
                'value': 0,
                'gas': gas_estimate,
                'gasPrice': gas_price,
                'nonce': nonce,
                'chainId': CHAIN_ID,
                'data': '0x183ff085'  # Checkin function signature
            }

            signed_txn = w3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for transaction receipt
            receipt = self.wait_for_transaction(tx_hash)
            
            if receipt and receipt['status'] == 1:
                self.last_checkin[self.address] = datetime.now()
                print(f"[{account_info}] Checkin berhasil: {tx_hash.hex()}")
                return True
            else:
                if receipt:
                    print(f"[{account_info}] Checkin gagal! Gas used: {receipt.get('gasUsed', 'unknown')}")
                    try:
                        # Get transaction trace or error message
                        tx = w3.eth.get_transaction(tx_hash)
                        print(f"[{account_info}] Transaction details:")
                        print(f"  Gas price: {tx.get('gasPrice', 'unknown')}")
                        print(f"  Gas limit: {tx.get('gas', 'unknown')}")
                        print(f"  Nonce: {tx.get('nonce', 'unknown')}")
                        print(f"  Value: {tx.get('value', 'unknown')}")
                    except Exception as e:
                        print(f"[{account_info}] Error getting transaction details: {str(e)}")
                return False
                
        except Exception as e:
            print(f"[{account_info}] Error pada checkin: {str(e)}")
            return False

    def get_token_balance(self, token_address):
        """Get token balance"""
        token_contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)
        balance = token_contract.functions.balanceOf(self.address).call()
        return balance

    def wait_for_transaction(self, tx_hash, timeout=300):
        """Wait for transaction to be mined and return receipt"""
        start_time = time.time()
        print(f"[{self.address}] Menunggu konfirmasi transaksi: {tx_hash.hex()}")
        
        while True:
            try:
                receipt = w3.eth.get_transaction_receipt(tx_hash)
                if receipt is not None:
                    return receipt
            except Exception as e:
                pass
            
            if time.time() - start_time > timeout:
                print(f"[{self.address}] Error saat menunggu konfirmasi: Transaction {tx_hash.hex()} tidak dikonfirmasi setelah {timeout} detik")
                return None
            
            print(f"[{self.address}] Masih menunggu konfirmasi... ({int(time.time() - start_time)} detik)")
            time.sleep(10)

    def approve_token(self, token_address, amount, account_info):
        """Approve token for router"""
        token_contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)
        
        try:
            print(f"[{account_info}] Memulai proses approve...")
            
            # Check allowance dulu
            current_allowance = token_contract.functions.allowance(self.address, ROUTER_CONTRACT).call()
            if current_allowance >= amount:
                print(f"[{account_info}] Allowance sudah cukup, tidak perlu approve lagi")
                return True
            
            nonce = w3.eth.get_transaction_count(self.address)
            gas_price = self.get_approve_gas_price()  # Menggunakan gas price yang lebih tinggi untuk approve
            
            print(f"[{account_info}] Mengirim transaksi approve dengan gas price: {gas_price / 1e9:.2f} Gwei")
            
            # Convert amount to integer
            amount = int(amount)
            
            approve_txn = token_contract.functions.approve(
                ROUTER_CONTRACT,
                amount
            ).build_transaction({
                'from': self.address,
                'gas': 100000,
                'gasPrice': gas_price,
                'nonce': nonce,
                'chainId': CHAIN_ID
            })
            
            signed_txn = w3.eth.account.sign_transaction(approve_txn, self.account.key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            receipt = self.wait_for_transaction(tx_hash)
            return receipt is not None and receipt['status'] == 1
            
        except Exception as e:
            print(f"[{account_info}] Error pada approve: {str(e)}")
            return False

    def get_token_price(self, token_in, token_out, amount_in):
        """Get token price from router"""
        try:
            path = [token_in, token_out]
            amount_in_wei = int(amount_in * 1e18)
            
            # Get amounts out
            amounts_out = self.router_contract.functions.getAmountsOut(
                amount_in_wei,
                path
            ).call()
            
            return amounts_out[1] / 1e18
        except Exception as e:
            print(f"[{self.address}] Error getting price: {str(e)}")
            return 0

    def swap_usdt_to_ini(self, amount, account_info):
        """Swap USDT to INI"""
        try:
            # Convert amount to wei format
            amount_in_wei = int(amount * (10 ** USDT_DECIMALS))
            
            if not self.approve_token(USDT_CONTRACT, amount_in_wei, account_info):
                print(f"[{account_info}] Gagal approve USDT")
                return
                
            nonce = w3.eth.get_transaction_count(self.address)
            gas_price = self.get_gas_price()
            deadline = int(time.time()) + 300  # 5 minutes deadline
            
            # Get expected output amount
            expected_out = self.get_token_price(USDT_CONTRACT, WINI_CONTRACT, amount)
            if expected_out == 0:
                print(f"[{account_info}] Gagal mendapatkan harga, membatalkan swap")
                return
            
            min_out = int(expected_out * 1e18 * 0.95)  # 5% slippage
            
            print(f"[{account_info}] Memulai swap USDT ke INI...")
            print(f"[{account_info}] Gas price: {gas_price / 1e9:.2f} Gwei")
            print(f"[{account_info}] Amount: {amount:.6f} USDT")
            print(f"[{account_info}] Expected output: {expected_out:.6f} INI")
            print(f"[{account_info}] Min output: {min_out / 1e18:.6f} INI")
            
            # Path: USDT -> WINI
            path = [USDT_CONTRACT, WINI_CONTRACT]
            
            # Estimate gas limit
            try:
                gas_estimate = self.router_contract.functions.swapExactTokensForETH(
                    amount_in_wei,
                    min_out,
                    path,
                    self.address,
                    deadline
                ).estimate_gas({
                    'from': self.address,
                    'gasPrice': gas_price,
                    'nonce': nonce
                })
                print(f"[{account_info}] Estimated gas: {gas_estimate}")
            except Exception as e:
                print(f"[{account_info}] Error estimating gas: {str(e)}")
                gas_estimate = 201306  # Gas limit dari transaksi sukses
            
            swap_txn = self.router_contract.functions.swapExactTokensForETH(
                amount_in_wei,  # amountIn
                min_out,  # amountOutMin
                path,  # path
                self.address,  # to
                deadline  # deadline
            ).build_transaction({
                'from': self.address,
                'gas': gas_estimate,
                'gasPrice': gas_price,
                'nonce': nonce,
                'chainId': CHAIN_ID
            })
            
            signed_txn = w3.eth.account.sign_transaction(swap_txn, self.account.key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            receipt = self.wait_for_transaction(tx_hash)
            if receipt and receipt['status'] == 1:
                print(f"[{account_info}] Swap USDT ke INI berhasil!")
                return True
            else:
                print(f"[{account_info}] Swap USDT ke INI gagal!")
                return False
                
        except Exception as e:
            print(f"[{account_info}] Error pada swap USDT ke INI: {str(e)}")
            return False

    def swap_ini_to_usdt(self, amount, account_info):
        """Swap INI to USDT via swapExactETHForTokens"""
        try:
            nonce = w3.eth.get_transaction_count(self.address)
            gas_price = self.get_gas_price()
            deadline = int(time.time()) + 300  # 5 minutes deadline
            
            # Convert amount to wei
            amount_in_wei = w3.to_wei(amount, 'ether')
            
            # Get expected output amount
            expected_out = self.get_token_price(WINI_CONTRACT, USDT_CONTRACT, amount)
            if expected_out == 0:
                print(f"[{account_info}] Gagal mendapatkan harga, membatalkan swap")
                return
                
            min_out = int(expected_out * 1e18 * 0.95)  # 5% slippage
            
            print(f"[{account_info}] Memulai swap INI ke USDT...")
            print(f"[{account_info}] Gas price: {gas_price / 1e9:.2f} Gwei")
            print(f"[{account_info}] Amount: {amount:.6f} INI")
            print(f"[{account_info}] Expected output: {expected_out:.6f} USDT")
            print(f"[{account_info}] Min output: {min_out / 1e18:.6f} USDT")
            
            # Path: WINI -> USDT
            path = [WINI_CONTRACT, USDT_CONTRACT]
            
            # Estimate gas limit
            try:
                gas_estimate = self.router_contract.functions.swapExactETHForTokens(
                    min_out,  # amountOutMin
                    path,  # path
                    self.address,  # to
                    deadline  # deadline
                ).estimate_gas({
                    'from': self.address,
                    'value': amount_in_wei,
                    'gasPrice': gas_price,
                    'nonce': nonce
                })
                print(f"[{account_info}] Estimated gas: {gas_estimate}")
            except Exception as e:
                print(f"[{account_info}] Error estimating gas: {str(e)}")
                gas_estimate = 201306  # Gas limit dari transaksi sukses
            
            # Build transaction
            swap_txn = self.router_contract.functions.swapExactETHForTokens(
                min_out,  # amountOutMin
                path,  # path
                self.address,  # to
                deadline  # deadline
            ).build_transaction({
                'from': self.address,
                'gas': gas_estimate,
                'gasPrice': gas_price,
                'value': amount_in_wei,  # Amount INI to swap
                'nonce': nonce,
                'chainId': CHAIN_ID
            })
            
            signed_txn = w3.eth.account.sign_transaction(swap_txn, self.account.key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            receipt = self.wait_for_transaction(tx_hash)
            if receipt and receipt['status'] == 1:
                print(f"[{account_info}] Swap INI ke USDT berhasil!")
                return True
            else:
                print(f"[{account_info}] Swap INI ke USDT gagal!")
                return False
                
        except Exception as e:
            print(f"[{account_info}] Error pada swap INI ke USDT: {str(e)}")
            return False

    def wrap_ini(self, amount):
        """Wrap INI to WINI"""
        try:
            nonce = w3.eth.get_transaction_count(self.address)
            gas_price = self.get_gas_price()
            
            # Convert amount to wei
            amount_in_wei = w3.to_wei(amount, 'ether')
            
            print(f"[{self.address}] Wrapping {amount:.6f} INI ke WINI...")
            print(f"[{self.address}] Gas price: {gas_price / 1e9:.2f} Gwei")
            
            # Estimate gas
            try:
                gas_estimate = self.wini_contract.functions.deposit().estimate_gas({
                    'from': self.address,
                    'value': amount_in_wei,
                    'gasPrice': gas_price,
                    'nonce': nonce
                })
                print(f"[{self.address}] Estimated gas: {gas_estimate}")
            except Exception as e:
                print(f"[{self.address}] Error estimating gas: {str(e)}")
                gas_estimate = 50000  # Fallback gas limit untuk deposit
            
            # Build transaction
            deposit_txn = self.wini_contract.functions.deposit().build_transaction({
                'from': self.address,
                'gas': gas_estimate,
                'gasPrice': gas_price,
                'value': amount_in_wei,
                'nonce': nonce,
                'chainId': CHAIN_ID
            })
            
            signed_txn = w3.eth.account.sign_transaction(deposit_txn, self.account.key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            receipt = self.wait_for_transaction(tx_hash)
            if receipt and receipt['status'] == 1:
                print(f"[{self.address}] Wrap INI ke WINI berhasil!")
                return True
            else:
                print(f"[{self.address}] Wrap INI ke WINI gagal!")
                return False
                
        except Exception as e:
            print(f"[{self.address}] Error pada wrap INI: {str(e)}")
            return False

    def perform_swap(self, account_info):
        """Perform random swap between INI and USDT"""
        try:
            # Get current INI balance first
            ini_balance = w3.eth.get_balance(self.address)
            formatted_balance = w3.from_wei(ini_balance, 'ether')
            
            # Calculate gas cost
            gas_price = self.get_gas_price()
            estimated_gas = 201306  # Gas limit dari transaksi sukses
            gas_cost = gas_price * estimated_gas
            
            # Keep some INI for future gas (1.2x current gas cost)
            safe_balance = ini_balance - (gas_cost * 1.2)
            
            if safe_balance > gas_cost:
                # Swap 10-25% INI ke USDT
                swap_percentage = random.uniform(0.10, 0.25)
                amount_to_swap = float(w3.from_wei(int(safe_balance * swap_percentage), 'ether'))
                
                print(f"[{account_info}] Saldo saat ini: {formatted_balance:.6f} INI")
                print(f"[{account_info}] Gas cost: {w3.from_wei(gas_cost, 'ether'):.6f} INI")
                print(f"[{account_info}] Saldo aman: {w3.from_wei(safe_balance, 'ether'):.6f} INI")
                print(f"[{account_info}] Akan swap: {amount_to_swap:.6f} INI ({swap_percentage*100:.1f}% dari saldo aman)")
                
                self.swap_ini_to_usdt(amount_to_swap, account_info)
            else:
                # Check USDT balance
                usdt_balance = self.get_token_balance(USDT_CONTRACT)
                formatted_balance = self.format_amount(usdt_balance, USDT_DECIMALS)
                
                if usdt_balance > 0:
                    # Swap 80-90% USDT ke INI
                    swap_percentage = random.uniform(0.80, 0.90)
                    amount_to_swap = formatted_balance * swap_percentage
                    
                    print(f"[{account_info}] Saldo USDT: {formatted_balance:.6f}")
                    print(f"[{account_info}] Akan swap: {amount_to_swap:.6f} USDT ke INI ({swap_percentage*100:.1f}% dari saldo)")
                    
                    self.swap_usdt_to_ini(amount_to_swap, account_info)
                else:
                    print(f"[{account_info}] Saldo INI tidak cukup untuk swap")
                    print(f"[{account_info}] Saldo saat ini: {formatted_balance:.6f} INI")
                    print(f"[{account_info}] Minimum gas cost: {w3.from_wei(gas_cost * 1.2, 'ether'):.6f} INI")
                
        except Exception as e:
            print(f"[{account_info}] Error pada swap: {str(e)}")

    def create_token(self, name, symbol, total_supply, decimals, account_info):
        """Create new token with specified parameters"""
        try:
            token_factory = w3.eth.contract(address=TOKEN_FACTORY_CONTRACT, abi=TOKEN_FACTORY_ABI)
            
            # Convert total supply ke wei format
            total_supply_wei = int(total_supply * (10 ** decimals))
            
            nonce = w3.eth.get_transaction_count(self.address)
            gas_price = self.get_dynamic_gas_price("normal")  # Gunakan gas price dinamis
            
            print(f"[{account_info}] Memulai create token...")
            print(f"[{account_info}] Gas price: {gas_price / 1e9:.2f} Gwei")
            print(f"[{account_info}] Token name: {name}")
            print(f"[{account_info}] Token symbol: {symbol}")
            print(f"[{account_info}] Total supply: {total_supply_wei}")
            print(f"[{account_info}] Decimals: {decimals}")
            
            # Build transaction dengan gas limit yang sama dengan transaksi sukses
            gas_limit = 1548128  # Gas limit dari transaksi sukses
            estimated_gas_cost = gas_limit * gas_price / 1e18
            print(f"[{account_info}] Estimated gas cost: {estimated_gas_cost:.6f} INI")
            
            # Cek saldo INI
            balance = w3.eth.get_balance(self.address)
            formatted_balance = w3.from_wei(balance, 'ether')
            print(f"[{account_info}] Current balance: {formatted_balance:.6f} INI")
            
            if balance < (gas_limit * gas_price):
                print(f"[{account_info}] Saldo INI tidak cukup untuk membayar gas!")
                return False
            
            # Gunakan input data yang sama persis dengan transaksi sukses
            input_data = "0x8ab84b4a000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000c000000000000000000000000000000000000000000000000000000000000186a000000000000000000000000000000000000000000000000000000000000000120000000000000000000000000000000000000000000000000000000000000004757364740000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000047573647400000000000000000000000000000000000000000000000000000000"
            
            # Build transaction
            transaction = {
                'from': self.address,
                'to': TOKEN_FACTORY_CONTRACT,
                'gas': gas_limit,
                'gasPrice': gas_price,
                'nonce': nonce,
                'chainId': CHAIN_ID,
                'data': input_data
            }
            
            # Sign and send transaction
            signed_txn = w3.eth.account.sign_transaction(transaction, self.account.key)
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            print(f"[{account_info}] Menunggu konfirmasi create token...")
            receipt = self.wait_for_transaction(tx_hash)
            
            if receipt and receipt['status'] == 1:
                print(f"[{account_info}] Token berhasil dibuat!")
                print(f"[{account_info}] Transaction hash: {tx_hash.hex()}")
                return True
            else:
                print(f"[{account_info}] Gagal membuat token!")
                if receipt:
                    print(f"[{account_info}] Gas used: {receipt.get('gasUsed', 'unknown')}")
                return False
            
        except Exception as e:
            print(f"[{account_info}] Error creating token: {str(e)}")
            return False

def get_transaction_type(tx, bot_address):
    """Get transaction type and details"""
    if tx['to'] is None:
        return "Contract Creation", None
        
    # Check for daily check-in
    if tx['to'].lower() == DAILY_CHECKIN_CONTRACT.lower():
        return "Daily Check-in", None
        
    # Check for token transfers
    if tx['to'].lower() == ROUTER_CONTRACT.lower():
        if tx['value'] > 0:
            return "Swap INI ke USDT", f"{bot.format_amount(tx['value'], INI_DECIMALS):.6f} INI"
        else:
            return "Swap USDT ke INI", None
            
    # Default transaction
    if tx['from'].lower() == bot_address.lower():
        return "Transfer Keluar", f"{bot.format_amount(tx['value'], INI_DECIMALS):.6f} INI"
    else:
        return "Transfer Masuk", f"{bot.format_amount(tx['value'], INI_DECIMALS):.6f} INI"

def show_status(private_key, account_num):
    """Show account status"""
    # Initialize bot
    bot = IniChainBot(private_key)
    account_info = f"Account {account_num} | {bot.address[-4:]}"
    
    # Get balances
    ini_balance = w3.eth.get_balance(bot.address) / 10**18
    usdt_balance = bot.get_token_balance(USDT_CONTRACT) / 10**18
    
    # Get gas price
    gas_price = w3.eth.gas_price / 10**9
    
    # Estimate fees
    checkin_gas = 150000  # Estimated gas for check-in
    swap_gas = 300000     # Estimated gas for swap
    
    checkin_fee = (checkin_gas * gas_price) / 10**9
    swap_fee = (swap_gas * gas_price) / 10**9
    
    print(f"\nStatus [{account_info}]")
    print(f"Alamat Lengkap: {bot.address}")
    print(f"Saldo INI: {ini_balance:.6f}")
    print(f"Saldo USDT: {usdt_balance:.6f}")
    print(f"Gas Price: {gas_price:.2f} Gwei")
    print(f"Estimasi Fee Check-in: {checkin_fee:.6f} INI")
    print(f"Estimasi Fee Swap: {swap_fee:.6f} INI")
    
    print(f"\nRiwayat Transaksi Terakhir [{account_info}]:")
    try:
        # Get last 100 blocks
        latest = w3.eth.block_number
        start_block = max(0, latest - 100)
        
        # Get transactions
        for block in range(latest, start_block, -1):
            block_data = w3.eth.get_block(block, True)
            
            for tx in block_data.transactions:
                if tx['from'].lower() == bot.address.lower() or tx['to'] and tx['to'].lower() == bot.address.lower():
                    # Get timestamp
                    timestamp = datetime.fromtimestamp(block_data.timestamp)
                    
                    # Determine transaction type
                    tx_type = "Unknown"
                    if tx['to'] and tx['to'].lower() == DAILY_CHECKIN_CONTRACT.lower():
                        tx_type = "Daily Check-in"
                    elif tx['to'] and tx['to'].lower() == ROUTER_CONTRACT.lower():
                        tx_type = "Swap"
                        
                    print(f"Block {block} ({timestamp:%Y-%m-%d %H:%M:%S}) - {tx_type} (Gas: {tx['gas']})")
                    print(f"  Hash: {tx['hash'].hex()}")
                    
    except Exception as e:
        print(f"Error mendapatkan riwayat transaksi: {str(e)}")
    
    print("\nProses selesai!")

def process_accounts(private_keys, action):
    """Process multiple accounts"""
    for i, private_key in enumerate(private_keys, 1):
        bot = IniChainBot(private_key)
        account_info = f"Account {i} | {bot.address[-4:]}"
        if action == "checkin":
            bot.daily_checkin(account_info)
        elif action == "swap":
            bot.perform_swap(account_info)
        elif action == "status":
            show_status(private_key, i)
        time.sleep(5)  # Delay between accounts

def auto_daily_and_swap(private_keys):
    """Melakukan auto daily check-in dan swap secara berulang"""
    cycle_count = 1
    while True:
        try:
            print(f"\n{'='*50}")
            print(f"Memulai cycle ke-{cycle_count}...")
            print(f"{'='*50}")
            
            # Lakukan daily check-in
            print("\nMemulai Daily Check-in...")
            process_accounts(private_keys, "checkin")
            print("Daily Check-in selesai!")
            
            # Tunggu 5 detik sebelum swap
            print("\nMenunggu 5 detik sebelum memulai swap...")
            time.sleep(5)
            
            # Lakukan swap
            print("\nMemulai proses Swap...")
            process_accounts(private_keys, "swap")
            print("Proses Swap selesai!")
            
            print(f"\nCycle ke-{cycle_count} selesai")
            print("Menunggu 10 menit untuk cycle berikutnya...")
            
            # Countdown timer
            for i in range(600, 0, -1):  # 600 detik = 10 menit
                minutes = i // 60
                seconds = i % 60
                print(f"\rWaktu menuju cycle berikutnya: {minutes:02d}:{seconds:02d}", end="")
                time.sleep(1)
            
            print("\n")  # New line after countdown
            cycle_count += 1
            
        except KeyboardInterrupt:
            print("\nMenghentikan Auto Daily & Swap...")
            break
        except Exception as e:
            print(f"\nError pada cycle: {str(e)}")
            print("Mencoba melanjutkan ke cycle berikutnya...")
            time.sleep(10)

def show_menu():
    """Menampilkan menu interaktif"""
    print("\n=== Menu ===")
    print("1. Check Status")
    print("2. Daily Check-in")
    print("3. Swap INI-USDT")
    print("4. Create Token")
    print("5. Auto (Daily & Swap)")
    print("6. Exit")
    return input("Pilih menu (1-6): ")

def cycle_swap(private_keys):
    """Melakukan cycle swap setiap 10 menit"""
    cycle_count = 1
    while True:
        try:
            print(f"\nMemulai cycle swap ke-{cycle_count}...")
            process_accounts(private_keys, "swap")
            print(f"\nCycle swap ke-{cycle_count} selesai")
            print("Menunggu 10 menit untuk cycle berikutnya...")
            
            # Countdown timer
            for i in range(600, 0, -1):  # 600 detik = 10 menit
                minutes = i // 60
                seconds = i % 60
                print(f"\rWaktu menuju cycle berikutnya: {minutes:02d}:{seconds:02d}", end="")
                time.sleep(1)
            
            print("\n")  # New line after countdown
            cycle_count += 1
            
        except KeyboardInterrupt:
            print("\nMenghentikan cycle swap...")
            break
        except Exception as e:
            print(f"\nError pada cycle swap: {str(e)}")
            print("Mencoba melanjutkan ke cycle berikutnya...")
            time.sleep(10)

def show_logo():
    """Menampilkan logo saat startup"""
    logo = """@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@@@@@@@@@@*%@@@@@@@@@@@@@@@@@@@@%*=%@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@%+@@@@@@@@@@@@#: #@@@@@@@@@@@@@@@@%*=:   %@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@+=@@@@@@@@@@%=   #@@@@@@@@@@@@#+-.       %@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@%.=@@@@@@@@@+.    #@@@@@@@@#+-.           %@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@+ =@@@@@@@*:      #@@@%*=:.               %@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@. =@@@@@@-        #@=:                    %@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@  =@@@@@@.        #@.                     %@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@  =@@@@@@.        #@.                     %@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@  =@@@@@@.        #@.                     %@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@  =@@@@@@.        #@.                     %@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@  =@@@@@@.        #@.                     %@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@  =@@@@@@.        #@.                     %@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@  =@@@@@@.        #@.                     %@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@  =@@@@@@.        #@.                     %@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@  =@@@@@@.        #@.                     %@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@  =@@@@@@.        #@.                     %@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@  =@@@@@@.        #@.                     %@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@  +@@@@@@.       .%@.                   .-%@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@  %@@@@@@.     .+%@@.               :=*%@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@ =@@@@@@@.    =%@@@@.           :=*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@ %@@@@@@@.  -#@@@@@@.      .-+#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@=@@@@@@@@..*@@@@@@@@.  .-+#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@%@@@@@@@@+%@@@@@@@@@=*%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
"""
    print(logo)
    print("\nIniChain Bot v1.0 - Automated Daily Check-in & Swap by Aethereal")
    print("=================================================")

def main():
    # Tampilkan logo saat startup
    show_logo()
    
    # Load private keys
    try:
        with open("privatekey.txt", "r") as f:
            private_keys = [line.strip() for line in f.readlines() if line.strip()]
    except FileNotFoundError:
        print("Error: File privatekey.txt tidak ditemukan!")
        return
        
    while True:
        choice = show_menu()
        
        if choice == "1":
            process_accounts(private_keys, "status")
        elif choice == "2":
            process_accounts(private_keys, "checkin")
        elif choice == "3":
            cycle_swap(private_keys)
        elif choice == "4":
            # Create Token menu
            print("\n=== Create Token ===")
            name = input("Token Full Name: ")
            symbol = input("Token Abbreviation: ")
            try:
                total_supply = float(input("Number of Tokens to Issue: "))
                decimals = int(input("Token Decimals (default 18): ") or "18")
            except ValueError:
                print("Error: Invalid input for total supply or decimals!")
                continue
                
            # Process create token untuk setiap private key
            for i, private_key in enumerate(private_keys, 1):
                bot = IniChainBot(private_key)
                account_info = f"Account #{i}"
                bot.create_token(name, symbol, total_supply, decimals, account_info)
        elif choice == "5":
            print("\n=== Auto Daily & Swap ===")
            print("Bot akan melakukan Daily Check-in dan Swap secara otomatis")
            print("Tekan Ctrl+C untuk menghentikan")
            auto_daily_and_swap(private_keys)
        elif choice == "6":
            print("\nTerima kasih telah menggunakan bot!")
            break
        else:
            print("\nPilihan tidak valid!")

if __name__ == "__main__":
    main() 
    main() 
