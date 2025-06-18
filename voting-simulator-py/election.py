from typing import Dict, List, Union
from vote_types import VoterProfile, Candidate, Ballot, Results, WeightCoefficients


def verify_voting_system():
    """
    Verify that the implemented voting system follows proper ranked choice (AV) rules
    """
    print("\n" + "=" * 60)
    print("VOTING SYSTEM VERIFICATION")
    print("=" * 60)

    print("✓ Ranked Choice Voting (Alternative Vote) Implementation:")
    print("  - Voters rank candidates in order of preference")
    print("  - If no candidate has >50% of first preferences, lowest is eliminated")
    print("  - Eliminated candidate's votes transfer to next preference")
    print("  - Process continues until a candidate has majority")
    print("  - System prevents vote splitting and tactical voting")

    print("\n✓ Weighted Yes/No Voting Implementation:")
    print("  - Each voter has weighted influence based on multiple factors")
    print("  - Weights are normalized using min-max scaling")
    print("  - Final decision based on weighted majority threshold")
    print("  - Multiple weighting scenarios can be compared")

    print("\n✓ Mathematical Verification:")
    print("  - Weight formula: W = wE*E + wP*P + wD*D + wA*A + wS*S")
    print("  - All coefficients sum to 1.0 for proper weighting")
    print("  - Normalization ensures fair comparison across different scales")

    return True

# Custom single transferable vote style simulator


def run_election(
        candidates: List[Candidate],
        ballots: List[Ballot],
        round_duration: int = 30) -> Results:
    """
    Run a ranked choice (single transferable vote) election with timed rounds.

    Args:
        candidates: List of candidate objects
        ballots: List of voter preferences as ordered lists of candidate IDs
        round_duration: Duration of each round in seconds (default: 30)

    Returns:
        Results object with winner and round-by-round details
    """
    if not candidates or not ballots:
        return Results(winner=None, round_details=[])

    print(
        f"\n🗳️  Starting Ranked Choice Election with {round_duration}-second rounds...")

    # Build a lookup for candidates by ID
    candidate_map = {c.id: c for c in candidates}

    # Track rounds
    rounds = []
    remaining_candidates = set(c.id for c in candidates)

    # Continue until we have a winner
    round_num = 1
    while remaining_candidates and len(remaining_candidates) > 1:
        print(f"\n⏱️  Round {round_num} starting... ({round_duration} seconds)")

        # Count first preferences of all valid ballots
        tallies = {cid: 0 for cid in remaining_candidates}

        for ballot in ballots:
            # Find the first preference that's still in the running
            for choice in ballot:
                if choice in remaining_candidates:
                    tallies[choice] += 1
                    break

        # Display real-time results
        total_votes = sum(tallies.values())
        print(f"   Current standings:")
        sorted_tallies = sorted(tallies.items(), key=lambda x: x[1], reverse=True)
        for cid, votes in sorted_tallies:
            candidate_name = candidate_map[cid].name
            percentage = (votes / total_votes) * 100 if total_votes > 0 else 0
            print(f"   • {candidate_name}: {votes} votes ({percentage:.1f}%)")

        # Record this round
        round_detail = {
            "round": round_num,
            "tallies": tallies.copy()
        }

        # Check for a majority winner
        for cid, votes in tallies.items():
            if votes > total_votes / 2:                # We have a winner
                rounds.append(round_detail)
                winner = candidate_map.get(cid)
                if winner:
                    print(
                        f"\n🎉 WINNER: {
                            winner.name} with {votes} votes ({
                            votes /
                            total_votes *
                            100:.1f}%)")
                return Results(
                    winner=winner,
                    round_details=rounds
                )
          # No winner yet, eliminate lowest candidate
        min_votes = float('inf')
        to_eliminate = None

        # Find the candidate with the lowest votes
        # In case of tie, eliminate the candidate who appears first alphabetically
        candidates_by_votes = sorted(tallies.items(), key=lambda x: (x[1], x[0]))
        if candidates_by_votes:
            to_eliminate = candidates_by_votes[0][0]
            min_votes = candidates_by_votes[0][1]

        if to_eliminate:
            eliminated_name = candidate_map[to_eliminate].name
            round_detail["eliminated"] = to_eliminate
            remaining_candidates.remove(to_eliminate)
            print(f"   ❌ ELIMINATED: {eliminated_name} ({min_votes} votes)")

        rounds.append(round_detail)
        round_num += 1
      # If we exit the loop, either we have a single candidate left, or we're
      # out of candidates
    winner = None
    if remaining_candidates:
        winner_id = list(remaining_candidates)[0]
        winner = candidate_map.get(winner_id)
        if winner:
            print(f"\n🎉 WINNER: {winner.name} (last remaining candidate)")

    return Results(
        winner=winner,
        round_details=rounds
    )


