from web3 import Web3
from eth_account import Account
from web3.middleware import geth_poa_middleware
import json,datetime

WALLET = ""

# Use infura NODE to connect polygon network
infura_url = "https://polygon-mainnet.infura.io/v3/YOUR_API_KEY"
w3 = Web3(Web3.HTTPProvider(infura_url))
if "polygon" in infura_url:
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

POLY_QUICKSWAP3_ROUTER_ADDR = "0xf5b509bB0909a69B1c207E495f687a596C168E12"
POLY_QUICKSWAP3_ROUTER = w3.to_checksum_address(POLY_QUICKSWAP3_ROUTER_ADDR)
POLY_MATIC_ADDR = "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"
POLY_USDC_ADDR = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"

abi_quickswap3_router = json.load(open('./swaprouter_abi.json'))

params = {
    'tokenIn': POLY_MATIC_ADDR,
    'tokenOut': POLY_USDC_ADDR,
    'fee': 3000,
    'recipient': WALLET,
    'deadline': int((datetime.datetime.now() + datetime.timedelta(seconds=20)).timestamp()),
    'amountIn': 1000000000000000000,
    'amountOutMinimum': 0,
    'limitSqrtPrice': 0,
}

router_contract = w3.eth.contract(address=POLY_QUICKSWAP3_ROUTER, abi=abi_quickswap3_router)

# Build the transaction
tx = router_contract.functions.exactInputSingle(params).build_transaction({
    'from': WALLET,
    'value': 1000000000000000000,  # No ETH is sent along, adjust if needed
    'gas': 500000,  
    'gasPrice': w3.eth.gas_price,
    'nonce': w3.eth.get_transaction_count(WALLET),
})

private_key = ''

signed_txn = w3.eth.account.sign_transaction(tx, private_key)
transaction_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
transaction_receipt = w3.eth.wait_for_transaction_receipt(transaction_hash)

print('Transaction successful!')
print('Transaction hash:', transaction_receipt['transactionHash'].hex())
print('Gas used:', transaction_receipt['gasUsed'])
