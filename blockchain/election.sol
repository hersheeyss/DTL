// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Election {

    // Candidate ID => total votes
    mapping(uint256 => uint256) public votes;

    // address => did this address vote?
    mapping(address => bool) public hasVoted;

    event VoteSubmitted(address voter, uint256 candidateId);

    function vote(uint256 candidateId) public {
        require(!hasVoted[msg.sender], "You already voted!");
        require(candidateId == 1 || candidateId == 2 || candidateId == 3, "Invalid candidate");

        hasVoted[msg.sender] = true;
        votes[candidateId] += 1;

        emit VoteSubmitted(msg.sender, candidateId);
    }

    function getVotes(uint256 candidateId) public view returns (uint256) {
        return votes[candidateId];
    }
}
