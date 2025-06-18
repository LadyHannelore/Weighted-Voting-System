# Tutorials - UK Weighted Voting System

## Tutorial 1: Your First Weighted Vote

### Goal
Create a simple weighted yes/no vote on a policy decision.

### Step 1: Set Up Voter Profiles
```python
from vote_types import VoterProfile, WeightCoefficients

# Create three different voter types
profiles = [
    VoterProfile(
        id='policy_expert',
        E=9,   # High expertise in policy area
        P=85,  # High historical participation
        D=8,   # Good decision-making track record
        A=7,   # Good alignment with public interest
        S=90   # High stake in outcome
    ),
    VoterProfile(
        id='average_citizen',
        E=5,   # Moderate expertise
        P=60,  # Moderate participation
        D=6,   # Average decision quality
        A=7,   # Good public alignment
        S=75   # Moderate stake
    ),
    VoterProfile(
        id='occasional_voter',
        E=3,   # Lower expertise
        P=30,  # Lower participation
        D=5,   # Average decisions
        A=6,   # Moderate alignment
        S=60   # Lower stake
    )
]
```

### Step 2: Define Weight Coefficients
```python
# Equal weighting across all attributes
equal_weights = WeightCoefficients(
    wE=0.2,  # 20% expertise
    wP=0.2,  # 20% participation
    wD=0.2,  # 20% decision quality
    wA=0.2,  # 20% alignment
    wS=0.2   # 20% stake
)

# Expertise-focused weighting
expert_weights = WeightCoefficients(
    wE=0.4,  # 40% expertise
    wP=0.3,  # 30% participation
    wD=0.1,  # 10% decision quality
    wA=0.1,  # 10% alignment
    wS=0.1   # 10% stake
)
```

### Step 3: Set Normalization Bounds
```python
bounds = {
    "min": VoterProfile(id='', E=0, P=0, D=0, A=0, S=0),
    "max": VoterProfile(id='', E=10, P=100, D=10, A=10, S=100)
}
```

### Step 4: Run the Vote
```python
from election import run_weighted_yes_no_election

# Define who votes yes vs no
yes_voters = ['policy_expert', 'average_citizen']
no_voters = ['occasional_voter']

# Run with equal weights
result_equal = run_weighted_yes_no_election(
    profiles=profiles,
    yes_voter_ids=yes_voters,
    no_voter_ids=no_voters,
    coeffs=equal_weights,
    threshold=0.5,
    bounds=bounds
)

# Run with expert-focused weights
result_expert = run_weighted_yes_no_election(
    profiles=profiles,
    yes_voter_ids=yes_voters,
    no_voter_ids=no_voters,
    coeffs=expert_weights,
    threshold=0.5,
    bounds=bounds
)

print(f"Equal weights: {'PASSED' if result_equal['passed'] else 'FAILED'}")
print(f"Expert weights: {'PASSED' if result_expert['passed'] else 'FAILED'}")
```

---

## Tutorial 2: Ranked Choice Election

### Goal
Simulate a multi-candidate election using ranked choice voting.

### Step 1: Create Candidates
```python
from vote_types import Candidate

candidates = [
    Candidate(id='progressive', name='Progressive Party'),
    Candidate(id='centrist', name='Centrist Party'),
    Candidate(id='conservative', name='Conservative Party'),
    Candidate(id='green', name='Green Party')
]
```

### Step 2: Create Voter Ballots
```python
# Each ballot is a list of candidate IDs in preference order
ballots = [
    # Progressive voters (30%)
    ['progressive', 'green', 'centrist', 'conservative'],
    ['progressive', 'green', 'centrist', 'conservative'],
    ['progressive', 'centrist', 'green', 'conservative'],
    
    # Conservative voters (25%)
    ['conservative', 'centrist', 'progressive', 'green'],
    ['conservative', 'centrist', 'progressive', 'green'],
    ['conservative', 'progressive', 'centrist', 'green'],
    
    # Centrist voters (25%)
    ['centrist', 'progressive', 'conservative', 'green'],
    ['centrist', 'conservative', 'progressive', 'green'],
    
    # Green voters (20%)
    ['green', 'progressive', 'centrist', 'conservative'],
    ['green', 'progressive', 'centrist', 'conservative']
]
```

