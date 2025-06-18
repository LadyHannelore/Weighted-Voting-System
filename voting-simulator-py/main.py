#!/usr/bin/env python
"""
Weighted Voting System - UK Elections Simulator

This module serves as the main entry point for the weighted voting system simulation,
using real UK political party data from the 2024 general election.
"""

from collections import Counter

# Import from the vote_types module
from vote_types import VoterProfile, WeightCoefficients, Candidate
from election import run_election, run_weighted_yes_no_election, verify_voting_system
from visualization import (
    create_weighted_vote_chart, create_ranked_choice_visualization,
    create_voter_profile_heatmap, create_first_preferences_pie_chart,
    save_all_charts, display_charts_in_browser
)


def main():
    """
    Run the weighted voting system simulation with UK general election data.

    This function demonstrates both:
    1. A weighted yes/no vote on a specific policy
    2. A ranked choice election between major UK political parties
    using data from the 2024 general election.
    """
    # First, verify our voting system implementation
    verify_voting_system()

    # UK Political Parties as candidates (using parties with most candidates)
    candidates = [
        Candidate(id="conservative", name="Conservative and Unionist Party"),
        Candidate(id="labour", name="Labour Party"),
        Candidate(id="libdem", name="Liberal Democrats"),
        Candidate(id="reform", name="Reform UK"),
        Candidate(id="green", name="Green Party"),
        Candidate(id="snp", name="Scottish National Party"),
        Candidate(id="plaid", name="Plaid Cymru")
    ]

    # Simulated ballots based on regional preferences
    # Creating 100 ballots with realistic UK voting patterns
    ballots = []

    # England - South East (Conservative leaning)
    for _ in range(25):
        # Different preference orders to show regional variety
        ballots.append(["conservative", "libdem", "reform", "labour", "green"])
        ballots.append(["conservative", "reform", "libdem", "labour", "green"])
        ballots.append(["libdem", "conservative", "labour", "green", "reform"])

    # England - Urban/North (Labour leaning)
    for _ in range(30):
        ballots.append(["labour", "green", "libdem", "conservative", "reform"])
        ballots.append(["labour", "libdem", "green", "conservative", "reform"])
        ballots.append(["green", "labour", "libdem", "reform", "conservative"])

    # Scotland
    for _ in range(10):
        ballots.append(["snp", "labour", "green", "libdem", "conservative"])
        ballots.append(["labour", "snp", "libdem", "green", "conservative"])

    # Wales
    for _ in range(5):
        ballots.append(["labour", "plaid", "libdem", "green", "conservative"])
        ballots.append(["plaid", "labour", "green", "libdem", "conservative"])

    # Reform-first voters
    for _ in range(15):
        ballots.append(["reform", "conservative", "labour", "libdem", "green"])

    print(f"Total ballots: {len(ballots)}")
    counter = Counter([ballot[0] for ballot in ballots])
    print("First preferences distribution:")
    for party, count in counter.items():
        # UK voter profiles based on demographic segments
        print(f"  {party}: {count} votes ({count / len(ballots) * 100:.1f}%)")
    # E: expertise (political knowledge), P: participation (voting history),
    # D: decision quality (consistency), A: alignment (with general public
    # interest), S: stake (impact on voter)
    profiles = [
        # Urban professionals
        VoterProfile(id='urban_professionals', E=8, P=70, D=7, A=6, S=80),
        # Rural communities
        VoterProfile(id='rural_voters', E=7, P=75, D=8, A=7, S=90),
        # University students
        VoterProfile(id='students', E=6, P=40, D=5, A=6, S=85),
        # Retirees
        VoterProfile(id='retirees', E=7, P=90, D=8, A=7, S=95),
        # Young professionals
        VoterProfile(id='young_professionals', E=7, P=60, D=6, A=7, S=75),
        # Working class
        VoterProfile(id='working_class', E=6, P=65, D=7, A=8, S=90),
        # Business owners
        VoterProfile(id='business_owners', E=8, P=80, D=7, A=6, S=95),
        # Public sector workers
        VoterProfile(id='public_sector', E=8, P=85, D=7, A=8, S=85),
        # First-time voters
        VoterProfile(id='first_time_voters', E=4, P=10, D=4, A=6, S=70)
    ]

    # Define coefficient weights summing to 1
    # Simulation 1: Equal weighting
    coeffs_equal = WeightCoefficients(
        wE=0.2, wP=0.2, wD=0.2, wA=0.2, wS=0.2
    )

    # Simulation 2: Expertise and participation weighted heavily
    coeffs_expert = WeightCoefficients(
        wE=0.4, wP=0.3, wD=0.1, wA=0.1, wS=0.1
    )

    # Simulation 3: Stake and alignment weighted heavily
    coeffs_stake = WeightCoefficients(
        wE=0.1, wP=0.1, wD=0.1, wA=0.3, wS=0.4
    )

    # Using the equal weighting for this simulation
    coeffs = coeffs_equal

    # Define min/max bounds for normalization
    bounds = {
        "min": VoterProfile(id='', E=0, P=0, D=0, A=0, S=0),
        "max": VoterProfile(id='', E=10, P=100, D=10, A=10, S=100)
    }    # Simulate a yes/no vote on "UK Rejoining the EU" policy
    print("\n" + "=" * 50)
    print("SIMULATION 1: WEIGHTED YES/NO VOTE ON 'UK REJOINING THE EU'")
    print("=" * 50)

    # Define voting patterns by demographic
    yes_ids = [
        'urban_professionals',
        'students',
        'young_professionals',
        'public_sector',
        'first_time_voters']
    no_ids = ['rural_voters', 'retirees', 'working_class', 'business_owners']

    print("\nVoting Groups:")
    print("YES voters:", ", ".join(yes_ids))
    print("NO voters:", ", ".join(no_ids))

    # Run simulations with different weighting systems
    print("\nRunning vote with different weighting systems:")

    # Equal weights
    result_equal = run_weighted_yes_no_election(
        profiles, yes_ids, no_ids,
        coeffs_equal, 0.5,
        bounds
    )

    # Expert-biased weights
    result_expert = run_weighted_yes_no_election(
        profiles, yes_ids, no_ids,
        coeffs_expert, 0.5,
        bounds
    )

    # Stake-biased weights
    result_stake = run_weighted_yes_no_election(
        profiles, yes_ids, no_ids,
        coeffs_stake, 0.5,
        bounds
    )

    # Display yes/no results with different weighting systems
    print(f"\n1. Equal weights:")
    print(f"   Passed? {result_equal['passed']}")
    print(
        f"   YES: {
            result_equal['total_yes']:.3f} ({
            result_equal['total_yes'] /
            (
                result_equal['total_yes'] +
                result_equal['total_no']) *
            100:.1f}%)")
    print(
        f"   NO:  {
            result_equal['total_no']:.3f} ({
            result_equal['total_no'] /
            (
                result_equal['total_yes'] +
                result_equal['total_no']) *
            100:.1f}%)")

    print(f"\n2. Expertise-focused weights:")
    print(f"   Passed? {result_expert['passed']}")
    print(
        f"   YES: {
            result_expert['total_yes']:.3f} ({
            result_expert['total_yes'] /
            (
                result_expert['total_yes'] +
                result_expert['total_no']) *
            100:.1f}%)")
    print(
        f"   NO:  {
            result_expert['total_no']:.3f} ({
            result_expert['total_no'] /
            (
                result_expert['total_yes'] +
                result_expert['total_no']) *
            100:.1f}%)")

    print(f"\n3. Stake-focused weights:")
    print(f"   Passed? {result_stake['passed']}")
    print(
        f"   YES: {
            result_stake['total_yes']:.3f} ({
            result_stake['total_yes'] /
            (
                result_stake['total_yes'] +
                result_stake['total_no']) *
            100:.1f}%)")
    print(
        f"   NO:  {
            result_stake['total_no']:.3f} ({
            result_stake['total_no'] /
            (
                result_stake['total_yes'] +
                result_stake['total_no']) *
            100:.1f}%)")

    # Run the ranked choice election simulation
    print("\n" + "=" * 50)
    print("SIMULATION 2: RANKED CHOICE VOTING FOR UK PARTIES")
    print("=" * 50)

    results = run_election(candidates, ballots)

    print(f"\nWinner: {results.winner.name if results.winner else 'No winner'}")
    print("\nRound-by-round results:")

    for round_detail in results.round_details:
        round_num = round_detail["round"]
        print(f"\nRound {round_num}:")

        # Sort candidates by votes in descending order
        sorted_results = sorted(
            round_detail["tallies"].items(),
            key=lambda x: x[1],
            reverse=True)

        # Calculate total votes
        total_votes = sum(round_detail["tallies"].values())

        # Print each candidate's results
        for candidate_id, votes in sorted_results:
            # Find the candidate name
            candidate_name = next(
                (c.name for c in candidates if c.id == candidate_id),
                candidate_id)
            # Calculate and display percentage
            percentage = (votes / total_votes) * 100 if total_votes > 0 else 0
            print(f"  {candidate_name}: {votes} votes ({percentage:.1f}%)")
            # Show elimination if applicable
        if "eliminated" in round_detail:
            eliminated_id = round_detail["eliminated"]
            eliminated_name = next(
                (c.name for c in candidates if c.id == eliminated_id),
                eliminated_id)
            print(f"  Eliminated: {eliminated_name}")

    # Generate visualizations
    print("\n" + "=" * 50)
    print("GENERATING CHARTS AND VISUALIZATIONS")
    print("=" * 50)

    charts = {}

    # 1. Weighted voting comparison chart
    weighted_results = {
        "Equal Weights": result_equal,
        "Expertise Focus": result_expert,
        "Stake Focus": result_stake
    }
    charts["Weighted Vote Comparison"] = create_weighted_vote_chart(
        weighted_results,
        "UK Rejoining EU - Different Weighting Systems"
    )

    # 2. Ranked choice visualization
    charts["Ranked Choice Results"] = create_ranked_choice_visualization(
        results, candidates)

    # 3. Voter profile heatmap
    charts["Voter Profiles"] = create_voter_profile_heatmap(profiles)

    # 4. First preferences pie chart
    charts["First Preferences"] = create_first_preferences_pie_chart(
        ballots, candidates)

    # Save charts to files
    save_all_charts(charts)

    # Display charts in browser
    print("\n📊 Opening charts in your default web browser...")
    try:
        display_charts_in_browser(charts)
        print("✅ Charts displayed successfully!")
    except Exception as e:
        print(f"⚠️  Could not display charts in browser: {e}")
        print("📁 Charts have been saved as HTML files in the 'charts' directory")

    print("\n🎯 Simulation completed! Check the 'charts' directory for saved visualizations.")


if __name__ == "__main__":
    main()
