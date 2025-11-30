const connectBtn = document.getElementById("connectWalletBtn");
const walletStatus = document.getElementById("walletStatus");
const submitVoteBtn = document.getElementById("submitVoteBtn");
const statusEl = document.getElementById("status");

let userAccount = null;


// ---------------- CONNECT METAMASK ----------------
connectBtn.addEventListener("click", async () => {
    if (window.ethereum) {
        try {
            const accounts = await window.ethereum.request({
                method: "eth_requestAccounts"
            });

            userAccount = accounts[0];
            walletStatus.textContent = "Wallet: " + shorten(userAccount);

            connectBtn.textContent = "Connected";
            connectBtn.disabled = true;

            statusEl.textContent = "Wallet connected!";
            statusEl.classList.add("success");

        } catch (err) {
            statusEl.textContent = "MetaMask connection denied!";
            statusEl.classList.add("error");
        }

    } else {
        statusEl.textContent = "MetaMask not installed!";
        statusEl.classList.add("error");
    }
});


// Shorten wallet address
function shorten(addr) {
    return addr.slice(0, 6) + "..." + addr.slice(-4);
}


// ---------------- CAST VOTE ----------------
submitVoteBtn.addEventListener("click", async () => {
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

    // Show animation box
    const animation = document.getElementById("voteAnimation");
    animation.classList.remove("hidden");

    // Send vote to Flask API
    const response = await fetch("/cast_vote", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({candidate_id: candidateId})
    });

    const result = await response.json();

    // Finish animation
    setTimeout(() => {
        animation.classList.add("hidden");

        if (result.status === "success") {
            statusEl.textContent = "Vote successfully cast!";
            statusEl.classList.add("success");

            // redirect to dashboard
            setTimeout(() => {
                window.location.href = "/dashboard";
            }, 2000);

        } else {
            statusEl.textContent = result.message;
            statusEl.classList.add("error");
        }

    }, 1500);
});


