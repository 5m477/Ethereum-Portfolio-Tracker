Ethereum Portfolio Tracker
This is a tool to track new pending transactions on the Ethereum blockchain, and notify the user if a transaction involves one of their specified Ethereum addresses.

Requirements
Python 3.7 or higher
web3 library
websockets library
colorama library
pyfiglet library

Installation
Clone the repository to your local machine
Install the required dependencies using pip:
pip install web3 websockets colorama pyfiglet
or
pip install requirements.txt

Configure the tool by creating a config.json file in the root directory of the repository, with the following contents:
{
    "infura_ws": "wss://mainnet.infura.io/ws/v3/YOUR-PROJECT-ID",
    "infura_http": "https://mainnet.infura.io/v3/YOUR-PROJECT-ID",
    "eth_addresses": [
        "0x1234567890123456789012345678901234567890",
        "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd"
    ]
}
Replace the YOUR-PROJECT-ID placeholders with your Infura project ID.
Add Ethereum addresses you want to track to the eth_addresses list. You can add as many addresses as you want, separated by commas.

Usage
To start the tool, run python portfolio_tracker.py from the command line.
The tool will connect to the Ethereum network using the WebSocket URL specified in the config.json file, and subscribe to new pending transactions. If a pending transaction is found that involves one of the specified Ethereum addresses, the tool will print a notification to the console.

Press Ctrl + C to exit the tool.

follow me on twitter @5m477
