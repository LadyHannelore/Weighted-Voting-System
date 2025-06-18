"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.runWeightedYesNoElection = exports.calculateWeights = exports.runElection = void 0;
// Custom single transferable vote style simulator
function runElection(candidates, ballots) {
    // ...existing code...
    // Implement rounds, tally first preferences, eliminate lowest, transfer votes, etc.
    // Return final winner and per-round details.
    return {
        winner: null,
        roundDetails: []
    };
}
exports.runElection = runElection;
/** Min-Max normalize a score to [0,1] */
function normalize(x, min, max) {
    return max > min ? (x - min) / (max - min) : 0;
}
/** Compute each voter's composite weight */
function calculateWeights(profiles, coeffs, bounds) {
    const W = {};
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
exports.calculateWeights = calculateWeights;
/** Simple weighted yes/no vote */
function runWeightedYesNoElection(profiles, yesVoterIds, noVoterIds, coeffs, threshold, bounds) {
    const weights = calculateWeights(profiles, coeffs, bounds);
    const totalYes = yesVoterIds.reduce((sum, id) => sum + (weights[id] || 0), 0);
    const totalNo = noVoterIds.reduce((sum, id) => sum + (weights[id] || 0), 0);
    const passed = totalYes / (totalYes + totalNo) > threshold;
    return { passed, totalYes, totalNo };
}
exports.runWeightedYesNoElection = runWeightedYesNoElection;
