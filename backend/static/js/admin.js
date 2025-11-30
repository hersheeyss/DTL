const refreshBcBtn = document.getElementById("refreshBcBtn");
const pushBtn = document.getElementById("pushBtn");

function adminPopup(msg) {
    alert(msg);
}

// ------------------- REFRESH BLOCKCHAIN COUNTS -------------------
refreshBcBtn.addEventListener("click", async () => {
    try {
        const res = await fetch("/admin/blockchain_results");
        const data = await res.json();

        if (data.status === "ok") {
            document.getElementById("bc1").textContent = data.data["1"];
            document.getElementById("bc2").textContent = data.data["2"];
            document.getElementById("bc3").textContent = data.data["3"];
            adminPopup("Blockchain counts refreshed!");
        } else {
            adminPopup("Error refreshing blockchain results.");
        }
    } catch (e) {
        adminPopup("Network error while refreshing blockchain.");
    }
});


// ------------------- PUSH DB → BLOCKCHAIN -------------------
pushBtn.addEventListener("click", async () => {

    if (!window.ethereum) {
        return adminPopup("MetaMask is required to push votes.");
    }

    // Fetch DB results
    let res = await fetch("/admin/db_results");
    let data = await res.json();

    if (data.status !== "ok") {
        return adminPopup("Could not fetch DB counts.");
    }

    const counts = data.data; // { "1": x, "2": y, "3": z }

    // NEW CONTRACT
    const contractAddress = "0xe95351ae58db4575eefbD1c78e4324A3F1914f2e";

    const ABI = [
        {
            "inputs": [{"internalType": "uint256", "name": "candidateId", "type": "uint256"}],
            "name": "castVote",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "anonymous": false,
            "inputs": [
                {"indexed": false, "internalType": "uint256", "name": "candidateId", "type": "uint256"}
            ],
            "name": "VoteCasted",
            "type": "event"
        },
        {
            "inputs": [{"internalType": "uint256", "name": "candidateId", "type": "uint256"}],
            "name": "getVotes",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "name": "votes",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function"
        }
    ];

    try {
        const provider = new ethers.BrowserProvider(window.ethereum);
        await provider.send("eth_requestAccounts", []); // opens MetaMask

        const signer = await provider.getSigner();
        const contract = new ethers.Contract(contractAddress, ABI, signer);

        let log = "Pushing votes...\n";

        for (let cid of [1, 2, 3]) {
            let numVotes = counts[String(cid)] || 0;
            log += `Candidate ${cid}: pushing ${numVotes} votes\n`;

            for (let i = 0; i < numVotes; i++) {
                const tx = await contract.castVote(cid);
                await tx.wait();
            }
        }

        adminPopup("DONE!\n\n" + log);

    } catch (err) {
        console.error(err);
        adminPopup("Failed to push votes:\n" + err.message);
    }
});



