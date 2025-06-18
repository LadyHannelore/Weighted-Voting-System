export interface Candidate {
  id: string;
  name: string;
}

export type Ballot = string[];  // ordered list of candidate IDs

export interface Results {
  winner: Candidate | null;
  roundDetails: Array<{
    round: number;
    tallies: Record<string, number>;
    eliminated?: string;
  }>;
}

export interface VoterProfile {
  id: string;
  E: number; // expertise raw score
  P: number; // participation raw score
  D: number; // decision-quality raw score
  A: number; // alignment raw score
  S: number; // stake/raw score
}

export interface WeightCoefficients {
  wE: number;
  wP: number;
  wD: number;
  wA: number;
  wS: number;
}
