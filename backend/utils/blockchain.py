import requests
from eth_utils import keccak

# Your Alchemy Sepolia RPC URL
ALCHEMY_URL = "https://eth-sepolia.g.alchemy.com/v2/TEkkZ3BRzreVg2_AWzKIp"

# NEW deployed voting contract address
CONTRACT_ADDRESS = "0xe95351ae58db4575eefbD1c78e4324A3F1914f2e"


def encode_uint256(value: int) -> str:
    return value.to_bytes(32, "big").hex()


def selector(signature: str) -> str:
    """First 4 bytes of keccak(functionSignature)."""
    return keccak(text=signature).hex()[:8]


def get_blockchain_votes(candidate_id: int) -> int:
    """
    Calls getVotes(uint256) on your contract using eth_call via Alchemy.
    No gas / no ETH needed (read-only).
    """
    function_selector = selector("getVotes(uint256)")
    encoded_arg = encode_uint256(candidate_id)
    data = "0x" + function_selector + encoded_arg

    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_call",
        "params": [
            {
                "to": CONTRACT_ADDRESS,
                "data": data
            },
            "latest"
        ]
    }

    try:
        response = requests.post(ALCHEMY_URL, json=payload).json()
        result_hex = response.get("result", "0x0")
        return int(result_hex, 16)
    except Exception as e:
        print("Blockchain read error:", e)
        return 0



