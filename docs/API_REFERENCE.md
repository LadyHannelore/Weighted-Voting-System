# API Reference - UK Weighted Voting System

## Core Modules

### `vote_types.py` - Data Structures

#### `VoterProfile`
```python
@dataclass
class VoterProfile:
    id: str
    E: float  # expertise raw score (0-10)
    P: float  # participation raw score (0-100)
    D: float  # decision-quality raw score (0-10)
    A: float  # alignment raw score (0-10)
    S: float  # stake raw score (0-100)
```

**Usage:**
```python
profile = VoterProfile(
    id='tech_expert',
    E=9.0,    # High expertise
    P=85.0,   # High participation
    D=8.0,    # Good decision quality
    A=7.0,    # Good alignment
    S=90.0    # High stake
)
```

#### `WeightCoefficients`
```python
@dataclass
class WeightCoefficients:
    wE: float  # expertise weight
    wP: float  # participation weight
    wD: float  # decision quality weight
    wA: float  # alignment weight
    wS: float  # stake weight
```

**Constraints:** All weights must sum to 1.0

**Usage:**
```python
# Expertise-focused weighting
coeffs = WeightCoefficients(
    wE=0.4,  # 40% expertise
    wP=0.3,  # 30% participation
    wD=0.1,  # 10% decision quality
    wA=0.1,  # 10% alignment
    wS=0.1   # 10% stake
)
```

#### `Candidate`
```python
@dataclass
class Candidate:
    id: str
    name: str
```

#### `Results`
```python
@dataclass
class Results:
    winner: Optional[Candidate]
    round_details: List[RoundDetail]
```

### `election.py` - Voting Algorithms

#### `run_weighted_yes_no_election()`
```python
def run_weighted_yes_no_election(
    profiles: List[VoterProfile],
    yes_voter_ids: List[str],
    no_voter_ids: List[str],
    coeffs: WeightCoefficients,
    threshold: float,
    bounds: Dict[str, VoterProfile]
) -> Dict[str, Union[bool, float]]
```

**Parameters:**
- `profiles`: List of voter profiles
- `yes_voter_ids`: IDs of voters voting YES
- `no_voter_ids`: IDs of voters voting NO
- `coeffs`: Weight coefficients
- `threshold`: Passing threshold (0.0-1.0)
- `bounds`: Min/max bounds for normalization

**Returns:**
```python
{
    "passed": bool,      # Whether motion passed
    "total_yes": float,  # Total weighted YES votes
    "total_no": float    # Total weighted NO votes
}
```

**Example:**
```python
result = run_weighted_yes_no_election(
    profiles=voter_profiles,
    yes_voter_ids=['alice', 'bob'],
    no_voter_ids=['charlie'],
    coeffs=equal_weights,
    threshold=0.5,
    bounds=normalization_bounds
)

if result['passed']:
    print(f"Motion passed: {result['total_yes']:.2f} vs {result['total_no']:.2f}")
```

#### `run_election()`
```python
def run_election(
    candidates: List[Candidate],
    ballots: List[Ballot],
    round_duration: int = 30
) -> Results
```

**Parameters:**
- `candidates`: List of candidate objects
- `ballots`: List of preference-ordered ballot lists
- `round_duration`: Seconds per elimination round

**Returns:** `Results` object with winner and round details

**Example:**
```python
candidates = [
    Candidate(id='labour', name='Labour Party'),
    Candidate(id='conservative', name='Conservative Party')
]

ballots = [
    ['labour', 'conservative'],      # Labour first preference
    ['conservative', 'labour'],      # Conservative first preference
    ['labour', 'conservative']       # Labour first preference
]

results = run_election(candidates, ballots, round_duration=5)
print(f"Winner: {results.winner.name}")
```

#### `calculate_weights()`
```python
def calculate_weights(
    profiles: List[VoterProfile],
    coeffs: WeightCoefficients,
    bounds: Dict[str, VoterProfile]
) -> Dict[str, float]
```

**Purpose:** Calculate weighted voting power for each voter profile

**Formula:** `W = wE×norm(E) + wP×norm(P) + wD×norm(D) + wA×norm(A) + wS×norm(S)`

**Returns:** Dictionary mapping voter IDs to calculated weights

#### `normalize()`
```python
def normalize(x: float, min_val: float, max_val: float) -> float
```

**Purpose:** Apply min-max normalization to scale values to [0,1]

**Formula:** `(x - min) / (max - min)`

#### `verify_voting_system()`
```python
def verify_voting_system() -> bool
```

**Purpose:** Print verification that voting algorithms follow proper democratic principles

### `visualization.py` - Chart Generation

#### `create_weighted_vote_chart()`
```python
def create_weighted_vote_chart(
    results_dict: Dict[str, Dict], 
    title: str = "Weighted Voting Results"
) -> go.Figure
```

**Purpose:** Create bar chart comparing different weighting systems

**Parameters:**
- `results_dict`: Dictionary of weighting system names to results
- `title`: Chart title

**Returns:** Plotly Figure object

#### `create_ranked_choice_visualization()`
```python
def create_ranked_choice_visualization(
    results: Results, 
    candidates: List[Candidate]
) -> go.Figure
```

**Purpose:** Create visualization showing vote progression through elimination rounds

