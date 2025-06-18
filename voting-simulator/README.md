# UK Voting Simulator

A TypeScript-based simulator for voting systems with weighted voter profiles and alternative vote (ranked choice) elections.

## Features

- **Weighted Yes/No Voting**: Simulate yes/no votes with weighted voter profiles based on multiple factors:
  - Expertise (E)
  - Participation (P)
  - Decision Quality (D)
  - Alignment (A)
  - Stake (S)

- **Ranked Choice Voting**: Implements a single transferable vote (STV) style election system where voters rank candidates in order of preference.

- **Customizable Weights**: Define coefficient weights for different voter attributes to reflect their importance in the voting process.

## Setup

1. Clone the repository
2. Navigate to the voting-simulator directory
3. Install dependencies:
   ```
   npm install
   ```
4. Build the project:
   ```
   npm run build
   ```

## Usage

### Configure Your Simulation

Edit `src/index.ts` to:

1. Define candidates and voter profiles
2. Set up weighted coefficient values
3. Specify bounds for normalization
4. Configure yes/no votes or ranked ballots

Example configuration:

```typescript
// Define voter profiles with raw scores for each attribute
const profiles: VoterProfile[] = [
  { id: 'alice', E: 8, P: 50, D: 7, A: 9, S: 100 },
  { id: 'bob',   E: 5, P: 20, D: 6, A: 4, S: 50 },
  { id: 'carol', E: 9, P: 80, D: 8, A: 8, S: 75 }
];

// Set weight coefficients (should sum to 1)
const coeffs: WeightCoefficients = {
  wE: 0.3, wP: 0.2, wD: 0.3, wA: 0.1, wS: 0.1
};
```

### Run the Simulation

```
npm start
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
