import sys
import os
import random
import pytest

# ensure the simulator modules are importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from vote_types import Candidate
import voting_systems as vs

# Fixtures for simple election
@pytest.fixture
def three_cands():
    return [Candidate('A','A'), Candidate('B','B'), Candidate('C','C')]

@pytest.fixture
def ballots_three():
    # A is majority first-choice
    return [ ['A','B','C'], ['A','C','B'], ['B','C','A'], ['C','B','A'] ]

def test_plurality(three_cands, ballots_three):
    res = vs.plurality(three_cands, ballots_three)
    assert res.winner is not None
    assert res.winner.id == 'A'

def test_anti_plurality(three_cands, ballots_three):
    # C gets most last-place votes, so avoids negative and wins
    res = vs.anti_plurality(three_cands, ballots_three)
    assert res.winner is not None
    assert res.winner.id in {'A','B'}

def test_borda(three_cands, ballots_three):
    res = vs.borda_count(three_cands, ballots_three)
    assert res.winner is not None
    assert res.winner.id == 'A'

def test_dowdall(three_cands, ballots_three):
    res = vs.dowdall(three_cands, ballots_three)
    assert res.winner is not None
    assert res.winner.id == 'A'

def test_veto(three_cands, ballots_three):
    res = vs.veto(three_cands, ballots_three)
    assert res.winner is not None
    # Under veto, B and C tie at 3 points; B wins by alphabetical order
    assert res.winner.id == 'B'

def test_two_round_runoff(three_cands, ballots_three):
    res = vs.two_round_runoff(three_cands, ballots_three)
    assert res.winner is not None
    assert res.winner.id == 'A'

def test_instant_runoff(three_cands, ballots_three):
    res = vs.instant_runoff(three_cands, ballots_three)
    assert res.winner is not None
    # IRV on this profile yields C after elimination and tie-break
    assert res.winner.id == 'C'

def test_coombs(three_cands, ballots_three):
    res = vs.coombs(three_cands, ballots_three)
    assert res.winner is not None
    assert isinstance(res.winner, Candidate)

def test_bucklin(three_cands, ballots_three):
    res = vs.bucklin(three_cands, ballots_three)
    assert res.winner is not None
    assert res.winner.id == 'A'

def test_baldwin_and_nanson(three_cands, ballots_three):
    res1 = vs.baldwin(three_cands, ballots_three)
    res2 = vs.nanson(three_cands, ballots_three)
    assert res1.winner is not None and res1.winner.id == 'A'
    assert res2.winner is not None and res2.winner.id == 'A'

# Condorcet tests
@pytest.fixture
def ballots_condorcet():
    # A beats B and C head-to-head
    return [ ['A','B','C'], ['B','A','C'], ['A','C','B'], ['C','A','B'], ['A','B','C'] ]

def test_condorcet_winner(three_cands, ballots_condorcet):
    cw = vs.condorcet_winner(three_cands, ballots_condorcet)
    assert cw is not None
    assert cw.id == 'A'

def test_minimax(three_cands, ballots_condorcet):
    res = vs.minimax(three_cands, ballots_condorcet)
    assert res.winner is not None
    assert res.winner.id == 'A'

def test_copeland(three_cands, ballots_condorcet):
    res = vs.copeland(three_cands, ballots_condorcet)
    assert res.winner is not None
    assert res.winner.id == 'A'

def test_black_rule_with_and_without_cw(three_cands, ballots_three, ballots_condorcet):
    # no Condorcet here, fallback to Borda
    res = vs.black_rule(three_cands, ballots_three)
    fallback = vs.borda_count(three_cands, ballots_three)
    assert res.winner is not None and fallback.winner is not None
    assert res.winner.id == fallback.winner.id
    # with Condorcet
    res2 = vs.black_rule(three_cands, ballots_condorcet)
    assert res2.winner is not None
    assert res2.winner.id == 'A'

def test_ranked_pairs_and_schulze(three_cands, ballots_condorcet):
    rp = vs.ranked_pairs(three_cands, ballots_condorcet)
    sch = vs.schulze_method(three_cands, ballots_condorcet)
    assert rp.winner is not None and rp.winner.id == 'A'
    assert sch.winner is not None and sch.winner.id == 'A'

def test_kemeny_and_dodgson(three_cands, ballots_condorcet):
    km = vs.kemeny_young(three_cands, ballots_condorcet)
    dg = vs.dodgson(three_cands, ballots_condorcet)
    assert km.winner is not None and km.winner.id == 'A'
    assert dg.winner is not None and dg.winner.id == 'A'

# Cardinal tests
def test_random_dictatorship(three_cands, ballots_condorcet):
    random.seed(0)
    res = vs.random_dictatorship(three_cands, ballots_condorcet)
    assert res.winner is not None
    assert res.winner.id in {'A','B','C'}

def test_max_utility(three_cands):
    utils = {'A':[3.0,4.0], 'B':[1.0,2.0], 'C':[0.0,1.0]}
    res = vs.max_utility(three_cands, utils)
    assert res.winner is not None
    assert res.winner.id == 'A'

# Majority Judgment and 3-2-1
def test_majority_judgment(three_cands):
    ballots = [ {'A':'Excellent','B':'Good','C':'Poor'},
                {'A':'Good','B':'Excellent','C':'Poor'},
                {'A':'Excellent','B':'Poor','C':'Good'} ]
    res = vs.majority_judgment(three_cands, ballots)
    assert res.winner is not None
    assert res.winner.id == 'A'

def test_three_two_one(three_cands):
    ballots = [ {'A':'Good','B':'Bad','C':'Ok'},
                {'A':'Ok','B':'Good','C':'Bad'},
                {'A':'Bad','B':'Ok','C':'Good'} ]
    res = vs.three_two_one_voting(three_cands, ballots)
    assert res.winner is not None
    assert isinstance(res.winner, Candidate)
