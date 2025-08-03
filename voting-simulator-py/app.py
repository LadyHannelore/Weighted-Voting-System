"""
Flask web application for the UK Weighted Voting System.
Provides an interactive web interface for running voting simulations.
"""

from flask import Flask, render_template, request, jsonify, send_file, Response
import os
import tempfile
import threading
import time
import random
import uuid

from vote_types import (
    Candidate, VoterProfile, WeightCoefficients, Results
)
from election import run_weighted_yes_no_election, run_election_web
from visualization import (
    create_weighted_vote_chart,
    create_ranked_choice_visualization,
    create_voter_profile_heatmap,
    create_first_preferences_pie_chart
)
from voting_systems import (
    plurality, anti_plurality, borda_count, dowdall, veto,
    five_three_one, two_round_runoff, instant_runoff, coombs, bucklin,
    baldwin, nanson, minimax, copeland, black_rule,
    smith_irv, ranked_pairs, schulze_method, kemeny_young,
    dodgson, young, random_dictatorship
)

app = Flask(__name__)

# Global variables for simulation state
simulation_state = {
    'weighted_results': None,
    'ranked_results': None,
    'current_round': 0,
    'is_running': False,
    'round_duration': 5  # Default 5 seconds for web interface
}
# Mapping rule names to functions for ranking-based rules
rule_funcs = {
    'plurality': plurality,
    'anti_plurality': anti_plurality,
    'borda_count': borda_count,
    'dowdall': dowdall,
    'veto': veto,
    'five_three_one': five_three_one,
    'two_round_runoff': two_round_runoff,
    'instant_runoff': instant_runoff,
    'coombs': coombs,
    'bucklin': bucklin,
    'baldwin': baldwin,
    'nanson': nanson,
    'minimax': minimax,
    'copeland': copeland,
    'black_rule': black_rule,
    'smith_irv': smith_irv,
    'ranked_pairs': ranked_pairs,
    'schulze_method': schulze_method,
    'kemeny_young': kemeny_young,
    'dodgson': dodgson,
    'young': young,
    'random_dictatorship': random_dictatorship
}


def get_uk_parties():
    """Get the UK political parties for the simulation."""
    return [
        Candidate(id="conservative", name="Conservative and Unionist Party"),
        Candidate(id="labour", name="Labour Party"),
        Candidate(id="libdem", name="Liberal Democrats"),
        Candidate(id="reform", name="Reform UK"),
        Candidate(id="green", name="Green Party"),
        Candidate(id="snp", name="Scottish National Party"),
        Candidate(id="plaid", name="Plaid Cymru")
    ]


def get_voter_profiles():
    """Get predefined UK voter demographic profiles."""
    return [
        VoterProfile(id="urban_professionals", E=8, P=75, D=7, A=6, S=80,
                     name="Urban Professionals", count=25),
        VoterProfile(id="rural_voters", E=6, P=85, D=8, A=8, S=85,
                     name="Rural Voters", count=20),
        VoterProfile(id="students", E=7, P=60, D=6, A=7, S=70,
                     name="Students & Young Adults", count=15),
        VoterProfile(id="retirees", E=7, P=90, D=9, A=8, S=75,
                     name="Retirees", count=20),
        VoterProfile(id="working_class", E=5, P=70, D=7, A=8, S=90,
                     name="Working Class", count=25),
        VoterProfile(id="young_professionals", E=7, P=65, D=6, A=6, S=75,
                     name="Young Professionals", count=18),
        VoterProfile(id="business_owners", E=8, P=80, D=8, A=5, S=95,
                     name="Business Owners", count=12),
        VoterProfile(id="public_sector", E=7, P=85, D=8, A=9, S=80,
                     name="Public Sector Workers", count=15),
        VoterProfile(id="first_time_voters", E=5, P=45, D=5, A=7, S=65,
                     name="First-time Voters", count=10)
    ]


