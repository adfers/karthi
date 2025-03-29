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
    """Create a bar chart showing progress by week."""
    weeks = ['Week 1', 'Week 2', 'Week 3']
    completed_per_week = weekly_progress
    total_per_week = [7, 7, 7]  # 7 days in each week
    
    df = pd.DataFrame({
        'Week': weeks,
        'Completed': completed_per_week,
        'Total': total_per_week
    })
    
    # Calculate completion percentages
    df['Percentage'] = (df['Completed'] / df['Total']) * 100
    
    # Create the bar chart
    fig = px.bar(
        df,
        x='Week',
        y='Percentage',
        text=df['Completed'].astype(str) + '/' + df['Total'].astype(str),
        color='Week',
        labels={'Percentage': 'Completion %'},
        title='Weekly Progress',
        height=300,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_layout(xaxis_title=None)
    fig.update_yaxes(range=[0, 100])
    
    return fig

def create_time_spent_chart(progress_data):
    """Create a bar chart showing time spent on each day."""
    days = [f"Day {d['day']}" for d in progress_data]
    time_spent = [d['time_spent_minutes'] / 60 for d in progress_data]  # Convert to hours
    
    df = pd.DataFrame({
        'Day': days,
        'Time Spent (hours)': time_spent
    })
    
    fig = px.bar(
        df,
        x='Day',
        y='Time Spent (hours)',
        title='Time Spent on Each Day',
        height=300,
        color='Time Spent (hours)',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(xaxis_title=None, coloraxis_showscale=False)
    
    return fig

def create_completion_gauge(completion_percentage):
    """Create a gauge chart showing overall completion percentage."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=completion_percentage,
        title={'text': "Overall Completion"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "green"},
            'steps': [
                {'range': [0, 33], 'color': "lightgray"},
                {'range': [33, 66], 'color': "gray"},
                {'range': [66, 100], 'color': "darkgray"}
            ],
        }
    ))
    
    fig.update_layout(height=250)
    
    return fig

def create_weekly_time_chart(weekly_time_data):
    """Create a line chart showing time spent per week."""
    weeks = ['Week 1', 'Week 2', 'Week 3']
    
    df = pd.DataFrame({
        'Week': weeks,
        'Time Spent (hours)': weekly_time_data
    })
    
    fig = px.line(
        df,
        x='Week',
        y='Time Spent (hours)',
        markers=True,
        title='Time Spent per Week',
        height=300
    )
    
    fig.update_layout(xaxis_title=None)
    
    return fig

def create_streak_calendar(progress_data):
    """Create a calendar view to visualize learning streaks."""
    try:
        # Get today's date and the date from 30 days ago to show a month's view
        today = datetime.now().date()
        start_date = today - timedelta(days=30)
        
        # Create a list of dates in the range
        date_range = [(start_date + timedelta(days=i)) for i in range(31)]
        
        # Extract completion dates from progress data
        completion_dates = []
        for d in progress_data:
            if d['completed'] and d['completion_date']:
                try:
                    date = datetime.strptime(d['completion_date'], "%Y-%m-%d").date()
                    completion_dates.append(date)
                except (ValueError, TypeError):
                    # Skip invalid dates
                    continue
        
        # Create a dict marking dates with completed activities
        activity_count = {date: 0 for date in date_range}
        for date in completion_dates:
            if date in date_range:
                activity_count[date] = 1
        
        # Convert to a format for the heatmap
        dates = list(activity_count.keys())
        counts = list(activity_count.values())
        
        # Group by week for better visualization
        weeks = []
        days = []
        values = []
        
        for date, count in zip(dates, counts):
            week_num = (date - start_date).days // 7
            day_of_week = date.weekday()
            weeks.append(week_num)
            days.append(day_of_week)
            values.append(count)
        
        # Create a pivot table
        df = pd.DataFrame({
            'Week': weeks,
            'Day': days,
            'Value': values
        })
        
        # Handle empty dataframe case
        if df.empty:
            fig = go.Figure()
            fig.update_layout(
                title="Learning Streak Calendar (Last 30 Days)",
                annotations=[dict(
                    text="No activity data available yet",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5
                )]
            )
            return fig
        
        pivot = df.pivot_table(index='Week', columns='Day', values='Value', fill_value=0)
        
        # Create the heatmap
        day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        week_names = [f"W{i+1}" for i in range(len(pivot))]
        
        fig = px.imshow(
            pivot,
            labels=dict(x="Day of Week", y="Week", color="Activity"),
            x=day_names,
            y=week_names,
            color_continuous_scale=['lightgrey', 'green'],
            title="Learning Streak Calendar (Last 30 Days)"
        )
        
        fig.update_layout(height=250, coloraxis_showscale=False)
        
        return fig
    
    except Exception as e:
        # Fallback to a simple figure with error message
        fig = go.Figure()
        fig.update_layout(
            title="Learning Streak Calendar (Last 30 Days)",
            annotations=[dict(
                text=f"Could not generate calendar view",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5
            )]
        )
        return fig
