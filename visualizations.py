"""
Module to create visualizations for the Python learning tracker.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Visualization constants
CHART_HEIGHT = 300
CHART_CONFIG = {'displayModeBar': False}

def create_progress_heatmap(progress_data):
    """Create a heatmap showing the completion status for each day."""
    try:
        days = [f"Day {d['day']}" for d in progress_data]
        completion = [1 if d['completed'] else 0 for d in progress_data]

        # Create the heatmap using Plotly
        fig = px.imshow(
            np.array(completion).reshape(1, -1),
            y=['Progress'],
            x=days,
            color_continuous_scale=['lightgrey', '#4B89DC'],
            range_color=[0, 1]
        )

        fig.update_layout(
            height=CHART_HEIGHT,
            title="Curriculum Progress",
            coloraxis_showscale=False,
            xaxis_title=None,
            yaxis_title=None
        )

        return fig
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=f"Error: {str(e)}", showarrow=False, xref="paper", yref="paper")
        return fig

def create_weekly_progress_chart(weekly_progress):
    """Create a bar chart showing weekly progress."""
    try:
        weeks = [f"Week {i+1}" for i in range(len(weekly_progress))]
        fig = go.Figure(data=[
            go.Bar(
                x=weeks,
                y=weekly_progress,
                marker_color='#4B89DC'
            )
        ])

        fig.update_layout(
            height=CHART_HEIGHT,
            title="Weekly Progress",
            yaxis_title="Days Completed",
            yaxis=dict(range=[0, 7])
        )

        return fig
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=f"Error: {str(e)}", showarrow=False, xref="paper", yref="paper")
        return fig

def create_weekly_time_chart(weekly_time):
    """Create a bar chart showing time spent per week."""
    try:
        weeks = [f"Week {i+1}" for i in range(len(weekly_time))]
        fig = go.Figure(data=[
            go.Bar(
                x=weeks,
                y=weekly_time,
                marker_color='#4B89DC'
            )
        ])

        fig.update_layout(
            height=CHART_HEIGHT,
            title="Time Spent per Week",
            yaxis_title="Minutes"
        )

        return fig
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=f"Error: {str(e)}", showarrow=False, xref="paper", yref="paper")
        return fig

def create_time_spent_chart(progress_data):
    """Create a line chart showing time spent per day."""
    try:
        days = list(range(1, len(progress_data) + 1))
        times = [day.get('time_spent_minutes', 0) for day in progress_data]

        fig = go.Figure(data=go.Scatter(
            x=days,
            y=times,
            mode='lines+markers',
            line=dict(color='#4B89DC'),
            marker=dict(size=8)
        ))

        fig.update_layout(
            height=CHART_HEIGHT,
            title="Time Spent per Day",
            xaxis_title="Day",
            yaxis_title="Minutes"
        )

        return fig
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=f"Error: {str(e)}", showarrow=False, xref="paper", yref="paper")
        return fig

def create_completion_gauge(percentage):
    """Create a gauge chart showing completion percentage."""
    try:
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=percentage,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#4B89DC"},
                'steps': [
                    {'range': [0, 33], 'color': "#FFE5E5"},
                    {'range': [33, 66], 'color': "#FFD6A5"},
                    {'range': [66, 100], 'color': "#CAFFBF"}
                ]
            }
        ))

        fig.update_layout(
            height=CHART_HEIGHT,
            title="Overall Completion"
        )

        return fig
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=f"Error: {str(e)}", showarrow=False, xref="paper", yref="paper")
        return fig

def create_streak_calendar(progress_data):
    """Create a calendar view of learning streaks."""
    try:
        # Get the last 30 days of data
        dates = []
        values = []
        today = datetime.now()

        for i in range(30):
            date = today - timedelta(days=i)
            dates.append(date)

            # Find if there was progress on this date
            day_progress = 0
            for day in progress_data:
                completion_date = day.get('completion_date')
                if completion_date:
                    try:
                        completion_datetime = datetime.strptime(completion_date, "%Y-%m-%d")
                        if completion_datetime.date() == date.date():
                            day_progress = 1
                            break
                    except ValueError:
                        continue

            values.append(day_progress)

        df = pd.DataFrame({
            'date': dates,
            'value': values
        })

        fig = px.scatter(df, x='date', y='value',
                        title="Learning Streak Calendar")

        fig.update_traces(marker=dict(
            size=12,
            symbol='square',
            color=df['value'].map({0: '#FFE5E5', 1: '#4B89DC'})
        ))

        fig.update_layout(
            height=CHART_HEIGHT,
            yaxis=dict(showticklabels=False, showgrid=False),
            plot_bgcolor='white'
        )

        return fig
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=f"Error: {str(e)}", showarrow=False, xref="paper", yref="paper")
        return fig