### Step 3: Run the Election
```python
from election import run_election

# Run with 5-second rounds for quick demo
results = run_election(
    candidates=candidates,
    ballots=ballots,
    round_duration=5
)

print(f"Winner: {results.winner.name}")
print(f"Total rounds: {len(results.round_details)}")
```

### Step 4: Analyze Results
```python
for round_detail in results.round_details:
    print(f"\nRound {round_detail['round']}:")
    
    # Sort by vote count
    sorted_votes = sorted(
        round_detail['tallies'].items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    total_votes = sum(round_detail['tallies'].values())
    
    for candidate_id, votes in sorted_votes:
        candidate_name = next(c.name for c in candidates if c.id == candidate_id)
        percentage = (votes / total_votes) * 100
        print(f"  {candidate_name}: {votes} votes ({percentage:.1f}%)")
    
    if 'eliminated' in round_detail:
        eliminated_name = next(c.name for c in candidates if c.id == round_detail['eliminated'])
        print(f"  ELIMINATED: {eliminated_name}")
```

---

## Tutorial 3: Visualization and Analysis

### Goal
Create charts and visualizations for your voting results.

### Step 1: Run Multiple Scenarios
```python
# Run the same yes/no vote with different weighting systems
scenarios = {}

# Equal weights
scenarios['Equal Weights'] = run_weighted_yes_no_election(
    profiles, yes_voters, no_voters, equal_weights, 0.5, bounds
)

# Expertise-focused
scenarios['Expertise Focus'] = run_weighted_yes_no_election(
    profiles, yes_voters, no_voters, expert_weights, 0.5, bounds
)

# Participation-focused
participation_weights = WeightCoefficients(0.1, 0.4, 0.2, 0.2, 0.1)
scenarios['Participation Focus'] = run_weighted_yes_no_election(
    profiles, yes_voters, no_voters, participation_weights, 0.5, bounds
)
```

### Step 2: Create Visualizations
```python
from visualization import (
    create_weighted_vote_chart,
    create_voter_profile_heatmap,
    create_first_preferences_pie_chart,
    save_all_charts
)

charts = {}

# Weighted vote comparison
charts['Weighted Comparison'] = create_weighted_vote_chart(
    scenarios, 
    title="Policy Vote: Different Weighting Systems"
)

# Voter profile heatmap
charts['Voter Profiles'] = create_voter_profile_heatmap(profiles)

# First preferences for ranked choice
charts['First Preferences'] = create_first_preferences_pie_chart(ballots, candidates)
```

### Step 3: Save and Display Charts
```python
from visualization import save_all_charts, display_charts_in_browser

# Save all charts as HTML files
save_all_charts(charts, output_dir="my_analysis")

# Display in browser (optional)
try:
    display_charts_in_browser(charts)
    print("Charts opened in your browser!")
except Exception as e:
    print(f"Could not open browser: {e}")
    print("Charts saved as HTML files in 'my_analysis' directory")
```

---

## Tutorial 4: Real-World Application - DAO Governance

### Goal
Model a Decentralized Autonomous Organization (DAO) governance vote.

### Step 1: Define DAO Member Profiles
```python
# Different types of DAO participants
dao_members = [
    VoterProfile(
        id='founding_developer',
        E=9,   # Deep technical expertise
        P=95,  # Always participates
        D=8,   # Good decision history
        A=8,   # Aligned with DAO mission
        S=95   # High token holdings/stake
    ),
    VoterProfile(
        id='active_contributor',
        E=7,   # Good technical knowledge
        P=80,  # Regular participation
        D=7,   # Solid decisions
        A=8,   # Well aligned
        S=70   # Moderate stake
    ),
    VoterProfile(
        id='casual_holder',
        E=4,   # Limited expertise
        P=40,  # Occasional participation
        D=5,   # Mixed decision record
        A=6,   # Somewhat aligned
        S=85   # High financial stake
    ),
    VoterProfile(
        id='new_member',
        E=5,   # Moderate expertise
        P=20,  # New to participation
        D=5,   # No track record yet
        A=7,   # Seems aligned
        S=30   # Small stake
    )
]
```