#### `create_voter_profile_heatmap()`
```python
def create_voter_profile_heatmap(
    profiles: List[VoterProfile]
) -> go.Figure
```

**Purpose:** Create heatmap showing voter attribute distributions

#### `create_first_preferences_pie_chart()`
```python
def create_first_preferences_pie_chart(
    ballots: List[List[str]], 
    candidates: List[Candidate]
) -> go.Figure
```

**Purpose:** Create pie chart of initial vote distribution

#### `save_all_charts()`
```python
def save_all_charts(
    charts: Dict[str, go.Figure], 
    output_dir: str = "charts"
) -> None
```

**Purpose:** Save all charts as HTML files in specified directory

## Usage Patterns

### Basic Weighted Voting
```python
from vote_types import VoterProfile, WeightCoefficients
from election import run_weighted_yes_no_election

# 1. Define voter profiles
profiles = [
    VoterProfile('expert', E=9, P=80, D=8, A=7, S=85),
    VoterProfile('novice', E=3, P=20, D=5, A=6, S=70)
]

# 2. Set up weighting
coeffs = WeightCoefficients(0.3, 0.2, 0.2, 0.2, 0.1)

# 3. Define bounds
bounds = {
    'min': VoterProfile('', 0, 0, 0, 0, 0),
    'max': VoterProfile('', 10, 100, 10, 10, 100)
}

# 4. Run vote
result = run_weighted_yes_no_election(
    profiles, ['expert'], ['novice'], coeffs, 0.5, bounds
)
```

### Ranked Choice Election
```python
from vote_types import Candidate
from election import run_election

# 1. Define candidates
candidates = [
    Candidate('a', 'Candidate A'),
    Candidate('b', 'Candidate B'),
    Candidate('c', 'Candidate C')
]

# 2. Collect ballots
ballots = [
    ['a', 'b', 'c'],  # A > B > C
    ['b', 'a', 'c'],  # B > A > C
    ['a', 'c', 'b']   # A > C > B
]

# 3. Run election
results = run_election(candidates, ballots)
```

### Complete Simulation with Charts
```python
from visualization import create_weighted_vote_chart, save_all_charts

# Run multiple scenarios
scenarios = {
    'Equal': run_weighted_yes_no_election(...),
    'Expert-focused': run_weighted_yes_no_election(...),
    'Stake-focused': run_weighted_yes_no_election(...)
}

# Generate charts
chart = create_weighted_vote_chart(scenarios)
save_all_charts({'comparison': chart})
```

## Error Handling

### Common Errors

**Invalid Weight Coefficients:**
```python
# ERROR: Weights don't sum to 1.0
coeffs = WeightCoefficients(0.3, 0.3, 0.3, 0.3, 0.3)  # Sum = 1.5

# CORRECT:
coeffs = WeightCoefficients(0.2, 0.2, 0.2, 0.2, 0.2)  # Sum = 1.0
```

**Empty Ballot Lists:**
```python
# ERROR: Empty ballots
ballots = [[], ['a', 'b'], ['b', 'a']]

# CORRECT: All ballots have at least one preference
ballots = [['a'], ['a', 'b'], ['b', 'a']]
```

**Mismatched Candidate IDs:**
```python
# ERROR: Ballot references non-existent candidate
candidates = [Candidate('a', 'A'), Candidate('b', 'B')]
ballots = [['a', 'b', 'c']]  # 'c' doesn't exist

# CORRECT: All ballot entries match candidate IDs
ballots = [['a', 'b']]
```

### Error Prevention

1. **Validate inputs** before calling functions
2. **Check coefficient sums** equal 1.0
3. **Verify candidate IDs** match between candidates and ballots
4. **Ensure positive bounds** for normalization
5. **Handle empty results** gracefully

## Performance Considerations

### Large-Scale Simulations
- **Ballot Processing**: O(n×m) where n=ballots, m=average preferences
- **Weight Calculation**: O(p) where p=number of profiles
- **Visualization**: Memory usage scales with data points

### Optimization Tips
1. **Batch Processing**: Process large ballot sets in chunks
2. **Caching**: Store calculated weights for reuse
3. **Lazy Loading**: Generate charts only when needed
4. **Sampling**: Use representative subsets for very large datasets

## Testing

### Unit Test Examples
```python
def test_weight_calculation():
    """Test that weights are calculated correctly."""
    profile = VoterProfile('test', E=5, P=50, D=5, A=5, S=50)
    coeffs = WeightCoefficients(0.2, 0.2, 0.2, 0.2, 0.2)
    bounds = {'min': VoterProfile('', 0, 0, 0, 0, 0),
              'max': VoterProfile('', 10, 100, 10, 10, 100)}
    
    weights = calculate_weights([profile], coeffs, bounds)
    expected = 0.2 * 0.5 + 0.2 * 0.5 + 0.2 * 0.5 + 0.2 * 0.5 + 0.2 * 0.5
    assert abs(weights['test'] - expected) < 0.001
```

### Integration Test Examples
```python
def test_full_election_workflow():
    """Test complete election from ballots to results."""
    candidates = [Candidate('a', 'A'), Candidate('b', 'B')]
    ballots = [['a', 'b'], ['a', 'b'], ['b', 'a']]
    
    results = run_election(candidates, ballots, round_duration=0)
    
    assert results.winner.id == 'a'
    assert len(results.round_details) == 1
```
