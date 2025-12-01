// ------------------------------------------------------
// SMART CONTRACT CONFIG
// ------------------------------------------------------

// YOUR CONTRACT ON SEPOLIA
let CONTRACT_ADDRESS = "0x02Fd7C0721D228b5EC2cb00564C22BC2c571760C";

// Allow override from localStorage
const saved = localStorage.getItem("contract_override");
if (saved && /^0x[a-fA-F0-9]{40}$/.test(saved)) {
    CONTRACT_ADDRESS = saved;
}

// Basic Election Contract ABI
const CONTRACT_ABI = [
    {
        "inputs":[{"internalType":"uint256","name":"candidateId","type":"uint256"}],
        "name":"vote",
        "outputs":[],
        "stateMutability":"nonpayable",
        "type":"function"
    },
    {
        "inputs":[{"internalType":"uint256","name":"candidateId","type":"uint256"}],
        "name":"getVotes",
        "outputs":[{"internalType":"uint256","name":"","type":"uint256"}],
        "stateMutability":"view",
        "type":"function"
    },
    {
        "inputs":[{"internalType":"address","name":"","type":"address"}],
        "name":"hasVoted",
        "outputs":[{"internalType":"bool","name":"","type":"bool"}],
        "stateMutability":"view",
        "type":"function"
    }
];


// SEPOLIA NETWORK CONFIG
window.DEFAULT_CHAIN = {
    chainIdDec: 11155111,
    chainIdHex: "0xAA36A7",
    rpcUrls: ["https://rpc.sepolia.org"],
    blockExplorerUrls: ["https://sepolia.etherscan.io"]
};


// EXPOSE TO ALL FILES
window.CONTRACT_ADDRESS = CONTRACT_ADDRESS;
window.CONTRACT_ABI = CONTRACT_ABI;

