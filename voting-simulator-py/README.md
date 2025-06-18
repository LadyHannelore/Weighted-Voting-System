# Weighted Voting System

A Python-based simulator for advanced voting systems with weighted voter profiles, designed to account for voter expertise, participation, and other factors in governance decisions.

## Features

- **Weighted Yes/No Voting**: Simulate yes/no votes with weighted voter profiles based on multiple factors:
  - Expertise (E)
  - Participation (P)
  - Decision Quality (D)
  - Alignment (A)
  - Stake (S)

- **Ranked Choice Voting**: Implements a single transferable vote (STV) style election system where voters rank candidates in order of preference.

- **Customizable Weights**: Define coefficient weights for different voter attributes to reflect their importance in the voting process.

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

Example configuration:

```python
# Define voter profiles with raw scores for each attribute
profiles = [
    VoterProfile(id='alice', E=8, P=50, D=7, A=9, S=100),
    VoterProfile(id='bob', E=5, P=20, D=6, A=4, S=50),
    VoterProfile(id='carol', E=9, P=80, D=8, A=8, S=75)
]

# Set weight coefficients (should sum to 1)
coeffs = WeightCoefficients(
    wE=0.3, wP=0.2, wD=0.3, wA=0.1, wS=0.1
)
```

### Run the Simulation

```
python run.py
```

### Understanding Results

The simulator outputs:
- For Yes/No votes: Whether the motion passed, and the weighted totals
- For ranked choice elections: The winner and details for each elimination round

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
