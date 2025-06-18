"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const election_1 = require("./election");
const election_2 = require("./election");
// Load candidates and ballots from JSON or define inline
const candidates = [ /* ... */];
const ballots = [ /* ... */];
// Example voter profiles (scores must be in your defined raw ranges)
const profiles = [
    { id: 'alice', E: 8, P: 50, D: 7, A: 9, S: 100 },
    { id: 'bob', E: 5, P: 20, D: 6, A: 4, S: 50 },
    { id: 'carol', E: 9, P: 80, D: 8, A: 8, S: 75 }
];
// Define coefficient weights summing to 1
const coeffs = {
    wE: 0.3, wP: 0.2, wD: 0.3, wA: 0.1, wS: 0.1
};
// Define min/max bounds for normalization
const bounds = {
    min: { id: '', E: 0, P: 0, D: 0, A: 0, S: 0 },
    max: { id: '', E: 10, P: 100, D: 10, A: 10, S: 100 }
};
// Simulate a yes/no vote
const yesIds = ['alice', 'carol'];
const noIds = ['bob'];
const result = (0, election_2.runWeightedYesNoElection)(profiles, yesIds, noIds, coeffs, 0.5, bounds);
console.log('Passed?', result.passed);
console.log('Weights yes/no:', result.totalYes, '/', result.totalNo);
const results = (0, election_1.runElection)(candidates, ballots);
console.log('Winner:', results.winner);
console.log('Details:', results.roundDetails);
