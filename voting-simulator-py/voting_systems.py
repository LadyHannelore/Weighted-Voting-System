from typing import List, Dict, Optional, Tuple, Union, Sequence
from itertools import combinations, permutations
from copy import deepcopy

from vote_types import Candidate, Ballot, Results

# Positional scoring rules

def positional_scoring(candidates: List[Candidate], ballots: List[Ballot], weights: Sequence[Union[int, float]]) -> Results:
    scores = {c.id: 0.0 for c in candidates}
    for ballot in ballots:
        for rank, cid in enumerate(ballot):
            if rank < len(weights):
                scores[cid] += weights[rank]
    # winner is highest score
    winner_id = max(scores, key=lambda cid: scores[cid])
    winner = next(c for c in candidates if c.id == winner_id)
    return Results(winner=winner, round_details=[{"round": 1, "tallies": scores, "eliminated": None}])


def plurality(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    return positional_scoring(candidates, ballots, [1] + [0] * (len(candidates) - 1))


def anti_plurality(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    m = len(candidates)
    return positional_scoring(candidates, ballots, [0] * (m - 1) + [-1])


def borda_count(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    m = len(candidates)
    weights = list(range(m - 1, -1, -1))
    return positional_scoring(candidates, ballots, weights)


def dowdall(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    m = len(candidates)
    weights = [1.0 / (i + 1) for i in range(m)]
    return positional_scoring(candidates, ballots, weights)


def veto(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    m = len(candidates)
    weights = [1.0] * (m - 1) + [0.0]
    return positional_scoring(candidates, ballots, weights)

# Ad-hoc example

def five_three_one(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    return positional_scoring(candidates, ballots, [5, 3, 1])

# Run-off / elimination systems

def two_round_runoff(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    # first round
    first = plurality(candidates, ballots)
    tallies = first.round_details[0]["tallies"]
    # top two
    top_two = sorted(tallies, key=lambda cid: tallies[cid], reverse=True)[:2]
    # head-to-head
    head2 = {cid: 0 for cid in top_two}
    for ballot in ballots:
        for choice in ballot:
            if choice in head2:
                head2[choice] += 1
                break
    winner_id = max(head2, key=lambda cid: head2[cid])
    winner = next(c for c in candidates if c.id == winner_id)
    details = [first.round_details[0], {"round": 2, "tallies": head2, "eliminated": None}]
    return Results(winner=winner, round_details=details)


def instant_runoff(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    # alias for runElection
    from election import run_election_web
    return run_election_web(candidates, ballots)


def coombs(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    remaining = [c.id for c in candidates]
    rounds = []
    while len(remaining) > 1:
        # tally last-place votes
        tallies = {cid: 0 for cid in remaining}
        for ballot in ballots:
            for choice in reversed(ballot):
                if choice in remaining:
                    tallies[choice] += 1
                    break
        total = sum(tallies.values())
        # check majority (lowest rejects means winner)
        for cid, v in tallies.items():
            if v == min(tallies.values()):
                winner_id = cid
        rounds.append({"round": len(rounds) + 1, "tallies": tallies, "eliminated": None})
        # eliminate highest last-place
        to_elim = max(tallies, key=lambda cid: tallies[cid])
        remaining.remove(to_elim)
        rounds[-1]["eliminated"] = to_elim
    winner = next(c for c in candidates if c.id == remaining[0])
    return Results(winner=winner, round_details=rounds)


def bucklin(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    m = len(candidates)
    cum = {c.id: 0 for c in candidates}
    rounds = []
    for k in range(1, m + 1):
        tallies = {cid: 0 for cid in cum}
        for ballot in ballots:
            for choice in ballot[:k]:
                if choice in tallies:
                    tallies[choice] += 1
        rounds.append({"round": k, "tallies": tallies, "eliminated": None})
        total = sum(tallies.values())
        for cid, v in tallies.items():
            if v > total / 2:
                return Results(winner=next(c for c in candidates if c.id == cid), round_details=rounds)
    # no majority, choose highest
    final = rounds[-1]["tallies"]
    winner_id = max(final, key=lambda cid: final[cid])
    return Results(winner=next(c for c in candidates if c.id == winner_id), round_details=rounds)


def borda_elimination(candidates: List[Candidate], ballots: List[Ballot], drop_below_avg: bool=False) -> Results:
    remaining = [c.id for c in candidates]
    rounds = []
    while len(remaining) > 1:
        # compute Borda
        m = len(remaining)
        weights = list(range(m - 1, -1, -1))
        scores = {cid: 0 for cid in remaining}
        for ballot in ballots:
            for rank, cid in enumerate(ballot):
                if cid in scores and rank < m:
                    scores[cid] += weights[rank]
        avg = sum(scores.values()) / m
        if drop_below_avg:
            to_drop = [cid for cid, v in scores.items() if v < avg]
        else:
            # drop one lowest
            to_drop = [min(scores, key=lambda cid: scores[cid])]
        for cid in to_drop:
            remaining.remove(cid)
        rounds.append({"round": len(rounds) + 1, "tallies": scores, "eliminated": to_drop})
    winner = next(c for c in candidates if c.id == remaining[0])
    return Results(winner=winner, round_details=rounds)


def baldwin(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    return borda_elimination(candidates, ballots, drop_below_avg=False)


def nanson(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    return borda_elimination(candidates, ballots, drop_below_avg=True)

# Condorcet-oriented rules

def pairwise_matrix(candidates: List[Candidate], ballots: List[Ballot]) -> Dict[Tuple[str, str], int]:
    ids = [c.id for c in candidates]
    M = {(x, y): 0 for x, y in permutations(ids, 2)}
    for ballot in ballots:
        for x, y in combinations(ids, 2):
            if ballot.index(x) < ballot.index(y):
                M[(x, y)] += 1
            else:
                M[(y, x)] += 1
    return M


def condorcet_winner(candidates: List[Candidate], ballots: List[Ballot]) -> Optional[Candidate]:
    M = pairwise_matrix(candidates, ballots)
    ids = [c.id for c in candidates]
    for x in ids:
        if all(M.get((x, y), 0) > M.get((y, x), 0) for y in ids if y != x):
            return next(c for c in candidates if c.id == x)
    return None


def minimax(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    M = pairwise_matrix(candidates, ballots)
    worst = {}
    for x in [c.id for c in candidates]:
        defeats = [M[(y, x)] - M[(x, y)] for y in [c.id for c in candidates] if y != x]
        worst[x] = max(defeats) if defeats else 0
    winner_id = min(worst, key=lambda x: worst[x])
    return Results(winner=next(c for c in candidates if c.id == winner_id), round_details=[])


def copeland(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    M = pairwise_matrix(candidates, ballots)
    score = {c.id: 0 for c in candidates}
    for x, y in combinations([c.id for c in candidates], 2):
        if M[(x, y)] > M[(y, x)]:
            score[x] += 1
            score[y] -= 1
        elif M[(x, y)] < M[(y, x)]:
            score[x] -= 1
            score[y] += 1
    winner_id = max(score, key=lambda cid: score[cid])
    return Results(winner=next(c for c in candidates if c.id == winner_id), round_details=[])


def black_rule(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    cw = condorcet_winner(candidates, ballots)
    if cw:
        return Results(winner=cw, round_details=[])
    return borda_count(candidates, ballots)

# Other Condorcet methods (placeholders)

def smith_irv(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    # Compute Smith set: smallest unbeaten set
    M = pairwise_matrix(candidates, ballots)
    ids = [c.id for c in candidates]
    # initialize set to all candidates
    S = set(ids)
    changed = True
    while changed:
        changed = False
        for x in list(S):
            for y in ids:
                if y in S and x in S and y != x:
                    if M[(y, x)] > M[(x, y)]:
                        # y beats x, so x not in Smith set
                        S.remove(x)
                        changed = True
                        break
            if changed:
                break
    # restrict candidates and ballots
    sub_candidates = [c for c in candidates if c.id in S]
    return instant_runoff(sub_candidates, ballots)


def ranked_pairs(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    # Tideman Ranked Pairs
    M = pairwise_matrix(candidates, ballots)
    ids = [c.id for c in candidates]
    # list of pairs with strength
    pairs = []
    for x, y in combinations(ids, 2):
        wxy = M[(x, y)] - M[(y, x)]
        if wxy > 0:
            pairs.append((x, y, wxy))
        elif wxy < 0:
            pairs.append((y, x, -wxy))
    # sort by descending strength
    pairs.sort(key=lambda t: t[2], reverse=True)
    locked = {c: set() for c in ids}
    def creates_cycle(start, end, graph):
        # DFS to detect if end reaches start
        stack = [end]
        visited = set()
        while stack:
            node = stack.pop()
            if node == start:
                return True
            if node not in visited:
                visited.add(node)
                for nbr in graph.get(node, []):
                    stack.append(nbr)
        return False
    # lock pairs
    for winner, loser, _ in pairs:
        # try to add edge winner->loser
        if not creates_cycle(winner, loser, locked):
            locked[winner].add(loser)
    # winner has no incoming edges
    incoming = {c: 0 for c in ids}
    for src, targets in locked.items():
        for tgt in targets:
            incoming[tgt] += 1
    winner_id = min(incoming, key=lambda c: incoming[c])
    winner = next(c for c in candidates if c.id == winner_id)
    return Results(winner=winner, round_details=[])


def schulze_method(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    # Schulze beatpath method
    M = pairwise_matrix(candidates, ballots)
    ids = [c.id for c in candidates]
    # initialize path strengths
    p = { (i, j): 0 for i in ids for j in ids }
    for i in ids:
        for j in ids:
            if i != j:
                if M[(i, j)] > M[(j, i)]:
                    p[(i, j)] = M[(i, j)]
                else:
                    p[(i, j)] = 0
    # Floyd-Warshall style
    for k in ids:
        for i in ids:
            for j in ids:
                if i != j and i != k and j != k:
                    p[(i, j)] = max(p[(i, j)], min(p[(i, k)], p[(k, j)]))
    # find winner whose path strengths beat all others
    for i in ids:
        if all(p[(i, j)] >= p[(j, i)] for j in ids if j != i):
            winner = next(c for c in candidates if c.id == i)
            return Results(winner=winner, round_details=[])
    return Results(winner=None, round_details=[])


def kemeny_young(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    # Brute-force Kemeny-Young: find ranking maximizing pairwise agreement
    from itertools import permutations
    ids = [c.id for c in candidates]
    M = pairwise_matrix(candidates, ballots)
    best_score = None
    best_ranking = None
    for perm in permutations(ids):
        score = 0
        for i in range(len(perm)):
            for j in range(i+1, len(perm)):
                score += M.get((perm[i], perm[j]), 0)
        if best_score is None or score > best_score:
            best_score = score
            best_ranking = perm
    # Winner is top of the optimal ranking
    winner_id = best_ranking[0] if best_ranking else None
    winner = next((c for c in candidates if c.id == winner_id), None)
    return Results(winner=winner, round_details=[])


def dodgson(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    # Approximate Dodgson distance by total pairwise deficit (sum of positive deficits)
    M = pairwise_matrix(candidates, ballots)
    ids = [c.id for c in candidates]
    deficits = {}
    for x in ids:
        total_deficit = 0
        for y in ids:
            if y != x:
                d = M[(y, x)] - M[(x, y)]
                if d > 0:
                    total_deficit += d
        deficits[x] = total_deficit
    winner_id = min(deficits, key=lambda cid: deficits[cid])
    winner = next((c for c in candidates if c.id == winner_id), None)
    return Results(winner=winner, round_details=[])


def young(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    # Approximate Young score by total pairwise deficit (voter deletions)
    # Similar to Dodgson approximation
    return dodgson(candidates, ballots)

# Cardinal systems

def approval_voting(candidates: List[Candidate], ballots: List[Dict[str, int]]) -> Results:
    scores = {c.id: 0 for c in candidates}
    for ballot in ballots:
        for cid, score in ballot.items():
            if score == 1 and cid in scores:
                scores[cid] += 1
    winner_id = max(scores, key=lambda cid: scores[cid])
    return Results(winner=next(c for c in candidates if c.id == winner_id), round_details=[{"round": 1, "tallies": scores, "eliminated": None}])


def score_voting(candidates: List[Candidate], ballots: List[Dict[str, float]]) -> Results:
    scores = {c.id: 0.0 for c in candidates}
    for ballot in ballots:
        for cid, val in ballot.items():
            if cid in scores:
                scores[cid] += val
    winner_id = max(scores, key=lambda cid: scores[cid])
    return Results(winner=next(c for c in candidates if c.id == winner_id), round_details=[{"round": 1, "tallies": scores, "eliminated": None}])


def majority_judgment(candidates: List[Candidate], ballots: List[Dict[str, str]]) -> Results:
    # Median grade wins; tie-break by lexicographic grade distribution
    # Collect all unique grades
    unique_grades = set()
    for b in ballots:
        unique_grades.update(b.values())
    # Sort grades descending (assumes string order conveys quality)
    sorted_grades = sorted(unique_grades, reverse=True)
    # Map grade to rank (0 = best)
    grade_rank = {g: i for i, g in enumerate(sorted_grades)}
    # Compute median rank and distribution for each candidate
    cand_stats = {}
    for c in candidates:
        # gather ranks
        ranks = [grade_rank.get(b.get(c.id, ''), len(sorted_grades)) for b in ballots]
        ranks_sorted = sorted(ranks)
        if not ranks_sorted:
            continue
        mid = len(ranks_sorted) // 2
        median_rank = ranks_sorted[mid]
        cand_stats[c.id] = (median_rank, ranks_sorted)
    # select winner by minimal median_rank, tie-break by lex minimal ranks_sorted
    winner_id = min(
        cand_stats.keys(),
        key=lambda cid: (cand_stats[cid][0], cand_stats[cid][1])
    )
    winner = next((c for c in candidates if c.id == winner_id), None)
    return Results(winner=winner, round_details=[])


def star_voting(candidates: List[Candidate], ballots: List[Dict[str, float]]) -> Results:
    # score stage
    total = score_voting(candidates, ballots)
    top2 = sorted(total.round_details[0]["tallies"], key=lambda cid: total.round_details[0]["tallies"][cid], reverse=True)[:2]
    # runoff
    runoff = {cid: 0 for cid in top2}
    for ballot in ballots:
        if ballot.get(top2[0], 0) > ballot.get(top2[1], 0):
            runoff[top2[0]] += 1
        else:
            runoff[top2[1]] += 1
    winner_id = max(runoff, key=lambda cid: runoff[cid])
    winner = next(c for c in candidates if c.id == winner_id)
    details = [total.round_details[0], {"round": 2, "tallies": runoff, "eliminated": None}]
    return Results(winner=winner, round_details=details)

# Hybrids & special-purpose

def three_two_one_voting(candidates: List[Candidate], ballots: List[Dict[str, str]]) -> Results:
    # Grades: Good, OK, Bad
    ids = [c.id for c in candidates]
    # step 1: eliminate anyone with >50% Bad
    bad_counts = {cid: 0 for cid in ids}
    total = len(ballots)
    for b in ballots:
        for cid, grade in b.items():
            if cid in bad_counts and grade.lower() == 'bad':
                bad_counts[cid] += 1
    S = [cid for cid in ids if bad_counts[cid] <= total/2]
    # step 2: count Good for survivors
    good_counts = {cid: 0 for cid in S}
    for b in ballots:
        for cid, grade in b.items():
            if cid in good_counts and grade.lower() == 'good':
                good_counts[cid] += 1
    # keep top three by Good
    top3 = sorted(good_counts, key=lambda cid: good_counts[cid], reverse=True)[:3]
    if not top3:
        return Results(winner=None, round_details=[])
    # step 3: Condorcet among top3
    # build pairwise among top3
    pair_wins = {cid: 0 for cid in top3}
    for x, y in combinations(top3, 2):
        x_pref = 0
        y_pref = 0
        for b in ballots:
            gx = b.get(x, '').lower()
            gy = b.get(y, '').lower()
            # Good > OK > Bad
            order = {'good': 3, 'ok': 2, 'bad': 1}
            if order.get(gx, 0) > order.get(gy, 0): x_pref += 1
            elif order.get(gy, 0) > order.get(gx, 0): y_pref += 1
        if x_pref > y_pref:
            pair_wins[x] += 1
        elif y_pref > x_pref:
            pair_wins[y] += 1
    # winner is who wins 2 pairwise or highest pair_wins
    winner_id = max(pair_wins, key=lambda cid: pair_wins[cid])
    winner = next(c for c in candidates if c.id == winner_id)
    return Results(winner=winner, round_details=[])

# Theoretical & stochastic

def random_dictatorship(candidates: List[Candidate], ballots: List[Ballot]) -> Results:
    import random
    if not ballots:
        return Results(winner=None, round_details=[])
    choice = random.choice(ballots)[0] if ballots[0] else None
    winner = next((c for c in candidates if c.id == choice), None)
    return Results(winner=winner, round_details=[])


def max_utility(candidates: List[Candidate], utilities: Dict[str, List[float]]) -> Results:
    # utilities: candidate_id -> list of utilities from each voter
    avg = {cid: sum(vals) / len(vals) for cid, vals in utilities.items() if vals}
    winner_id = max(avg, key=lambda cid: avg[cid])
    return Results(winner=next(c for c in candidates if c.id == winner_id), round_details=[])
