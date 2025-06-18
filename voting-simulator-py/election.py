from typing import Dict, List, Tuple, Optional, Union
from vote_types import VoterProfile, Candidate, Ballot, Results, WeightCoefficients

# Custom single transferable vote style simulator
def run_election(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    # ...existing code...
    # Implement rounds, tally first preferences, eliminate lowest, transfer votes, etc.
    # Return final winner and per-round details.
    return Results(
        winner=None,
        round_details=[]
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
