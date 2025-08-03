# Field Guide to Voting Rules

A compact overview of common voting systems, including ballot format, winner computation, and distinctive properties.

---

## 1. Positional-Scoring Rules (Fixed weight vectors on ranks)

**Ballot:** Strict ranking of as many candidates as the voter wishes.  
Let *m* be the number of candidates; the rule is defined by a vector \(w = (w_1, w_2, \dots, w_m)\) with \(w_1 \ge w_2 \ge \dots \ge w_m\).

| System                                    | Weight vector \(w\)                              | Catch-phrase                     |
|-------------------------------------------|---------------------------------------------------|----------------------------------|
| **Plurality / First-Past-The-Post**        | \((1, 0, 0, \dots, 0)\)                         | One mark, winner-take-all.       |
| **Anti-plurality (Negative Voting)**      | \((0, 0, \dots, 0, -1)\)                        | Vote against, not for.           |
| **Borda Count**                           | \((m-1, m-2, \dots, 1, 0)\)                    | Olympic podium average.          |
| **Dowdall (Harmonic Borda)**              | \((1, \tfrac12, \tfrac13, \dots, \tfrac1m)\) | Rank reciprocals.                |
| **5-3-1 rule** (three-slot ballots)       | \((5, 3, 1)\)                                     | Informal ad-hoc example.         |
| **Veto**                                  | \((1,1,\dots,1,0)\)                             | Approve all but one.             |

---

## 2. Run-off / Elimination Systems

**Ballot:** Ranked list (full or truncated).  

1. **Two-Round Run-off (Top-Two, TRS)**
   - 1st round: Plurality.  
   - 2nd round: Top two advance; majority winner wins.  
   - *Catch-phrase:* Two Saturdays, easy to explain.

2. **Instant-Runoff Voting (IRV / Hare)**
   - Repeated plurality-with-elimination until a candidate has majority.  
   - *Catch-phrase:* Count once, eliminate many.

3. **Coombs Method**
   - Like IRV but eliminate the candidate with the most last-place votes.  
   - *Catch-phrase:* IRV upside-down.

4. **Bucklin (and Grand Bucklin)**
   - Accumulate 1st, then 2nd, 3rd preferences… stop at majority.  
   - Grand Bucklin uses fractional thresholds for smoother counts.  
   - *Catch-phrase:* Keep lowering the bar.

5. **Baldwin Elimination**
   - Repeated Borda: drop lowest Borda scorer each round.  
   - *Catch-phrase:* Borda meets Survivor.

6. **Nanson Elimination**
   - Drop all candidates below the average Borda score each round.  
   - *Catch-phrase:* Borda with mass lay-offs.

---

## 3. Condorcet-Oriented Rules

**Ballot:** Ranking. Build the \(m\times m\) pairwise matrix \(M\) with \(M_{xy}\) = voters preferring *x* to *y*.

| System                                    | Definition                                                                          | Catch-phrase                     |
|-------------------------------------------|-------------------------------------------------------------------------------------|----------------------------------|
| **Condorcet Winner Test**                 | If some candidate beats every rival head-to-head, they win.                          | Majority beats all.              |
| **Minimax (Simpson-Kramer)**              | Elect the candidate whose largest pairwise defeat is smallest.                      | Minimise worst loss.             |
| **Copeland**                              | Score = (# pairwise wins) – (# losses).                                             | Win-loss differential.           |
| **Black’s Rule**                          | Condorcet winner if exists; otherwise Borda.                                        | Best of both worlds.             |
| **Condorcet-Hare (Smith-IRV)**            | IRV restricted to the Smith set (smallest unbeaten set).                            | Majority core, IRV finish.       |
| **Ranked Pairs (Tideman)**                | Lock in victories by descending strength, skip cycles; top of resulting DAG wins.   | Lock strong edges, ignore cycles.|
| **Schulze Path Method (Beatpath)**        | Elect candidate whose weakest path to every other is strongest.                     | Strongest weakest link.          |
| **Kemeny–Young**                          | Find ranking reversing fewest pairwise preferences; top wins.                        | Global best ranking.             |
| **Dodgson**                               | Candidate needing fewest adjacent swaps to become Condorcet winner.                 | Edit ballots minimally.          |
| **Young**                                 | Candidate requiring fewest voter deletions to become Condorcet winner.              | Fewest voters to discard.        |

---

## 4. Cardinal (Explicit numeric score) Systems

**Ballot:** Assign numeric score or grade to each candidate.

| System                      | Score type               | Winner criterion           | Catch-phrase                 |
|-----------------------------|--------------------------|----------------------------|------------------------------|
| **Approval Voting**         | Binary \{0,1\}          | Most approvals             | Tick the ones you like.      |
| **Range / Score Voting**    | Real/bounded             | Highest mean               | Average star rating.         |
| **Majority Judgment**       | Ordinal grades           | Highest median grade       | Middlemost grade.            |
| **STAR Voting**             | Score + automatic runoff | Top two by score + pairwise| Score first, majority last.  |

---

## 5. Hybrid & Special-Purpose Rules

- **3-2-1 Voting**: 3 grades (Good/OK/Bad). Eliminate >50% Bad; keep most Good; Condorcet among top three.  
  *Catch-phrase:* Grade, approve, Condorcet.
- **Designer Hybrids**: e.g. 0-3-2 Approval hybrids, majority-width Bucklin variants mix grading, approval, Bucklin—aim for expressive ballots + simple counts.

---

## 6. Theoretical & Stochastic Constructs

- **Random Dictatorship**: Pick one ballot at random; its top wins. *Catch-phrase:* One voter decides, fairly chosen.
- **Max-Utility (Utilitarian optimum)**: Hypothetical rule electing candidate with greatest true average utility. *Catch-phrase:* If we knew everyone’s happiness.

---

## 7. Quick Mnemonic Summary

- **Plurality:** 1 point to top.
- **Borda:** Olympic podium.
- **IRV:** Eliminate losers, keep ballots.
- **Condorcet:** Majority head-to-head.
- **Approval:** Binary like/unlike.
- **Range:** Star ratings.
- **STAR:** Range + runoff.
- **Random dictator:** Spin the bottle.
