# ---- FIX for Python 3.12 (Web3 Mapping ImportError) ----
import collections
import collections.abc

collections.Mapping = collections.abc.Mapping
collections.MutableMapping = collections.abc.MutableMapping
collections.Sequence = collections.abc.Sequence
# --------------------------------------------------------

from web3 import Web3


RPC_URL = "https://eth-sepolia.g.alchemy.com/v2/TEkkZ3BRzreVg2_AWzKIp"
CONTRACT_ADDRESS = "0x9BACc0331f680B9f4d2bE8C7E18A6baeE8dC23aA"
PRIVATE_KEY = "34fa044d0de0a7ac6767a6a66492a35e7a86da7495dc1f9a60f2221d1cad7a6e"
CHAIN_ID = 11155111

ABI = [
	{
		"inputs":[{"internalType":"uint256","name":"candidateId","type":"uint256"}],
		"name":"castVote","outputs":[],"stateMutability":"nonpayable","type":"function"
	},
	{
		"anonymous":False,
		"inputs":[{"indexed":False,"internalType":"uint256","name":"candidateId","type":"uint256"}],
		"name":"VoteCasted","type":"event"
	},
	{
		"inputs":[{"internalType":"uint256","name":"candidateId","type":"uint256"}],
		"name":"getVotes",
		"outputs":[{"internalType":"uint256","name":"","type":"uint256"}],
		"stateMutability":"view",
		"type":"function"
	},
	{
		"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],
		"name":"votes",
		"outputs":[{"internalType":"uint256","name":"","type":"uint256"}],
		"stateMutability":"view",
		"type":"function"
	}
]

web3 = Web3(Web3.HTTPProvider(RPC_URL))
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=ABI)


def send_vote_tx(candidate_id):
    account = web3.eth.account.from_key(PRIVATE_KEY)
    nonce = web3.eth.get_transaction_count(account.address)

    tx = contract.functions.castVote(candidate_id).build_transaction({
        "chainId": CHAIN_ID,
        "from": account.address,
        "nonce": nonce,
        "gas": 200000,
        "maxFeePerGas": web3.to_wei("2", "gwei"),
        "maxPriorityFeePerGas": web3.to_wei("1", "gwei")
    })

    signed = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed.rawTransaction)
    return tx_hash.hex()
