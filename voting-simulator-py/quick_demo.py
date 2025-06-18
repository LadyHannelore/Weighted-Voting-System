#!/usr/bin/env python
"""
Quick Demo Version of the UK Weighted Voting System

This is a fast demo version with 3-second rounds instead of 30-second rounds
for quick testing and demonstration purposes.
"""

from collections import Counter
from vote_types import Candidate
from election import run_election, verify_voting_system
from app import (
    get_uk_parties, get_voter_profiles, generate_ballots_for_election
)


def quick_demo():
    """
    Quick demo version with shorter round times for testing
    """
    # First, verify our voting system implementation
    verify_voting_system()

    # UK Political Parties as candidates (using parties with most candidates)
    candidates = [
        Candidate(id="conservative", name="Conservative and Unionist Party"),
        Candidate(id="labour", name="Labour Party"),
        Candidate(id="libdem", name="Liberal Democrats"),
        Candidate(id="reform", name="Reform UK"),
        Candidate(id="green", name="Green Party")
    ]

    # Smaller set of ballots for quicker demo
    ballots = [
        ["labour", "green", "libdem", "conservative", "reform"],
        ["labour", "libdem", "green", "conservative", "reform"],
        ["conservative", "libdem", "reform", "labour", "green"],
        ["conservative", "reform", "libdem", "labour", "green"],
        ["green", "labour", "libdem", "reform", "conservative"],
        ["libdem", "conservative", "labour", "green", "reform"],
        ["reform", "conservative", "labour", "libdem", "green"],
        ["labour", "green", "libdem", "conservative", "reform"],
        ["labour", "green", "libdem", "conservative", "reform"],
        ["conservative", "libdem", "reform", "labour", "green"]
    ]

    print(f"Quick Demo - Total ballots: {len(ballots)}")
    counter = Counter([ballot[0] for ballot in ballots])
    print("First preferences distribution:")
    for party, count in counter.items():
        print(f"  {party}: {count} votes ({count / len(ballots) * 100:.1f}%)")

    # Run the ranked choice election simulation with 3-second rounds
    print("\n" + "=" * 50)
    print("QUICK DEMO: RANKED CHOICE VOTING (3-second rounds)")
    print("=" * 50)

    results = run_election(candidates, ballots, round_duration=3)

    print(f"\n🏆 Final Winner: {results.winner.name if results.winner else 'No winner'}")


if __name__ == "__main__":
    print("🚀 Starting Quick Demo...")
    quick_demo()
