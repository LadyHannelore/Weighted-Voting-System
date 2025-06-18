# UK Weighted Voting System

A Python-based simulator for advanced voting systems modeled on UK election data, designed to account for voter expertise, participation, and other factors in governance decisions. This simulator uses real data from the 2024 UK General Election to model both ranked choice voting and weighted yes/no policy decisions.

## Features

- **Weighted Yes/No Voting**: Simulate yes/no votes with weighted voter profiles based on multiple factors:
  - Expertise (E)
  - Participation (P)
  - Decision Quality (D)
  - Alignment (A)
  - Stake (S)

- **Ranked Choice Voting**: Implements a single transferable vote (STV) style election system where voters rank candidates in order of preference.

- **Customizable Weights**: Define coefficient weights for different voter attributes to reflect their importance in the voting process.

- **Real-time Simulation**: Each round in ranked choice voting lasts 30 seconds (configurable), showing live results as the election progresses.

- **Interactive Visualizations**: Automatic generation of charts and graphs including:
  - Weighted vote comparison charts
  - Ranked choice progression visualizations  
  - Voter profile heatmaps
  - First preference distribution pie charts

- **System Verification**: Built-in verification that the voting algorithms follow proper ranked choice and weighted voting principles.

## Why Weighted Voting?

Traditional "one person, one vote" systems treat all votes equally, regardless of voters' knowledge, experience, or stake in the outcome. This system addresses that limitation by:

- **Recognizing Expertise**: Giving appropriate weight to those with subject matter knowledge
- **Rewarding Participation**: Valuing consistent engagement in the governance process
- **Accounting for Skin in the Game**: Considering each voter's stake in the outcome
- **Promoting Quality Decision-Making**: Factoring in a voter's history of thoughtful decisions

## Setup

1. Clone the repository
2. Navigate to the project directory
3. (Optional) Create a virtual environment:
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On Unix/MacOS
   ```

## Usage

### Configure Your Simulation

Edit `main.py` to:

1. Define candidates and voter profiles
2. Set up weighted coefficient values
3. Specify bounds for normalization
4. Configure yes/no votes or ranked ballots

Example configuration with UK demographic voter profiles:

```python
# UK voter profiles based on demographic segments
profiles = [
    # Urban professionals 
    VoterProfile(id='urban_professionals', E=8, P=70, D=7, A=6, S=80),
    # Rural communities
    VoterProfile(id='rural_voters', E=7, P=75, D=8, A=7, S=90),
    # University students
    VoterProfile(id='students', E=6, P=40, D=5, A=6, S=85),
    # Retirees
    VoterProfile(id='retirees', E=7, P=90, D=8, A=7, S=95)
]

# Set weight coefficients (should sum to 1)
coeffs = WeightCoefficients(
    wE=0.2, wP=0.2, wD=0.2, wA=0.2, wS=0.2
)
```

The simulation includes real UK political parties:
- Conservative and Unionist Party
- Labour Party
- Liberal Democrats
- Reform UK
- Green Party
- Scottish National Party
- Plaid Cymru

### Run the Simulation

There are several ways to run the simulation:

**Quick Demo (3-second rounds):**
```
python quick_demo.py
```

**Full Demo (30-second rounds):**
```
python full_demo.py
```

**Complete Simulation with Charts:**
```
python run.py
```

**Note:** The full simulation includes 30-second rounds for each elimination in ranked choice voting, making it more realistic but slower. Use the quick demo for testing.

### Understanding Results

The simulator provides detailed outputs for two types of simulations:

#### 1. Weighted Yes/No Policy Vote

Simulates a policy decision (like "UK Rejoining the EU") with different demographic groups voting yes or no. The system runs three different weighting scenarios:
- Equal weights across all voter attributes
- Expertise-focused weights
- Stake-focused weights

For each scenario, the simulator outputs:
- Whether the motion passed (based on weighted majority)
- The total weighted votes for Yes and No
- The percentage breakdown of the vote

Example output:
```
SIMULATION 1: WEIGHTED YES/NO VOTE ON 'UK REJOINING THE EU'
=================================================

Voting Groups:
YES voters: urban_professionals, students, young_professionals, public_sector, first_time_voters
NO voters: rural_voters, retirees, working_class, business_owners

1. Equal weights:
   Passed? True
   YES: 3.220 (51.1%)
   NO:  3.080 (48.9%)
```

#### 2. Ranked Choice Voting

Simulates a general election using the ranked choice (alternative vote) system with UK political parties. The simulator outputs:
- The ultimate winner after all elimination rounds
- Round-by-round vote tallies showing:
  - Each party's vote count and percentage
  - Which party was eliminated in each round
  - How votes transfer between rounds

Example output:
```
Round 1:
  Labour Party: 75 votes (35.7%)
  Conservative and Unionist Party: 50 votes (23.8%)
  Green Party: 30 votes (14.3%)
  Liberal Democrats: 25 votes (11.9%)
  Reform UK: 15 votes (7.1%)
  Scottish National Party: 10 votes (4.8%)
  Plaid Cymru: 5 votes (2.4%)
  Eliminated: Plaid Cymru
```

## Customization

You can customize the voting parameters by modifying:
- The weight coefficients to emphasize different voter attributes
- The threshold required for a motion to pass (default: 0.5 or majority)
- The normalization bounds for each attribute

## Use Cases

### Decentralized Organizations (DAOs)
Perfect for blockchain-based organizations where stake and participation metrics are already tracked on-chain. Expertise and alignment scores can be derived from on-chain reputation systems.

### Community Governance
For communities where the quality and sustainability of decisions depends on long-term thinking and domain expertise.

### Expert Committees
For technical decision-making bodies where both domain knowledge and stakeholder interests must be balanced.

### Corporate Governance
Can be used to balance shareholder voting power with factors such as institutional knowledge and long-term engagement.

## Mathematical Model

The weighted voting system uses a linear combination of normalized metrics:

```
Weight(voter) = wE * norm(E) + wP * norm(P) + wD * norm(D) + wA * norm(A) + wS * norm(S)
```

Where:
- `norm()` is a min-max normalization function
- Coefficients (wE, wP, wD, wA, wS) determine the relative importance of each factor
