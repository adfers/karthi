
"""
Module to create visualizations for the Python learning tracker.
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Visualization constants
CHART_HEIGHT = 300
CHART_CONFIG = {'displayModeBar': False}
DEFAULT_COLOR = '#4B89DC'
ERROR_COLOR = '#FF0000'

def handle_visualization_error(func):
    """Decorator to handle visualization errors gracefully."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            fig = go.Figure()
            fig.add_annotation(
                text=f"Error: {str(e)}",
                showarrow=False,
                xref="paper",
                yref="paper",
                font=dict(color=ERROR_COLOR)
            )
            fig.update_layout(height=CHART_HEIGHT)
            return fig
    return wrapper

@handle_visualization_error
def create_progress_heatmap(progress_data):
    """Create a heatmap showing the completion status for each day."""
    if not progress_data:
        raise ValueError("No progress data available")
        
    days = [f"Day {d['day']}" for d in progress_data]
    completion = [1 if d.get('completed', False) else 0 for d in progress_data]

    fig = px.imshow(
        np.array(completion).reshape(1, -1),
        y=['Progress'],
        x=days,
        color_continuous_scale=['lightgrey', DEFAULT_COLOR],
        range_color=[0, 1]
    )

    fig.update_layout(
        height=CHART_HEIGHT,
        title="Curriculum Progress",
        coloraxis_showscale=False,
        xaxis_title=None,
        yaxis_title=None,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig

@handle_visualization_error
def create_weekly_progress_chart(weekly_progress):
    """Create a bar chart showing weekly progress."""
    if not isinstance(weekly_progress, (list, tuple)):
        raise ValueError("Weekly progress must be a list or tuple")
        
    weeks = [f"Week {i+1}" for i in range(len(weekly_progress))]
    fig = go.Figure(data=[
        go.Bar(
            x=weeks,
            y=weekly_progress,
            marker_color=DEFAULT_COLOR
        )
    ])

    fig.update_layout(
        height=CHART_HEIGHT,
        title="Weekly Progress",
        yaxis_title="Days Completed",
        yaxis=dict(range=[0, 7]),
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig

@handle_visualization_error
def create_weekly_time_chart(weekly_time):
    """Create a bar chart showing time spent per week."""
    if not isinstance(weekly_time, (list, tuple)):
        raise ValueError("Weekly time must be a list or tuple")
        
    weeks = [f"Week {i+1}" for i in range(len(weekly_time))]
    fig = go.Figure(data=[
        go.Bar(
            x=weeks,
            y=weekly_time,
            marker_color=DEFAULT_COLOR
        )
    ])

    fig.update_layout(
        height=CHART_HEIGHT,
        title="Time Spent per Week",
        yaxis_title="Minutes",
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig

@handle_visualization_error
def create_time_spent_chart(progress_data):
    """Create a line chart showing time spent per day."""
    if not progress_data:
        raise ValueError("No progress data available")
        
    days = list(range(1, len(progress_data) + 1))
    times = [day.get('time_spent_minutes', 0) for day in progress_data]

    fig = go.Figure(data=go.Scatter(
        x=days,
        y=times,
        mode='lines+markers',
        line=dict(color=DEFAULT_COLOR),
        marker=dict(size=8)
    ))

    fig.update_layout(
        height=CHART_HEIGHT,
        title="Time Spent per Day",
        xaxis_title="Day",
        yaxis_title="Minutes",
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig

@handle_visualization_error
def create_completion_gauge(percentage):
    """Create a gauge chart showing completion percentage."""
    if not isinstance(percentage, (int, float)) or percentage < 0 or percentage > 100:
        raise ValueError("Percentage must be a number between 0 and 100")
        
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=percentage,
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': DEFAULT_COLOR},
            'steps': [
                {'range': [0, 33], 'color': "#FFE5E5"},
                {'range': [33, 66], 'color': "#FFD6A5"},
                {'range': [66, 100], 'color': "#CAFFBF"}
            ]
        }
    ))

    fig.update_layout(
        height=CHART_HEIGHT,
        title="Overall Completion",
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig

@handle_visualization_error
def create_streak_calendar(progress_data):
    """Create a calendar view of learning streaks."""
    if not progress_data:
        raise ValueError("No progress data available")
        
    dates = []
    values = []
    today = datetime.now()

    for i in range(30):
        date = today - timedelta(days=i)
        dates.append(date)
        
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
        color=df['value'].map({0: '#FFE5E5', 1: DEFAULT_COLOR})
    ))

    fig.update_layout(
        height=CHART_HEIGHT,
        yaxis=dict(showticklabels=False, showgrid=False),
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig
