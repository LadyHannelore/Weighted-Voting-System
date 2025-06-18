#!/usr/bin/env python
"""
Full Version Test - UK Weighted Voting System without Charts

Testing the full system with 30-second rounds but without visualization
to avoid any import issues.
"""

from collections import Counter

# Import from the vote_types module
from vote_types import VoterProfile, WeightCoefficients, Candidate
from election import run_election, run_weighted_yes_no_election, verify_voting_system


def main_no_charts():
    """
    Run the weighted voting system simulation without charts.
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

    # Smaller set of ballots for the full demo
    ballots = []

    # England - Urban/North (Labour leaning)
    for _ in range(15):
        ballots.append(["labour", "green", "libdem", "conservative", "reform"])
        ballots.append(["labour", "libdem", "green", "conservative", "reform"])

    # England - South East (Conservative leaning)
    for _ in range(12):
        ballots.append(["conservative", "libdem", "reform", "labour", "green"])
        ballots.append(["conservative", "reform", "libdem", "labour", "green"])

    # Reform-first voters
    for _ in range(8):
        ballots.append(["reform", "conservative", "labour", "libdem", "green"])

    print(f"Total ballots: {len(ballots)}")
    counter = Counter([ballot[0] for ballot in ballots])
    print("First preferences distribution:")
    for party, count in counter.items():
        print(f"  {party}: {count} votes ({count / len(ballots) * 100:.1f}%)")

    # UK voter profiles based on demographic segments
    profiles = [
        VoterProfile(id='urban_professionals', E=8, P=70, D=7, A=6, S=80),
        VoterProfile(id='rural_voters', E=7, P=75, D=8, A=7, S=90),
        VoterProfile(id='students', E=6, P=40, D=5, A=6, S=85),
        VoterProfile(id='retirees', E=7, P=90, D=8, A=7, S=95),
        VoterProfile(id='young_professionals', E=7, P=60, D=6, A=7, S=75),
        VoterProfile(id='working_class', E=6, P=65, D=7, A=8, S=90),
        VoterProfile(id='business_owners', E=8, P=80, D=7, A=6, S=95),
        VoterProfile(id='public_sector', E=8, P=85, D=7, A=8, S=85),
        VoterProfile(id='first_time_voters', E=4, P=10, D=4, A=6, S=70)
    ]

    # Define coefficient weights
    coeffs_equal = WeightCoefficients(wE=0.2, wP=0.2, wD=0.2, wA=0.2, wS=0.2)
    coeffs_expert = WeightCoefficients(wE=0.4, wP=0.3, wD=0.1, wA=0.1, wS=0.1)
    coeffs_stake = WeightCoefficients(wE=0.1, wP=0.1, wD=0.1, wA=0.3, wS=0.4)

    # Define bounds
    bounds = {
        "min": VoterProfile(id='', E=0, P=0, D=0, A=0, S=0),
        "max": VoterProfile(id='', E=10, P=100, D=10, A=10, S=100)
    }

    # Weighted yes/no vote simulation
    print("\n" + "=" * 50)
    print("SIMULATION 1: WEIGHTED YES/NO VOTE ON 'UK REJOINING THE EU'")
    print("=" * 50)

    yes_ids = [
        'urban_professionals',
        'students',
        'young_professionals',
        'public_sector',
        'first_time_voters']
    no_ids = ['rural_voters', 'retirees', 'working_class', 'business_owners']

    result_equal = run_weighted_yes_no_election(
        profiles, yes_ids, no_ids, coeffs_equal, 0.5, bounds)
    result_expert = run_weighted_yes_no_election(
        profiles, yes_ids, no_ids, coeffs_expert, 0.5, bounds)
    result_stake = run_weighted_yes_no_election(
        profiles, yes_ids, no_ids, coeffs_stake, 0.5, bounds)

    print(
        f"\n1. Equal weights: {
            result_equal['passed']} ({
            result_equal['total_yes']:.2f} vs {
                result_equal['total_no']:.2f})")
    print(
        f"2. Expertise focus: {
            result_expert['passed']} ({
            result_expert['total_yes']:.2f} vs {
                result_expert['total_no']:.2f})")
    print(
        f"3. Stake focus: {
            result_stake['passed']} ({
            result_stake['total_yes']:.2f} vs {
                result_stake['total_no']:.2f})")

    # Run the ranked choice election simulation
    print("\n" + "=" * 50)
    print("SIMULATION 2: RANKED CHOICE VOTING FOR UK PARTIES (30-second rounds)")
    print("=" * 50)

    print("⚠️  Note: Each round will last 30 seconds. You can interrupt with Ctrl+C if needed.")

    try:
        results = run_election(candidates, ballots, round_duration=30)
        print(
            f"\n🏆 Final Winner: {
                results.winner.name if results.winner else 'No winner'}")
    except KeyboardInterrupt:
        print("\n⏹️  Election interrupted by user.")
        return

    print("\n✅ Full simulation completed!")


if __name__ == "__main__":
    print("🗳️  Starting Full UK Weighted Voting System Demo...")
    main_no_charts()
