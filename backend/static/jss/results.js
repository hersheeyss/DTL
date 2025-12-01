const v1 = document.getElementById("v1");
const v2 = document.getElementById("v2");
const v3 = document.getElementById("v3");
const winnerText = document.getElementById("winnerText");

const card1 = document.getElementById("card1");
const card2 = document.getElementById("card2");
const card3 = document.getElementById("card3");

const chartEl = document.getElementById("resultsChart");
let chart = null;


// FETCH VOTES
async function fetchVotes() {
    try {
        const provider = new ethers.JsonRpcProvider(window.DEFAULT_CHAIN.rpcUrls[0]);
        const contract = new ethers.Contract(window.CONTRACT_ADDRESS, window.CONTRACT_ABI, provider);

        const [a, b, c] = await Promise.all([
            contract.getVotes(1),
            contract.getVotes(2),
            contract.getVotes(3)
        ]);

        return [Number(a), Number(b), Number(c)];
    } catch {
        return [0, 0, 0];
    }
}


// UPDATE UI
function updateLeader(a, b, c) {
    const max = Math.max(a, b, c);

    // Remove old glow
    card1.classList.remove("leader");
    card2.classList.remove("leader");
    card3.classList.remove("leader");

    if (a === max && b === max && c === max) {
        winnerText.textContent = "Three-way Tie!";
        return;
    }
    if (a === max && b === max) {
        winnerText.textContent = "Tie: Candidate One & Two";
        return;
    }
    if (a === max && c === max) {
        winnerText.textContent = "Tie: Candidate One & Three";
        return;
    }
    if (b === max && c === max) {
        winnerText.textContent = "Tie: Candidate Two & Three";
        return;
    }

    // Single winner highlight
    if (a === max) {
        winnerText.textContent = "Winner: Candidate One";
        card1.classList.add("leader");
    }
    else if (b === max) {
        winnerText.textContent = "Winner: Candidate Two";
        card2.classList.add("leader");
    }
    else {
        winnerText.textContent = "Winner: Candidate Three";
        card3.classList.add("leader");
    }
}


// RENDER FUNCTION
async function renderResults() {
    const [a, b, c] = await fetchVotes();

    v1.textContent = a;
    v2.textContent = b;
    v3.textContent = c;

    updateLeader(a, b, c);

    const data = {
        labels: ["Candidate One", "Candidate Two", "Candidate Three"],
        datasets: [{
            label: "Votes",
            data: [a, b, c],
            backgroundColor: ["#4f46e5", "#22c55e", "#f97316"]
        }]
    };

    if (!chart) {
        chart = new Chart(chartEl, {
            type: "bar",
            data,
            options: { scales: { y: { beginAtZero: true } } }
        });
    } else {
        chart.data = data;
        chart.update();
    }
}


// FIRST LOAD + AUTO REFRESH
renderResults();
setInterval(renderResults, 5000);


