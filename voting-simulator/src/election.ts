import { Candidate, Ballot, Results, VoterProfile, WeightCoefficients } from './types';

// Custom single transferable vote style simulator
export function runElection(
  candidates: Candidate[],
  ballots: Ballot[]
): Results {
  // ...existing code...
  // Implement rounds, tally first preferences, eliminate lowest, transfer votes, etc.
  // Return final winner and per-round details.
  return {
    winner: null,
    roundDetails: []
  };
}

/** Min-Max normalize a score to [0,1] */
function normalize(x: number, min: number, max: number): number {
  return max > min ? (x - min) / (max - min) : 0;
}

/** Compute each voter's composite weight */
export function calculateWeights(
  profiles: VoterProfile[],
  coeffs: WeightCoefficients,
  bounds: { min: VoterProfile; max: VoterProfile }
): Record<string, number> {
  const W: Record<string, number> = {};
  for (const p of profiles) {
    const E = normalize(p.E, bounds.min.E, bounds.max.E);
    const P = normalize(p.P, bounds.min.P, bounds.max.P);
    const D = normalize(p.D, bounds.min.D, bounds.max.D);
    const A = normalize(p.A, bounds.min.A, bounds.max.A);
    const S = normalize(p.S, bounds.min.S, bounds.max.S);
    W[p.id] =
      coeffs.wE * E +
      coeffs.wP * P +
      coeffs.wD * D +
      coeffs.wA * A +
      coeffs.wS * S;
  }
  return W;
}

/** Simple weighted yes/no vote */
export function runWeightedYesNoElection(
  profiles: VoterProfile[],
  yesVoterIds: string[],
  noVoterIds: string[],
  coeffs: WeightCoefficients,
  threshold: number,
  bounds: { min: VoterProfile; max: VoterProfile }
): { passed: boolean; totalYes: number; totalNo: number } {
  const weights = calculateWeights(profiles, coeffs, bounds);
  const totalYes = yesVoterIds.reduce((sum, id) => sum + (weights[id]||0), 0);
  const totalNo = noVoterIds.reduce((sum, id) => sum + (weights[id]||0), 0);
  const passed = totalYes / (totalYes + totalNo) > threshold;
  return { passed, totalYes, totalNo };
}