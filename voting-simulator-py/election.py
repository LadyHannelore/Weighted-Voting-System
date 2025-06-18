from typing import Dict, List, Tuple, Optional, Union
from vote_types import VoterProfile, Candidate, Ballot, Results, WeightCoefficients

# Custom single transferable vote style simulator
def run_election(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    """
    Run a ranked choice (single transferable vote) election.
    
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
            "tallies": tallies
        }
        
        # Find candidate with lowest votes
        min_votes = float('inf')
        to_eliminate = None
        
        for cid, votes in tallies.items():
            if votes < min_votes:
                min_votes = votes
                to_eliminate = cid
        
        # Check for a majority winner
        total_votes = sum(tallies.values())
        for cid, votes in tallies.items():
            if votes > total_votes / 2:
                # We have a winner
                rounds.append(round_detail)
                return Results(
                    winner=candidate_map.get(cid),
                    round_details=rounds
                )
        
        # No winner yet, eliminate lowest candidate
        if to_eliminate:
            round_detail["eliminated"] = to_eliminate
            remaining_candidates.remove(to_eliminate)
        
        rounds.append(round_detail)
        round_num += 1
    
    # If we exit the loop, either we have a single candidate left, or we're out of candidates
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
    passed = total_yes / (total_yes + total_no) > threshold if (total_yes + total_no) > 0 else False
    
    return {
        "passed": passed,
        "total_yes": total_yes,
        "total_no": total_no
    }
