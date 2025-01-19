***Forked from https://github.com/Aethereal-Collective***

```markdown
# IniChain/Initverse Bot ( Incentive / TGE 2025 )

IniChain Bot is a Python-based automation tool for the IniChain Testnet. 
It performs daily check-ins, token swaps, and other blockchain interactions, simplifying tasks for users.
```

<br><br> Go to : [Initchain Genesis Testnet](https://candy.inichain.com?invite=0S5DVUTY7X53WF6TL9TDON25B)
- Connect Wallet, Click Register until Registered
- Go to TASK and do all social task

---

## Features

- **Daily Check-In**: Automates daily check-ins to claim rewards.
- **Token Swaps**:
  - Swap INI to USDT and vice versa with optimized gas and slippage.
- **Token Creation**: Deploy custom ERC-20 tokens with specified parameters.
- **Wrap Tokens**: Wrap INI to WINI for easier liquidity management.
- **Transaction Monitoring**: Automates account transaction tracking.
- **Multi-Account Support**: Works with multiple accounts for streamlined automation.

---

## Requirements

1. **Python**: Version 3.11.
2. **Libraries**: Install dependencies using `pip install -r requirements.txt`.
3. **RPC Access**: Connect to the IniChain Testnet via `https://rpc-testnet.inichain.com`.
4. **Private Keys**: Store private keys in `privatekey.txt` (encrypted with your password).
5. **Faucet** : [FAUCET](https://faucet-testnet.inichain.com/)

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/envyst/initverse-bot-envy.git
   cd initverse-bot-envy
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Edit `bot.py` file with your password:
   ```py
   password = 'YOUR-PASSWORD-HERE'
   ```

---

## Usage

Run the bot using:
```bash
python bot.py
```

### Main Menu Options:
1. **Check Status**: View wallet balances and gas fee estimations.
2. **Daily Check-In**: Automate the daily rewards claim process.
3. **Swap Tokens**: Perform token swaps between INI and USDT.
4. **Create Tokens**: Deploy new ERC-20 tokens with custom parameters.
5. **Automated Cycles**: Perform continuous check-ins and swaps.
6. **Send INI to Self**: Transfer 3–5% of INI to the same address.
7. **Add Private Key**: Add new wallet private keys.
8. **Load Private Key**: Load existing encrypted keys.
9. **Empty Private Key**: Clear all stored keys.
10. **Exit**: Quit the bot.

### Recomended Actions
**Add Private Key** > **Check Status** > **Create Token** (one time only) > **Automated Cycles**
---

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
- Ensure INI balance enough for gas
- Bot will automaticaly swap USDT to INI if INI balance isn't enough

5. Error `replacement transaction underpriced`:
- Bot used gas price higher for approve (1.5x)
- Wait last transaction done

---

## Smart Contract Details

- **Daily Check-In**: `0x73439c32e125B28139823fE9C6C079165E94C6D1`
- **Router**: `0x4ccB784744969D9B63C15cF07E622DDA65A88Ee7`
- **WINI**: `0xfbECae21C91446f9c7b87E4e5869926998f99ffe`
- **USDT**: `0xcF259Bca0315C6D32e877793B6a10e97e7647FdE`
- **Token Factory**: `0x01AA0e004F7e7591f2fc2712384dF9B5FDB759DD`

---

## Key Functionalities

### Daily Check-In
Interact with the `Daily Check-In` contract to claim rewards.

### Token Swaps
Supports the following:
- **INI → USDT**: Swap 10–25% of INI balance.
- **USDT → INI**: Swap 80–90% of USDT balance.

### Token Creation
Deploy custom ERC-20 tokens with:
- Name, Symbol, Total Supply, and Decimals.

### Wrap INI
Wrap native INI tokens into WINI for liquidity and compatibility.

---

## Notes

- **Encryption**: Private keys are encrypted for security. Ensure your password is strong.
- **Gas Management**: The bot adjusts gas fees dynamically for efficient transactions.
- **Slippage**: Swaps include a default 5% slippage tolerance.
- **INI Balance**: Make sure there is always INI balance for gas **(USE FAUCET)**
- **Validate Private Key**: Bot validates private key format (0x... and 66 characters)
- **Security**: Your Private Key **STAY IN YOUR LOCAL**. Your Private Key **WILL NOT BE SENT TO ANYWHERE**

---

## Disclaimer

This bot is intended for educational and testnet use only. Use with caution, and never expose real assets. The developers are not responsible for any losses incurred.

---

## License

This project is licensed under the MIT License.
```

This single-file `README.md` consolidates all necessary information into a straightforward format. Let me know if you need any further modifications!

