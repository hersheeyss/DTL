const connectBtn = document.getElementById("connectWalletBtn");
const walletStatus = document.getElementById("walletStatus");
const submitVoteBtn = document.getElementById("submitVoteBtn");
const messageEl = document.getElementById("message");

let selectedAccount = null;

// Connect MetaMask
connectBtn.addEventListener("click", async () => {
    if (window.ethereum) {
        try {
            const accounts = await window.ethereum.request({
                method: "eth_requestAccounts"
            });
            selectedAccount = accounts[0];

            walletStatus.textContent = "Wallet: " + shorten(selectedAccount);
            connectBtn.textContent = "Connected";
            connectBtn.disabled = true;

        } catch {
            messageEl.textContent = "MetaMask connection denied.";
            messageEl.classList.add("error");
        }
    } else {
        messageEl.textContent = "MetaMask not installed.";
        messageEl.classList.add("error");
    }
});

// Shorten wallet address
function shorten(addr) {
    return addr.slice(0, 6) + "..." + addr.slice(-4);
}

// Vote button
submitVoteBtn.addEventListener("click", () => {
    messageEl.textContent = "";

    if (!selectedAccount) {
        messageEl.textContent = "Connect MetaMask first!";
        messageEl.classList.add("error");
        return;
    }

    const selected = document.querySelector('input[name="candidate"]:checked');
    if (!selected) {
        messageEl.textContent = "Please select a candidate.";
        messageEl.classList.add("error");
        return;
    }

    // Show animation
    const animation = document.getElementById("voteAnimation");
    animation.classList.remove("hidden");

    setTimeout(() => {
        animation.classList.add("hidden");
        messageEl.textContent = "Vote cast successfully!";
        messageEl.classList.add("success");
    }, 1500);
});
