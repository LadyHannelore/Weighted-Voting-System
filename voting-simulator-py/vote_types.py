from typing import Dict, List, Optional, TypedDict, Any
from dataclasses import dataclass


@dataclass
class Candidate:
    id: str
    name: str


# Ballot is a list of candidate IDs in order of preference
Ballot = List[str]


class RoundDetail(TypedDict):
    round: int
    # tallies may be numeric counts or scores
    tallies: Dict[str, Any]
    eliminated: Optional[str]


@dataclass
class Results:
    winner: Optional[Candidate]
    round_details: List[RoundDetail]


@dataclass
class VoterProfile:
    id: str
    E: float  # expertise raw score
    P: float  # participation raw score
    D: float  # decision-quality raw score
    A: float  # alignment raw score
    S: float  # stake raw score
    name: str = ""  # display name for web interface
    count: int = 1  # number of voters in this profile


@dataclass
class WeightCoefficients:
    wE: float
    wP: float
    wD: float
    wA: float
    wS: float
