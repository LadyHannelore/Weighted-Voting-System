#!/usr/bin/env python
"""
Weighted Voting System

This module serves as the main entry point for the weighted voting system simulation.
It demonstrates both weighted yes/no voting and ranked choice voting with voter profiles.
"""

import json

# Import from the vote_types module
from vote_types import VoterProfile, WeightCoefficients, Candidate, Ballot
from election import run_election, run_weighted_yes_no_election

def main():
    """
    Run the weighted voting system simulation with example data.
    
    This function demonstrates both the weighted yes/no voting mechanism
    and the ranked choice voting system.
    """
    # Load candidates and ballots from JSON or define inline
    candidates = [
        Candidate(id="candidate1", name="Candidate One"),
        Candidate(id="candidate2", name="Candidate Two"),
        Candidate(id="candidate3", name="Candidate Three")
    ]
    
    # Example ballots - each is a ranked list of candidate IDs
    ballots = [
        ["candidate1", "candidate2", "candidate3"],
        ["candidate2", "candidate1", "candidate3"],
        ["candidate1", "candidate3", "candidate2"]
    ]

    # Example voter profiles (scores must be in your defined raw ranges)
    profiles = [
        VoterProfile(id='alice', E=8, P=50, D=7, A=9, S=100),
        VoterProfile(id='bob', E=5, P=20, D=6, A=4, S=50),
        VoterProfile(id='carol', E=9, P=80, D=8, A=8, S=75)
    ]

    # Define coefficient weights summing to 1
    coeffs = WeightCoefficients(
        wE=0.3, wP=0.2, wD=0.3, wA=0.1, wS=0.1
    )

    # Define min/max bounds for normalization
    bounds = {
        "min": VoterProfile(id='', E=0, P=0, D=0, A=0, S=0),
        "max": VoterProfile(id='', E=10, P=100, D=10, A=10, S=100)
    }

    # Simulate a yes/no vote
    yes_ids = ['alice', 'carol']
    no_ids = ['bob']

    result = run_weighted_yes_no_election(
        profiles, yes_ids, no_ids,
        coeffs, 0.5,
        bounds
    )

    print(f"Passed? {result['passed']}")
    print(f"Weights yes/no: {result['total_yes']} / {result['total_no']}")

    results = run_election(candidates, ballots)
    print(f"Winner: {results.winner}")
    print(f"Details: {results.round_details}")

if __name__ == "__main__":
    main()