def generate_ballots_for_election(candidates, voter_profiles):
    """Generate ranked choice ballots for election."""
    ballots = []

    # Regional voting patterns for UK parties
    regional_preferences = {
        "urban_professionals": ["labour", "libdem", "green"],
        "rural_voters": ["conservative", "reform", "libdem"],
        "students": ["green", "labour", "libdem"],
        "retirees": ["conservative", "labour", "libdem"],
        "working_class": ["labour", "conservative", "reform"],
        "young_professionals": ["labour", "libdem", "green"],
        "business_owners": ["conservative", "reform", "libdem"],
        "public_sector": ["labour", "libdem", "green"],
        "first_time_voters": ["green", "labour", "libdem"]
    }

    for profile in voter_profiles:
        base_preferences = regional_preferences.get(
            profile.id, ["labour", "conservative", "libdem"])

        for _ in range(profile.count):
            # Create realistic preference ordering with some randomization
            preferences = base_preferences.copy()
            remaining = [c.id for c in candidates if c.id not in preferences]
            random.shuffle(remaining)

            # Add remaining candidates randomly
            full_preferences = preferences + remaining

            # Sometimes shuffle the order slightly for realism
            if random.random() < 0.3:
                random.shuffle(full_preferences)

            ballots.append(full_preferences[:min(5, len(full_preferences))])

    return ballots


@app.route('/')
def index():
    """Main page of the web application."""
    return render_template('index.html')


@app.route('/weighted-vote')
def weighted_vote_page():
    """Weighted voting simulation page."""
    return render_template('weighted_vote.html')


@app.route('/ranked-choice')
def ranked_choice_page():
    """Ranked choice voting simulation page."""
    return render_template('ranked_choice.html')


