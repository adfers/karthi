
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pandas as pd

def create_completion_gauge(percentage):
    """Create a gauge chart showing completion percentage."""
    try:
        # Ensure percentage is a valid number
        percentage = float(percentage)
        if not 0 <= percentage <= 100:
            percentage = max(0, min(100, percentage))  # Clamp between 0 and 100
            
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = percentage,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Completion"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#4B89DC"},
                'steps': [
                    {'range': [0, 33], 'color': "#FFE5E5"},
                    {'range': [33, 66], 'color': "#FFD6A5"},
                    {'range': [66, 100], 'color': "#CAFFBF"}
                ]
            }
        ))
        fig.update_layout(height=200, margin=dict(l=10, r=10, t=40, b=10))
        return fig
    except Exception as e:
        print(f"Error creating completion gauge: {e}")
        return go.Figure()  # Return empty figure on error

def create_weekly_progress_chart(weekly_progress):
    """Create a bar chart showing weekly progress."""
    try:
        if not weekly_progress or not isinstance(weekly_progress, (list, tuple)):
            return go.Figure()  # Return empty figure if data is invalid
            
        weeks = [f"Week {i+1}" for i in range(len(weekly_progress))]
        fig = go.Figure(data=[
            go.Bar(
                x=weeks,
                y=weekly_progress,
                marker_color='#4B89DC',
                text=weekly_progress,
                textposition='auto'
            )
        ])
        fig.update_layout(
            title="Weekly Progress",
            xaxis_title="Week",
            yaxis_title="Completed Days",
            height=300
        )
        return fig
    except Exception as e:
        print(f"Error creating weekly progress chart: {e}")
        return go.Figure()  # Return empty figure on error
        yaxis_title="Completed Days",
        height=300
    )
    return fig

def create_progress_heatmap(progress_data):
    """Create a heatmap showing daily progress."""
    # Convert progress data to format needed for heatmap
    days = list(range(1, 22))
    completion = [1 if d.get('completed', False) else 0 for d in progress_data]
    
    fig = px.imshow(
        [completion],
        labels=dict(x="Day", y="Progress", color="Completed"),
        x=days,
        color_continuous_scale=["#FFE5E5", "#4B89DC"]
    )
    fig.update_layout(
        title="Progress Heatmap",
        height=200,
        xaxis_title="Day",
        yaxis_visible=False
    )
    return fig

def create_time_spent_chart(progress_data):
    """Create a line chart showing time spent per day."""
    days = list(range(1, 22))
    times = [d.get('time_spent_minutes', 0) for d in progress_data]
    
    fig = go.Figure(data=go.Scatter(
        x=days,
        y=times,
        mode='lines+markers',
        line=dict(color='#4B89DC')
    ))
    fig.update_layout(
        title="Time Spent Per Day",
        xaxis_title="Day",
        yaxis_title="Minutes",
        height=300
    )
    return fig

def create_streak_calendar(progress_data):
    """Create a calendar heatmap showing activity streaks."""
    dates = []
    values = []
    for day in progress_data:
        if day.get('completion_date'):
            dates.append(day['completion_date'])
            values.append(1)
    
    if dates:
        df = pd.DataFrame({
            'date': dates,
            'value': values
        })
        fig = px.scatter(df, x='date', y='value', color='value')
        fig.update_layout(
            title="Activity Calendar",
            height=200,
            showlegend=False
        )
        return fig
    return go.Figure()
