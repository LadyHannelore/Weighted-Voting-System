"""
Visualization module for the UK Weighted Voting System
Provides charts and graphs for election results and weighted voting outcomes
"""

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import List, Dict
from vote_types import Results, VoterProfile


def create_weighted_vote_chart(
        results_dict: Dict[str, Dict], title: str = "Weighted Voting Results"):
    """
    Create a bar chart comparing different weighting systems for yes/no votes
    """
    systems = list(results_dict.keys())
    yes_votes = [results_dict[system]['total_yes'] for system in systems]
    no_votes = [results_dict[system]['total_no'] for system in systems]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='YES',
        x=systems,
        y=yes_votes,
        marker_color='green',
        text=[f"{vote:.2f}" for vote in yes_votes],
        textposition='auto'
    ))

    fig.add_trace(go.Bar(
        name='NO',
        x=systems,
        y=no_votes,
        marker_color='red',
        text=[f"{vote:.2f}" for vote in no_votes],
        textposition='auto'
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Weighting System",
        yaxis_title="Weighted Vote Count",
        barmode='group',
        showlegend=True
    )

    return fig


def create_ranked_choice_visualization(results: Results, candidates: List):
    """
    Create visualization for ranked choice voting results
    """
    if not results.round_details:
        return None

    # Prepare data for visualization
    rounds_data = []
    candidate_names = {c.id: c.name for c in candidates}

    for round_detail in results.round_details:
        for candidate_id, votes in round_detail["tallies"].items():
            rounds_data.append({
                'Round': round_detail["round"],
                'Candidate': candidate_names.get(candidate_id, candidate_id),
                'Votes': votes,
                'Eliminated': candidate_id == round_detail.get("eliminated", "")
            })

    df = pd.DataFrame(rounds_data)

    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Vote Progression by Round', 'Final Results'),
        row_heights=[0.7, 0.3]
    )

    # Line chart showing vote progression
    for candidate in df['Candidate'].unique():
        candidate_data = df[df['Candidate'] == candidate]
        fig.add_trace(
            go.Scatter(
                x=candidate_data['Round'],
                y=candidate_data['Votes'],
                mode='lines+markers',
                name=candidate,
                line=dict(width=3),
                marker=dict(size=8)
            ),
            row=1, col=1
        )

    # Bar chart for final round
    final_round = df[df['Round'] == df['Round'].max()]
    fig.add_trace(
        go.Bar(
            x=final_round['Candidate'],
            y=final_round['Votes'],
            name='Final Votes',
            marker_color=['gold' if results.winner and c == results.winner.name else 'lightblue'
                          for c in final_round['Candidate']],
            showlegend=False
        ),
        row=2, col=1
    )

    fig.update_layout(
        title="Ranked Choice Voting Results",
        height=800
    )

    fig.update_xaxes(title_text="Round", row=1, col=1)
    fig.update_yaxes(title_text="Votes", row=1, col=1)
    fig.update_xaxes(title_text="Candidate", row=2, col=1)
    fig.update_yaxes(title_text="Final Votes", row=2, col=1)

    return fig


def create_voter_profile_heatmap(profiles: List[VoterProfile]):
    """
    Create a heatmap showing voter profile attributes
    """
    # Prepare data
    profile_data = []
    for profile in profiles:
        profile_data.append({
            'Voter Group': profile.id.replace('_', ' ').title(),
            'Expertise': profile.E,
            'Participation': profile.P,
            'Decision Quality': profile.D,
            'Alignment': profile.A,
            'Stake': profile.S
        })

    df = pd.DataFrame(profile_data)
    df = df.set_index('Voter Group')

    fig = go.Figure(data=go.Heatmap(
        z=df.values,
        x=df.columns,
        y=df.index,
        colorscale='RdYlBu_r',
        text=df.values,
        texttemplate="%{text}",
        textfont={"size": 10},
        colorbar=dict(title="Score")
    ))

    fig.update_layout(
        title="Voter Profile Attributes Heatmap",
        xaxis_title="Attributes",
        yaxis_title="Voter Groups"
    )

    return fig


def create_first_preferences_pie_chart(ballots: List[List[str]], candidates: List):
    """
    Create a pie chart showing first preference distribution
    """
    candidate_names = {c.id: c.name for c in candidates}
    first_prefs = [ballot[0] for ballot in ballots if ballot]

    # Count first preferences
    from collections import Counter
    pref_counts = Counter(first_prefs)

    labels = [candidate_names.get(cid, cid) for cid in pref_counts.keys()]
    values = list(pref_counts.values())

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        textinfo='label+percent',
        textposition='auto'
    )])

    fig.update_layout(
        title="First Preference Distribution",
        annotations=[
            dict(
                text='First<br>Preferences',
                x=0.5,
                y=0.5,
                font_size=16,
                showarrow=False)])

    return fig


def save_all_charts(charts: Dict[str, go.Figure], output_dir: str = "charts"):
    """
    Save all charts as HTML files
    """
    import os

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for chart_name, fig in charts.items():
        if fig is not None:
            filename = f"{output_dir}/{chart_name.replace(' ', '_').lower()}.html"
            fig.write_html(filename)
            print(f"Chart saved: {filename}")


def display_charts_in_browser(charts: Dict[str, go.Figure]):
    """
    Display charts in the default web browser
    """
    for chart_name, fig in charts.items():
        if fig is not None:
            print(f"\nDisplaying: {chart_name}")
            fig.show()
