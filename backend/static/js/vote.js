const connectBtn = document.getElementById("connectWalletBtn");
const walletStatus = document.getElementById("walletStatus");
const submitVoteBtn = document.getElementById("submitVoteBtn");
const statusEl = document.getElementById("status");

let userAccount = null;


// Connect MetaMask
connectBtn.addEventListener("click", async () => {
    if (window.ethereum) {
        try {
            const accounts = await window.ethereum.request({
                method: "eth_requestAccounts"
            });

            userAccount = accounts[0];

            walletStatus.textContent = "Wallet: " + formatWallet(userAccount);
            connectBtn.textContent = "Connected";
            connectBtn.disabled = true;

            statusEl.textContent = "Wallet connected!";
            statusEl.classList.add("success");

        } catch (error) {
            statusEl.textContent = "MetaMask connection denied.";
            statusEl.classList.add("error");
        }
    } else {
        statusEl.textContent = "MetaMask is not installed.";
        statusEl.classList.add("error");
    }
});


// Shorten wallet for UI
function formatWallet(addr) {
    return addr.slice(0, 6) + "..." + addr.slice(-4);
}


// Cast Vote
submitVoteBtn.addEventListener("click", () => {
    statusEl.textContent = "";
    statusEl.classList.remove("error", "success");

    if (!userAccount) {
        statusEl.textContent = "Please connect MetaMask first.";
        statusEl.classList.add("error");
        return;
    }

    const selected = document.querySelector('input[name="candidate"]:checked');

    if (!selected) {
        statusEl.textContent = "Please select a candidate!";
        statusEl.classList.add("error");
        return;
    }

    const candidateId = selected.value;

    // Animation
    const animation = document.getElementById("voteAnimation");
    animation.classList.remove("hidden");

    setTimeout(() => {
        animation.classList.add("hidden");

        statusEl.textContent = "Vote successfully cast!";
        statusEl.classList.add("success");

    }, 1500);
});
