// =====================================================================
// POPUP SYSTEM
// =====================================================================
function showPopup(title, msg) {
    document.getElementById("popupTitle").textContent = title;
    document.getElementById("popupMsg").textContent = msg;
    document.getElementById("popupOverlay").classList.remove("hidden");
}

document.getElementById("popupClose").onclick = () => {
    document.getElementById("popupOverlay").classList.add("hidden");
};


// =====================================================================
// GLOBALS
// =====================================================================
let provider = null;
let signer = null;
let userAddress = null;
let contract = null;

const connectBtn = document.getElementById("connectWalletBtn");
const walletDisplay = document.getElementById("walletDisplay");
const submitVoteBtn = document.getElementById("submitVoteBtn");


// =====================================================================
// FASTEST CANDIDATE SELECTION (NO LAG, NO DOUBLE EVENTS)
// =====================================================================
document.querySelectorAll(".candidate-card").forEach(card => {

    // Click anywhere on card
    card.addEventListener("click", () => {
        document.querySelectorAll(".candidate-card")
            .forEach(c => c.classList.remove("selected"));

        card.classList.add("selected");
        card.querySelector(".hidden-radio").checked = true;
    });

    // Select button inside card
    card.querySelector(".select-btn").addEventListener("click", (e) => {
        e.stopPropagation();
        card.click();
    });
});


// =====================================================================
// CONNECT WALLET
// =====================================================================
connectBtn.addEventListener("click", async () => {
    if (!window.ethereum) {
        showPopup("MetaMask Not Found", "Please install MetaMask to continue.");
        return;
    }

    try {
        provider = new ethers.BrowserProvider(window.ethereum);
        await provider.send("eth_requestAccounts", []);

        signer = await provider.getSigner();
        userAddress = await signer.getAddress();

        walletDisplay.textContent =
            "Wallet: " + userAddress.slice(0, 6) + "..." + userAddress.slice(-4);

        connectBtn.disabled = true;
        connectBtn.textContent = "Connected";

        contract = new ethers.Contract(
            window.CONTRACT_ADDRESS,
            window.CONTRACT_ABI,
            signer
        );

    } catch (err) {
        showPopup("Connection Error", err.message);
    }
});


// =====================================================================
// SUBMIT VOTE
// =====================================================================
submitVoteBtn.addEventListener("click", async () => {

    if (!contract) {
        showPopup("Wallet Not Connected", "Please connect MetaMask before voting.");
        return;
    }

    const selected = document.querySelector('input[name="candidate"]:checked');
    if (!selected) {
        showPopup("No Candidate Selected", "Please choose a candidate first.");
        return;
    }

    const candidateId = parseInt(selected.value);


    try {
        // Check if already voted (client-side)
        const already = await contract.hasVoted(userAddress);
        if (already) {
            showPopup("Already Voted", "You already voted once.");
            return;
        }

        // Ask MetaMask
        showPopup("Confirm Vote", "Please confirm your vote in MetaMask...");

        const tx = await contract.vote(candidateId);
        await tx.wait();

        showPopup("Success!", "Your vote has been recorded.");

        setTimeout(() => {
            window.location.href = "/dashboard";
        }, 1600);


    } catch (err) {

        console.log("TX ERROR:", err);

        // =================================================================
        // USER REJECTED / CANCELLED
        // =================================================================
        if (
            err.code === 4001 ||
            err.code === "ACTION_REJECTED" ||
            (err.message && err.message.toLowerCase().includes("user rejected")) ||
            (err.info && err.info.error && err.info.error.code === 4001)
        ) {
            showPopup("Transaction Cancelled", "You rejected the transaction.");
            return;
        }

        // =================================================================
        // ALREADY VOTED (CONTRACT REVERT)
        // =================================================================
        if (
            (err.message && err.message.toLowerCase().includes("already voted")) ||
            (err.shortMessage && err.shortMessage.toLowerCase().includes("already voted")) ||
            (err.info && err.info.error && err.info.error.message &&
             err.info.error.message.toLowerCase().includes("already voted"))
        ) {
            showPopup("Already Voted", "You already voted once.");
            return;
        }

        // =================================================================
        // Closed MetaMask Window
        // =================================================================
        if (err.message && err.message.includes("denied transaction signature")) {
            showPopup("Transaction Cancelled", "You closed MetaMask before signing.");
            return;
        }

        // =================================================================
        // FALLBACK CLEAN ERROR
        // =================================================================
        showPopup("Transaction Error", "Something went wrong while submitting your vote.");
    }


});





