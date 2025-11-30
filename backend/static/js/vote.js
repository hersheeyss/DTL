const connectBtn = document.getElementById("connectWalletBtn");
const walletStatus = document.getElementById("walletStatus");
const submitVoteBtn = document.getElementById("submitVoteBtn");
const statusEl = document.getElementById("status");

const popup = document.getElementById("popup");
const popupTitle = document.getElementById("popup-title");
const popupMessage = document.getElementById("popup-message");
const popupBtn = document.getElementById("popup-btn");

let userAccount = null;

/* ---------------------- POPUP FUNCTION ---------------------- */
function showPopup(title, message) {
    popupTitle.textContent = title;
    popupMessage.textContent = message;
    popup.classList.remove("hidden");
}

popupBtn.addEventListener("click", () => {
    popup.classList.add("hidden");
});

/* ---------------------- CONNECT METAMASK ---------------------- */
connectBtn.addEventListener("click", async () => {
    if (!window.ethereum) {
        return showPopup("MetaMask Missing", "Please install MetaMask to vote.");
    }

    try {
        const accounts = await window.ethereum.request({
            method: "eth_requestAccounts"
        });

        userAccount = accounts[0];

        walletStatus.textContent =
            "Wallet: " + userAccount.slice(0, 6) + "..." + userAccount.slice(-4);

        connectBtn.textContent = "Connected";
        connectBtn.disabled = true;

        showPopup("Wallet Connected", "Your MetaMask wallet is now linked!");
    } catch (err) {
        return showPopup("Connection Failed", "Could not connect MetaMask.");
    }
});

/* ---------------------- SEND VOTE TO BLOCKCHAIN ---------------------- */
async function sendVoteToBlockchain(candidateId) {
    const contractAddress = "0x9BACc0331f680B9f4d2bE8C7E18A6baeE8dC23aA";

    const ABI = [
        {
            "inputs": [{ "internalType": "uint256", "name": "candidateId", "type": "uint256" }],
            "name": "castVote",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ];

    const provider = new ethers.BrowserProvider(window.ethereum);
    const signer = await provider.getSigner();
    const contract = new ethers.Contract(contractAddress, ABI, signer);

    let tx = await contract.castVote(candidateId);
    await tx.wait(); // Wait for confirmation

    return tx.hash;
}

/* ---------------------- SUBMIT VOTE ---------------------- */
submitVoteBtn.addEventListener("click", async () => {
    if (!userAccount) {
        return showPopup("Wallet Not Connected", "Please connect MetaMask first!");
    }

    const selected = document.querySelector('input[name="candidate"]:checked');

    if (!selected) {
        return showPopup("No Candidate Selected", "Please select a candidate.");
    }

    const candidateId = parseInt(selected.value);

    try {
        showPopup("Processing", "Please confirm the transaction in MetaMask...");

        /* 1️⃣ Send vote to blockchain */
        let txHash = await sendVoteToBlockchain(candidateId);

        /* 2️⃣ Send vote to database (prevents double voting) */
        const response = await fetch("/cast_vote", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ candidate_id: candidateId })
        });

        const result = await response.json();

        if (result.status === "success") {
            showPopup("Vote Recorded", "Your vote is successfully stored on blockchain! 🗳️");

            setTimeout(() => {
                window.location.href = "/dashboard";
            }, 1500);

        } else if (result.message === "You have already voted!") {
            showPopup("Already Voted", "You can vote only one time!");
        } else {
            showPopup("Error", result.message);
        }

    } catch (err) {
        console.error(err);
        showPopup("Error", "Voting failed. Try again.");
    }
});

