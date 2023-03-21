import asyncio
import json
from typing import List

from web3 import Web3
from websockets import connect
from colorama import Fore, Style
import pyfiglet


class Configuration:
    def __init__(self, infura_ws: str, infura_http: str, eth_addresses: List[str]):
        self.infura_ws = infura_ws
        self.infura_http = infura_http
        self.eth_addresses = eth_addresses


def load_config() -> Configuration:
    config_file = "config.json"

    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            return Configuration(
                infura_ws=config['infura_ws'],
                infura_http=config['infura_http'],
                eth_addresses=config['eth_addresses'],
            )
    except FileNotFoundError:
        infura_ws = input("Enter WebSocket URL: ")
        infura_http = input("Enter HTTP URL: ")
        eth_addresses = input("Enter comma-separated Ethereum addresses to track: ").split(',')
        config = Configuration(infura_ws, infura_http, eth_addresses)

        with open(config_file, 'w') as f:
            json.dump(config.__dict__, f)

        return config


async def subscribe_pending_transactions(config: Configuration):
    web3 = Web3(Web3.HTTPProvider(config.infura_http))

    if web3.isConnected():
        print(Fore.GREEN + "Connected via HTTP")
    else:
        print(Fore.RED + "Failed to connect via HTTP")
        exit()

    print(Fore.BLUE + pyfiglet.figlet_format("Portfolio Tracker"))
    print(Style.RESET_ALL)

    async with connect(config.infura_ws) as ws:
        await ws.send('{"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newPendingTransactions"]}')

        while True:
            try:
                pending_tx = await asyncio.wait_for(ws.recv(), timeout=15)
                transaction = json.loads(pending_tx)
                tx_hash = transaction['params']['result']
                tx = web3.eth.get_transaction(tx_hash)

                if tx:
                    from_address = tx['from']
                    to_address = tx['to']
                    value = web3.fromWei(tx['value'], 'ether')

                    if from_address.lower() in config.eth_addresses:
                        print(Fore.GREEN + f"{from_address} sent {value} ETH to {to_address}")
                        print(Style.RESET_ALL)

                    if to_address.lower() in config.eth_addresses:
                        print(Fore.GREEN + f"{from_address} sent {value} ETH to {to_address}")
                        print(Style.RESET_ALL)

            except KeyboardInterrupt:
                print(Fore.YELLOW + "Exiting...")
                exit()

            except Exception as e:
                print(Fore.RED + f"Error occurred: {e}")
                print(Style.RESET_ALL)
                await asyncio.sleep(10)
                print(Fore.YELLOW + "Reconnecting...")
                print(Style.RESET_ALL)
                await subscribe_pending_transactions(config)


if __name__ == "__main__":
    config = load_config()
    asyncio.run(subscribe_pending_transactions(config))
