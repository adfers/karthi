"""
Module to create visualizations for the Python learning tracker.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from functools import lru_cache
from datetime import datetime, timedelta
import gc
import calendar

# Enable garbage collection for better memory management
gc.enable()

# Visualization constants
CHART_HEIGHT_SMALL = 200
CHART_HEIGHT_MEDIUM = 250
CHART_HEIGHT_LARGE = 300
CHART_CONFIG = {'staticPlot': True, 'displayModeBar': False}

@lru_cache(maxsize=4)  # Cache the last 4 calls
def _create_progress_heatmap(progress_data_tuple):
    """Create a heatmap showing the completion status for each day.
    
    Args:
        progress_data_tuple: A tuple representation of progress data for caching
        
    Returns:
        A plotly figure object
    """
    # Convert tuple back to list of dicts for processing
    progress_data = []
    for item_tuple in progress_data_tuple:
        item_dict = {}
        for k, v in item_tuple:
            item_dict[k] = v
        progress_data.append(item_dict)
    
    try:
        # Convert progress data to a format suitable for a heatmap
        days = [f"Day {d['day']}" for d in progress_data]
        completion = [1 if d['completed'] else 0 for d in progress_data]
        
        # Create a DataFrame with the data
        df = pd.DataFrame({
            'Day': days,
            'Completed': completion
        })
        
        # Create the heatmap using Plotly
        fig = px.imshow(
            df['Completed'].values.reshape(1, -1),
            y=['Progress'],
            x=days,
            color_continuous_scale=['lightgrey', 'green'],
            range_color=[0, 1],
            labels=dict(color="Completed")
        )
        
        fig.update_layout(
            height=CHART_HEIGHT_SMALL,
            title="Curriculum Progress",
            coloraxis_showscale=False,
            xaxis_title=None,
            yaxis_title=None
        )
        
        return fig
    except Exception as e:
        # Provide a simple fallback in case of errors
        print(f"Error creating progress heatmap: {e}")
        fig = go.Figure()
        fig.add_annotation(
            text="Could not generate progress chart",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.5, y=0.5
        )
        fig.update_layout(height=CHART_HEIGHT_SMALL)
        return fig
        

# Wrapper function to handle the tuple conversion for caching
def create_progress_heatmap(progress_data):
    """Wrapper function for the cached progress heatmap function."""
    try:
        # Convert list of dicts to tuple of tuples for caching
        progress_tuples = tuple(
            tuple((k, v) for k, v in d.items())
            for d in progress_data
        )
        return _create_progress_heatmap(progress_tuples)
    except Exception as e:
        # If caching fails, fall back to direct rendering
        print(f"Caching error in progress heatmap: {e}")
        fig = go.Figure()
        fig.add_annotation(
            text="Could not generate progress chart",
            showarrow=False,
            xref="paper", yref="paper",
            x=0.5, y=0.5
        )
        fig.update_layout(height=CHART_HEIGHT_SMALL)
        return fig

def create_weekly_progress_chart(weekly_progress):
    """Create a bar chart showing weekly progress."""
    weeks = [f"Week {i+1}" for i in range(len(weekly_progress))]
    fig = go.Figure(data=[
        go.Bar(
            x=weeks,
            y=weekly_progress,
            marker_color='#4B89DC'
        )
    ])
    fig.update_layout(
        title="Weekly Progress",
        yaxis_title="Days Completed",
        yaxis=dict(range=[0, 7])
    )
    return fig

def create_weekly_time_chart(weekly_time):
    """Create a bar chart showing time spent per week."""
    weeks = [f"Week {i+1}" for i in range(len(weekly_time))]
    fig = go.Figure(data=[
        go.Bar(
            x=weeks,
            y=weekly_time,
            marker_color='#4B89DC'
        )
    ])
    fig.update_layout(
        title="Time Spent per Week",
        yaxis_title="Minutes"
    )
    return fig

def create_time_spent_chart(progress_data):
    """Create a line chart showing time spent per day."""
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
        title="Time Spent per Day",
        xaxis_title="Day",
        yaxis_title="Minutes"
    )
    return fig

def create_completion_gauge(percentage):
    """Create a gauge chart showing completion percentage."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = percentage,
        domain = {'x': [0, 1], 'y': [0, 1]},
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
    fig.update_layout(title="Overall Completion")
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

        # Create the calendar view
        df = pd.DataFrame({
            'date': dates,
            'value': values
        })

        fig = px.scatter(df, x='date', y='value',
                        title="Learning Streak Calendar (Last 30 Days)")

        # Customize the appearance
        fig.update_traces(marker=dict(size=12,
                                    symbol='square',
                                    color=df['value'].map({0: '#FFE5E5', 1: '#4B89DC'})))
        fig.update_layout(
            yaxis=dict(showticklabels=False, showgrid=False),
            plot_bgcolor='white'
        )

        return fig

    except Exception as e:
        # Fallback if calendar generation fails
        fig = go.Figure()
        fig.update_layout(
            title="Learning Streak Calendar (Last 30 Days)",
            annotations=[dict(
                text=f"Could not generate calendar view: {str(e)}",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5
            )]
        )
        return fig