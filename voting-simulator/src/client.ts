import {
  VoterProfile,
  WeightCoefficients
} from './types';
import {
  runWeightedYesNoElection
} from './election';

// 1. Define sample profiles & params (same as in index.ts)
const profiles: VoterProfile[] = [
  { id: 'alice', E: 8, P: 50, D: 7, A: 9, S: 100 },
  { id: 'bob',   E: 5, P: 20, D: 6, A: 4, S: 50 },
  { id: 'carol', E: 9, P: 80, D: 8, A: 8, S: 75 }
];
const coeffs: WeightCoefficients = {
  wE: 0.3, wP: 0.2, wD: 0.3, wA: 0.1, wS: 0.1
};
const bounds = {
  min: { id: '', E: 0, P: 0, D: 0, A: 0, S: 0 },
  max: { id: '', E: 10, P: 100, D: 10, A: 10, S: 100 }
};
const yesIds = ['alice','carol'];
const noIds  = ['bob'];

// 2. Run the vote
const res = runWeightedYesNoElection(
  profiles, yesIds, noIds,
  coeffs, 0.5,
  bounds
);

// 3. Render into the page
const container = document.getElementById('results')!;
container.innerHTML = `
  <div class="result">
    <strong>Passed?</strong> ${res.passed}
  </div>
  <div class="result">
    <strong>Total Yes Weight:</strong> ${res.totalYes.toFixed(2)}
  </div>
  <div class="result">
    <strong>Total No Weight:</strong> ${res.totalNo.toFixed(2)}
  </div>
`;