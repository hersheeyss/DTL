const connectBtn = document.getElementById("connectWalletBtn");
const walletStatus = document.getElementById("walletStatus");
const submitVoteBtn = document.getElementById("submitVoteBtn");
const statusEl = document.getElementById("status");

let userAccount = null;

// ---------------------- BEAUTIFUL POPUP ----------------------
function showPopup(title, message, color = "blue") {
    const div = document.createElement("div");
    div.style.position = "fixed";
    div.style.bottom = "20px";
    div.style.right = "20px";
    div.style.padding = "15px 20px";
    div.style.background = color;
    div.style.color = "white";
    div.style.borderRadius = "10px";
    div.style.boxShadow = "0 4px 12px rgba(0,0,0,0.3)";
    div.style.fontSize = "16px";
    div.style.zIndex = 9999;

    div.innerHTML = `<b>${title}</b><br>${message}`;

    document.body.appendChild(div);

    setTimeout(() => {
        div.remove();
    }, 2500);
}

// ---------------------- CONNECT METAMASK ----------------------
connectBtn.addEventListener("click", async () => {
    
    if (!window.ethereum) {
        showPopup("MetaMask Missing", "Please install MetaMask!", "red");
        return;
    }

    try {
        const accounts = await window.ethereum.request({
            method: "eth_requestAccounts"
        });

        userAccount = accounts[0];

        walletStatus.textContent =
            "Connected: " + userAccount.slice(0, 6) + "..." + userAccount.slice(-4);

        connectBtn.textContent = "Connected ✔";
        connectBtn.disabled = true;

        showPopup("Success", "Wallet connected!", "green");

    } catch (err) {
        showPopup("Failed", "User denied connection!", "red");
    }
});

// ---------------------- SUBMIT VOTE ----------------------
submitVoteBtn.addEventListener("click", async () => {
    statusEl.textContent = "";

    if (!userAccount) {
        showPopup("Error", "Please connect MetaMask first!", "red");
        return;
    }

    const selected = document.querySelector('input[name="candidate"]:checked');

    if (!selected) {
        showPopup("Error", "Select a candidate!", "red");
        return;
    }

    showPopup("Please wait", "Submitting vote to blockchain...", "blue");

    try {
        const response = await fetch("/cast_vote", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ candidate_id: selected.value })
        });

        const result = await response.json();

        if (result.status === "success") {
            showPopup("Success", "Vote submitted!", "green");

            setTimeout(() => {
                window.location.href = "/dashboard";
            }, 1200);

        } else {
            showPopup("Error", result.message, "red");
        }

    } catch (err) {
        showPopup("Failed", "Voting failed!", "red");
    }
});


