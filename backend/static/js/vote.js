const submitVoteBtn = document.getElementById("submitVoteBtn");
const statusEl = document.getElementById("status");

const popup = document.getElementById("popup");
const popupTitle = document.getElementById("popup-title");
const popupMessage = document.getElementById("popup-message");
const popupBtn = document.getElementById("popup-btn");

function showPopup(title, message) {
    popupTitle.textContent = title;
    popupMessage.textContent = message;
    popup.classList.remove("hidden");
}

popupBtn.addEventListener("click", () => {
    popup.classList.add("hidden");
});

submitVoteBtn.addEventListener("click", async () => {
    const selected = document.querySelector('input[name="candidate"]:checked');

    if (!selected) {
        return showPopup("No Candidate Selected", "Please choose a candidate before submitting.");
    }

    const candidateId = parseInt(selected.value);

    try {
        const response = await fetch("/cast_vote", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ candidate_id: candidateId })
        });

        const result = await response.json();

        if (result.status === "success") {
            showPopup("Vote Submitted", "Your vote has been recorded successfully.");
            setTimeout(() => {
                window.location.href = "/dashboard";
            }, 1500);

        } else if (result.message === "You have already voted!") {
            showPopup("Already Voted", "You have already cast your vote. Only one vote is allowed.");
        } else {
            showPopup("Error", result.message || "Something went wrong.");
        }

    } catch (err) {
        console.error(err);
        showPopup("Error", "Unable to submit vote. Please try again.");
    }
});







