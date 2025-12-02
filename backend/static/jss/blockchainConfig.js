// ===============================
// CONTRACT ADDRESS (SEPOLIA)
// ===============================
let CONTRACT_ADDRESS = "0x02Fd7C0721D228b5EC2cb00564C22BC2c571760C";
// ^^^^^ YOUR DEPLOYED CONTRACT ADDRESS


// ===============================
// DEFAULT CHAIN (SEPOLIA)
// ===============================
window.DEFAULT_CHAIN = {
    chainIdHex: "0xAA36A7",
    chainIdDec: 11155111,
    chainName: "Sepolia Testnet",
    nativeCurrency: { name: "Sepolia Ether", symbol: "SEP", decimals: 18 },

    // Use ONLY stable RPCs
    rpcUrls: [
        "https://1rpc.io/sepolia",
        "https://rpc2.sepolia.org",
        "https://rpc-sepolia.rockx.com"
    ],

    blockExplorerUrls: [
        "https://sepolia.etherscan.io"
    ]
};


// ===============================
// CONTRACT ABI
// ===============================
const CONTRACT_ABI = [
    {
        "inputs": [{ "internalType": "uint256", "name": "candidateId", "type": "uint256" }],
        "name": "vote",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{ "internalType": "uint256", "name": "candidateId", "type": "uint256" }],
        "name": "getVotes",
        "outputs": [{ "internalType": "uint256", "name": "", "type": "uint256" }],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{ "internalType": "address", "name": "", "type": "address" }],
        "name": "hasVoted",
        "outputs": [{ "internalType": "bool", "name": "", "type": "bool" }],
        "stateMutability": "view",
        "type": "function"
    }
];

window.CONTRACT_ABI = CONTRACT_ABI;
window.CONTRACT_ADDRESS = CONTRACT_ADDRESS;