@app.route('/api/run-weighted-vote', methods=['POST'])
def api_run_weighted_vote():
    """API endpoint to run weighted vote simulation."""
    try:
        data = request.get_json()

        # Get voter profiles
        voter_profiles = get_voter_profiles()

        # Define voting groups for EU referendum
        yes_ids = [
            'urban_professionals',
            'students',
            'young_professionals',
            'public_sector',
            'first_time_voters']
        no_ids = ['rural_voters', 'retirees', 'working_class', 'business_owners']

        # Define weighting systems
        equal_weights = WeightCoefficients(0.2, 0.2, 0.2, 0.2, 0.2)
        expertise_weights = WeightCoefficients(0.4, 0.3, 0.1, 0.1, 0.1)
        stake_weights = WeightCoefficients(0.1, 0.1, 0.1, 0.3, 0.4)

        # Define bounds for normalization
        bounds = {
            "min": VoterProfile(id='', E=0, P=0, D=0, A=0, S=0),
            "max": VoterProfile(id='', E=10, P=100, D=10, A=10, S=100)
        }

        # Run simulations
        results = {
            'equal': run_weighted_yes_no_election(
                voter_profiles,
                yes_ids,
                no_ids,
                equal_weights,
                0.5,
                bounds),
            'expertise': run_weighted_yes_no_election(
                voter_profiles,
                yes_ids,
                no_ids,
                expertise_weights,
                0.5,
                bounds),
            'stake': run_weighted_yes_no_election(
                voter_profiles,
                yes_ids,
                no_ids,
                stake_weights,
                0.5,
                bounds)}

        # Store results globally for chart generation
        simulation_state['weighted_results'] = results

        return jsonify({
            'success': True,
            'results': {                'equal': {
                    'yes_votes': results['equal']['total_yes'],
                    'no_votes': results['equal']['total_no'],
                    'yes_percentage': (results['equal']['total_yes'] /
                                       (results['equal']['total_yes'] +
                                        results['equal']['total_no']) * 100),
                    'no_percentage': (results['equal']['total_no'] /
                                      (results['equal']['total_yes'] +
                                       results['equal']['total_no']) * 100),
                    'result': 'PASSED' if results['equal']['passed'] else 'FAILED'
                },
                'expertise': {
                    'yes_votes': results['expertise']['total_yes'],
                    'no_votes': results['expertise']['total_no'],
                    'yes_percentage': (results['expertise']['total_yes'] /
                                       (results['expertise']['total_yes'] +
                                        results['expertise']['total_no']) * 100),
                    'no_percentage': (results['expertise']['total_no'] /
                                      (results['expertise']['total_yes'] +
                                       results['expertise']['total_no']) * 100),
                    'result': 'PASSED' if results['expertise']['passed'] else 'FAILED'
                },
                'stake': {
                    'yes_votes': results['stake']['total_yes'],
                    'no_votes': results['stake']['total_no'],
                    'yes_percentage': (results['stake']['total_yes'] /
                                       (results['stake']['total_yes'] +
                                        results['stake']['total_no']) * 100),
                    'no_percentage': (results['stake']['total_no'] /
                                      (results['stake']['total_yes'] +
                                       results['stake']['total_no']) * 100),
                    'result': 'PASSED' if results['stake']['passed'] else 'FAILED'
                }
            },
            'voter_profiles': [
                {
                    'name': p.name,
                    'count': p.count,
                    'expertise': p.E,
                    'participation': p.P,
                    'decision_quality': p.D,
                    'alignment': p.A,
                    'stake': p.S
                } for p in voter_profiles
            ]
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/run-ranked-choice', methods=['POST'])
def api_run_ranked_choice():
    """API endpoint to run ranked choice election simulation."""
    global simulation_state

    try:
        data = request.get_json()
        round_duration = data.get('round_duration', 5)
        rule = data.get('rule', 'instant_runoff')

        # Get parties and voter profiles
        candidates = get_uk_parties()
        voter_profiles = get_voter_profiles()
        ballots = generate_ballots_for_election(candidates, voter_profiles)

        # Reset simulation state
        simulation_state['is_running'] = True
        simulation_state['current_round'] = 0
        simulation_state['round_duration'] = round_duration

        # Run the selected voting rule
        func = rule_funcs.get(rule)
        if func:
            # For rules expecting (candidates, ballots)
            results = func(candidates, ballots)
        else:
            results = run_election_web(candidates, ballots)

        # Store results
        simulation_state['ranked_results'] = results
        simulation_state['is_running'] = False
        simulation_state['current_round'] = len(results.round_details)

        return jsonify({
            'success': True,
            'results': {
                'winner': results.winner.name if results.winner else 'No winner',
                'total_rounds': len(results.round_details),
                'rounds': [
                    {
                        'round_num': r['round'],
                        'vote_counts': r['tallies'],
                        'eliminated': r.get('eliminated', None)
                    } for r in results.round_details
                ]
            }
        })

    except Exception as e:
        simulation_state['is_running'] = False
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/run-ranked-choice-timed', methods=['POST'])
def api_run_ranked_choice_timed():
    """API endpoint to run ranked choice election with timed rounds for web display."""
    global simulation_state

    try:
        data = request.get_json()
        round_duration = data.get('round_duration', 5)
        rule = data.get('rule', 'instant_runoff')

        # Get parties and voter profiles
        candidates = get_uk_parties()
        voter_profiles = get_voter_profiles()
        ballots = generate_ballots_for_election(candidates, voter_profiles)

        # Precompute full results for selected rule
        func = rule_funcs.get(rule)
        if func:
            full_results = func(candidates, ballots)
        else:
            full_results = run_election_web(candidates, ballots)
        # Reset simulation state
        simulation_state['is_running'] = True
        simulation_state['current_round'] = 0
        simulation_state['round_duration'] = round_duration
        simulation_state['ranked_results'] = None
        simulation_state['current_results'] = []

        # Start animation thread: reveal one round at a time
        def run_timed_election():
            global simulation_state
            for rd in full_results.round_details:
                if not simulation_state['is_running']:
                    break
                simulation_state['current_results'].append(rd)
                simulation_state['current_round'] = rd.get('round', len(simulation_state['current_results']))
                time.sleep(round_duration)
            # Animation done
            simulation_state['is_running'] = False
            simulation_state['ranked_results'] = full_results

        election_thread = threading.Thread(target=run_timed_election)
        election_thread.daemon = True
        election_thread.start()

        return jsonify({
            'success': True,
            'message': 'Election started with timed rounds',
            'round_duration': round_duration
        })

    except Exception as e:
        simulation_state['is_running'] = False
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/simulation-status')
def api_simulation_status():
    """Get current simulation status."""
    return jsonify({
        'is_running': simulation_state['is_running'],
        'current_round': simulation_state['current_round']
    })


@app.route('/api/election-progress')
def api_election_progress():
    """Get current election progress and results."""
    global simulation_state

    response_data = {
        'is_running': simulation_state['is_running'],
        'current_round': simulation_state['current_round'],
        'round_duration': simulation_state['round_duration']
    }

    # Include current results if available
    if 'current_results' in simulation_state:
        response_data['current_results'] = simulation_state['current_results']

    # Include final results if election is complete
    if not simulation_state['is_running'] and simulation_state['ranked_results']:
        results = simulation_state['ranked_results']
        response_data['final_results'] = {
            'winner': results.winner.name if results.winner else 'No winner',
            'total_rounds': len(results.round_details),
            'rounds': [
                {
                    'round_num': r['round'],
                    'vote_counts': r['tallies'],
                    'eliminated': r.get('eliminated', None)
                } for r in results.round_details
            ]
        }

    return jsonify(response_data)


# Global variable to store generated chart files
chart_cache = {}

@app.route('/api/generate-chart/<chart_type>')
def api_generate_chart(chart_type):
    """Generate and return chart data."""
    try:
        chart = None

        if chart_type == 'weighted-comparison':
            if simulation_state.get('weighted_results'):
                # Adapt results for the chart function
                formatted_results = {
                    "Equal Weights": simulation_state['weighted_results']['equal'],
                    "Expertise Focus": simulation_state['weighted_results']['expertise'],
                    "Stake Focus": simulation_state['weighted_results']['stake']}
                chart = create_weighted_vote_chart(
                    formatted_results, "UK Rejoining EU - Different Weighting Systems")
            else:
                return jsonify(
                    {'error': 'No weighted voting results available. Run a weighted vote simulation first.'}), 404

        elif chart_type == 'ranked-choice':
            if simulation_state.get(
                    'ranked_results') and simulation_state['ranked_results'] is not None:
                candidates = get_uk_parties()
                chart = create_ranked_choice_visualization(
                    simulation_state['ranked_results'], candidates)
            else:
                return jsonify(
                    {'error': 'No ranked choice results available. Run a ranked choice election first.'}), 404

        elif chart_type == 'voter-profiles':
            voter_profiles = get_voter_profiles()
            chart = create_voter_profile_heatmap(voter_profiles)

        elif chart_type == 'first-preferences':
            candidates = get_uk_parties()
            voter_profiles = get_voter_profiles()
            ballots = generate_ballots_for_election(candidates, voter_profiles)
            chart = create_first_preferences_pie_chart(ballots, candidates)

        else:
            return jsonify({'error': f'Unknown chart type: {chart_type}'}), 404

        if chart is not None and hasattr(chart, 'to_html'):
            # Generate unique filename and store in cache
            chart_id = str(uuid.uuid4())
            chart_cache[chart_id] = chart.to_html()
            
            # Return JSON with chart URL instead of HTML
            return jsonify({
                'success': True,
                'chart_url': f'/chart/{chart_id}'
            })
        else:
            return jsonify(
                {'error': 'Chart generation failed or chart object is invalid'}), 500

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Chart generation error for {chart_type}: {error_details}")
        return jsonify({'error': f'Chart generation error: {str(e)}',
                       'details': error_details}), 500


@app.route('/chart/<chart_id>')
def serve_chart(chart_id):
    """Serve cached chart HTML."""
    if chart_id in chart_cache:
        return Response(chart_cache[chart_id], mimetype='text/html')
    else:
        return "Chart not found", 404


if __name__ == '__main__':
    # Create templates and static directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)

    print("🌐 Starting UK Weighted Voting System Web Interface...")
    print("📊 Access the application at: http://localhost:5000")
    print("🗳️ Features: Weighted voting, ranked choice, real-time charts")

    app.run(debug=True, host='0.0.0.0', port=5000)