### Step 2: Model a Treasury Allocation Vote
```python
# Proposal: "Allocate 100,000 tokens for developer incentives"

# Define voting positions based on member types
yes_voters = ['founding_developer', 'active_contributor']  # Developers support
no_voters = ['casual_holder', 'new_member']  # Token holders concerned about dilution

# Different weighting philosophies for DAOs
dao_weights = {
    'token_weighted': WeightCoefficients(0.1, 0.1, 0.1, 0.1, 0.6),  # Stake-heavy
    'contribution_weighted': WeightCoefficients(0.3, 0.4, 0.2, 0.1, 0.0),  # Merit-based
    'balanced': WeightCoefficients(0.2, 0.2, 0.2, 0.2, 0.2)  # Equal
}

# Run all scenarios
dao_results = {}
for name, weights in dao_weights.items():
    dao_results[name] = run_weighted_yes_no_election(
        dao_members, yes_voters, no_voters, weights, 0.5, bounds
    )
```

### Step 3: Analyze DAO Governance Outcomes
```python
print("DAO Treasury Allocation Vote Results:")
print("=" * 50)

for system, result in dao_results.items():
    status = "PASSED" if result['passed'] else "FAILED"
    yes_pct = result['total_yes'] / (result['total_yes'] + result['total_no']) * 100
    
    print(f"{system.title().replace('_', ' ')}: {status}")
    print(f"  YES: {result['total_yes']:.3f} ({yes_pct:.1f}%)")
    print(f"  NO:  {result['total_no']:.3f} ({100-yes_pct:.1f}%)")
    print()

# Create visualization
dao_chart = create_weighted_vote_chart(
    dao_results,
    title="DAO Treasury Allocation: Different Governance Models"
)

save_all_charts({'dao_governance': dao_chart}, "dao_analysis")
```

---

## Tutorial 5: Academic Research Application

### Goal
Use the system for academic research on voting mechanisms.

### Step 1: Design Research Questions
```python
# Research Question: How does voter expertise weighting affect
# policy outcomes in different demographic distributions?

import random
random.seed(42)  # For reproducible results

# Generate synthetic voter populations
def generate_population(size, expertise_mean, participation_mean):
    """Generate a synthetic voter population."""
    population = []
    for i in range(size):
        # Add some randomness around the means
        expertise = max(0, min(10, random.gauss(expertise_mean, 1.5)))
        participation = max(0, min(100, random.gauss(participation_mean, 15)))
        
        population.append(VoterProfile(
            id=f'voter_{i}',
            E=expertise,
            P=participation,
            D=random.gauss(6, 1),  # Random decision quality
            A=random.gauss(6.5, 1),  # Random alignment
            S=random.gauss(70, 20)  # Random stake
        ))
    
    return population
```

### Step 2: Run Systematic Experiments
```python
# Test different population characteristics
populations = {
    'highly_educated': generate_population(100, expertise_mean=8, participation_mean=75),
    'mixed_education': generate_population(100, expertise_mean=5, participation_mean=60),
    'low_engagement': generate_population(100, expertise_mean=4, participation_mean=40)
}

# Test different expertise weightings
expertise_levels = [0.1, 0.2, 0.3, 0.4, 0.5]

results_matrix = {}

for pop_name, population in populations.items():
    results_matrix[pop_name] = {}
    
    for expertise_weight in expertise_levels:
        # Create weighting system
        remaining_weight = (1.0 - expertise_weight) / 4
        weights = WeightCoefficients(
            wE=expertise_weight,
            wP=remaining_weight,
            wD=remaining_weight,
            wA=remaining_weight,
            wS=remaining_weight
        )
        
        # Simulate random yes/no split
        pop_size = len(population)
        yes_count = int(pop_size * 0.45)  # 45% vote yes
        
        yes_voters = [p.id for p in population[:yes_count]]
        no_voters = [p.id for p in population[yes_count:]]
        
        # Run vote
        result = run_weighted_yes_no_election(
            population, yes_voters, no_voters, weights, 0.5, bounds
        )
        
        results_matrix[pop_name][expertise_weight] = result['passed']
```

