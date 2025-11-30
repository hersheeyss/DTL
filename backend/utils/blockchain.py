import requests
from eth_utils import keccak

ALCHEMY_URL = "https://eth-sepolia.g.alchemy.com/v2/TEkkZ3BRzreVg2_AWzKIp"
CONTRACT_ADDRESS = "0x9BACc0331f680B9f4d2bE8C7E18A6baeE8dC23aA"

def encode_uint256(value: int):
    return value.to_bytes(32, 'big').hex()

def selector(signature: str):
    return keccak(text=signature).hex()[:8]

def call_getVotes(candidate_id: int):
    function_selector = selector("getVotes(uint256)")
    encoded_arg = encode_uint256(candidate_id)
    data = "0x" + function_selector + encoded_arg

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_call",
        "params": [
            {"to": CONTRACT_ADDRESS, "data": data},
            "latest"
        ]
    }

    try:
        response = requests.post(ALCHEMY_URL, json=payload).json()
        result_hex = response.get("result", "0x0")
        return int(result_hex, 16)
    except Exception as e:
        print("RPC ERROR:", e)
        return 0