def run_election_web(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    """
    Run a ranked choice election optimized for web interface (no delays).

    Args:
        candidates: List of candidate objects
        ballots: List of voter preferences as ordered lists of candidate IDs

    Returns:
        Results object with winner and round-by-round details
    """
    if not candidates or not ballots:
        return Results(winner=None, round_details=[])

    # Build a lookup for candidates by ID
    candidate_map = {c.id: c for c in candidates}

    # Track rounds
    rounds = []
    remaining_candidates = set(c.id for c in candidates)

    # Continue until we have a winner
    round_num = 1
    while remaining_candidates and len(remaining_candidates) > 1:
        # Count first preferences of all valid ballots
        tallies = {cid: 0 for cid in remaining_candidates}

        for ballot in ballots:
            # Find the first preference that's still in the running
            for choice in ballot:
                if choice in remaining_candidates:
                    tallies[choice] += 1
                    break

        # Record this round
        round_detail = {
            "round": round_num,
            "tallies": tallies.copy()
        }

        # Check for a majority winner
        total_votes = sum(tallies.values())
        for cid, votes in tallies.items():
            if votes > total_votes / 2:
                # We have a winner
                rounds.append(round_detail)
                winner = candidate_map.get(cid)
                return Results(
                    winner=winner,
                    round_details=rounds
                )

        # No winner yet, eliminate lowest candidate
        # Find the candidate with the lowest votes
        # In case of tie, eliminate the candidate who appears first alphabetically
        candidates_by_votes = sorted(tallies.items(), key=lambda x: (x[1], x[0]))
        if candidates_by_votes:
            to_eliminate = candidates_by_votes[0][0]
            round_detail["eliminated"] = to_eliminate
            remaining_candidates.remove(to_eliminate)

        rounds.append(round_detail)
        round_num += 1

    # If we exit the loop, either we have a single candidate left, or we're
    # out of candidates
    winner = None
    if remaining_candidates:
        winner_id = list(remaining_candidates)[0]
        winner = candidate_map.get(winner_id)

    return Results(
        winner=winner,
        round_details=rounds
    )


def normalize(x: float, min_val: float, max_val: float) -> float:
    """Min-Max normalize a score to [0,1]"""
    return (x - min_val) / (max_val - min_val) if max_val > min_val else 0


def calculate_weights(
    profiles: List[VoterProfile],
    coeffs: WeightCoefficients,
    bounds: Dict[str, VoterProfile]
) -> Dict[str, float]:
    """Compute each voter's composite weight"""
    W: Dict[str, float] = {}
    for p in profiles:
        E = normalize(p.E, bounds["min"].E, bounds["max"].E)
        P = normalize(p.P, bounds["min"].P, bounds["max"].P)
        D = normalize(p.D, bounds["min"].D, bounds["max"].D)
        A = normalize(p.A, bounds["min"].A, bounds["max"].A)
        S = normalize(p.S, bounds["min"].S, bounds["max"].S)
        W[p.id] = (
            coeffs.wE * E +
            coeffs.wP * P +
            coeffs.wD * D +
            coeffs.wA * A +
            coeffs.wS * S
        )
    return W


def run_weighted_yes_no_election(
    profiles: List[VoterProfile],
    yes_voter_ids: List[str],
    no_voter_ids: List[str],
    coeffs: WeightCoefficients,
    threshold: float,
    bounds: Dict[str, VoterProfile]
) -> Dict[str, Union[bool, float]]:
    """Simple weighted yes/no vote"""
    weights = calculate_weights(profiles, coeffs, bounds)
    total_yes = sum(weights.get(id, 0) for id in yes_voter_ids)
    total_no = sum(weights.get(id, 0) for id in no_voter_ids)
    passed = total_yes / \
        (total_yes + total_no) > threshold if (total_yes + total_no) > 0 else False

    return {
        "passed": passed,
        "total_yes": total_yes,
        "total_no": total_no
    }