### Step 3: Analyze Results
```python
import pandas as pd

# Convert results to DataFrame for analysis
data = []
for pop_name, results in results_matrix.items():
    for expertise_weight, passed in results.items():
        data.append({
            'Population': pop_name,
            'Expertise_Weight': expertise_weight,
            'Motion_Passed': passed
        })

df = pd.DataFrame(data)

# Print summary
print("Research Results: Impact of Expertise Weighting")
print("=" * 50)

for pop_name in populations.keys():
    pop_data = df[df['Population'] == pop_name]
    pass_rate = pop_data['Motion_Passed'].mean()
    print(f"{pop_name.replace('_', ' ').title()}: {pass_rate:.1%} pass rate")

# Find tipping points
print("\nExpertise Weight Tipping Points:")
for pop_name in populations.keys():
    pop_data = df[df['Population'] == pop_name]
    
    # Find where outcome changes
    for i in range(len(expertise_levels) - 1):
        current = pop_data[pop_data['Expertise_Weight'] == expertise_levels[i]]['Motion_Passed'].iloc[0]
        next_val = pop_data[pop_data['Expertise_Weight'] == expertise_levels[i+1]]['Motion_Passed'].iloc[0]
        
        if current != next_val:
            print(f"  {pop_name}: Outcome changes between {expertise_levels[i]} and {expertise_levels[i+1]}")
```

---

## Best Practices

### 1. Data Validation
Always validate inputs before running simulations:
```python
def validate_weights(coeffs):
    """Ensure weight coefficients sum to 1.0."""
    total = coeffs.wE + coeffs.wP + coeffs.wD + coeffs.wA + coeffs.wS
    if abs(total - 1.0) > 0.001:
        raise ValueError(f"Weights sum to {total}, must sum to 1.0")

def validate_ballots(ballots, candidates):
    """Ensure all ballot entries are valid candidate IDs."""
    candidate_ids = {c.id for c in candidates}
    for ballot in ballots:
        for candidate_id in ballot:
            if candidate_id not in candidate_ids:
                raise ValueError(f"Unknown candidate ID: {candidate_id}")
```

### 2. Reproducible Results
Use fixed random seeds for academic research:
```python
import random
random.seed(12345)  # Fixed seed for reproducibility
```

### 3. Clear Documentation
Document your assumptions and methodology:
```python
# Document your voter profile methodology
"""
Voter Profiles Methodology:
- Expertise (E): Based on educational background and subject knowledge (0-10 scale)
- Participation (P): Historical voting frequency over past 5 years (0-100 percentage)
- Decision Quality (D): Consistency of past votes with long-term outcomes (0-10 scale)
- Alignment (A): Correlation with public interest measures (0-10 scale)
- Stake (S): Financial/personal impact of decisions (0-100 relative scale)
"""
```

### 4. Sensitivity Analysis
Test how sensitive your results are to parameter changes:
```python
# Test sensitivity to threshold changes
thresholds = [0.45, 0.50, 0.55, 0.60]
for threshold in thresholds:
    result = run_weighted_yes_no_election(profiles, yes_voters, no_voters, weights, threshold, bounds)
    print(f"Threshold {threshold}: {'PASSED' if result['passed'] else 'FAILED'}")
```

### 5. Performance Monitoring
For large simulations, monitor performance:
```python
import time

start_time = time.time()
results = run_election(candidates, large_ballot_list)
elapsed = time.time() - start_time

print(f"Election completed in {elapsed:.2f} seconds")
print(f"Processed {len(large_ballot_list)} ballots")
print(f"Rate: {len(large_ballot_list)/elapsed:.0f} ballots/second")
```

## Troubleshooting

### Common Issues

**Charts not displaying:**
- Check that matplotlib and plotly are installed
- Ensure you have a display/browser available
- Try saving charts to files instead

**Slow performance:**
- Reduce round duration for testing
- Use smaller ballot sets for development
- Consider using quick_demo.py for rapid iteration

**Unexpected voting outcomes:**
- Verify weight coefficients sum to 1.0
- Check voter profile bounds are set correctly
- Ensure ballot preferences are in correct order

**Import errors:**
- Make sure you're in the correct directory
- Check that all required packages are installed
- Verify Python version compatibility (3.7+)

Remember: The goal is to explore how different democratic mechanisms affect outcomes. Experiment with different scenarios and document your findings!
