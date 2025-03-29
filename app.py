"""
Python Learning Tracker - A Streamlit app to track progress through a 21-day Python learning curriculum.
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import calendar
import base64
from io import StringIO
import os
import json

# Import custom modules
import curriculum as curr
import data_handler as dh
import visualizations as viz
import utils

# Page configuration
st.set_page_config(
    page_title="Python Learning Tracker",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
def local_css():
    st.markdown("""
    <style>
    /* General styling */
    h1 {
        color: #3366CC;
        background-color: #F0F8FF;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    h2, h3 {
        color: #3366CC;
        border-bottom: 2px solid #4B89DC;
        padding-bottom: 5px;
    }
    
    /* Styling for cards */
    .stCard {
        border-radius: 15px !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* Style the checkboxes */
    div[data-testid="stCheckbox"] {
        background-color: #F0F8FF;
        padding: 5px;
        border-radius: 5px;
        margin-bottom: 5px;
    }
    
    /* Style the sidebar */
    section[data-testid="stSidebar"] {
        background-color: #F0F8FF;
        border-right: 2px solid #4B89DC;
    }
    
    /* Button styling */
    button {
        background-color: #4B89DC !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    /* Make links stand out */
    a {
        color: #4B89DC !important;
        font-weight: bold !important;
        text-decoration: none !important;
    }
    
    a:hover {
        text-decoration: underline !important;
        color: #2E5CB8 !important;
    }
    
    /* Completion status badges */
    .completed-badge {
        background-color: #28a745;
        color: white;
        padding: 3px 8px;
        border-radius: 10px;
        font-size: 14px;
    }
    
    .incomplete-badge {
        background-color: #dc3545;
        color: white;
        padding: 3px 8px;
        border-radius: 10px;
        font-size: 14px;
    }
    
    /* Day card styling */
    .day-card {
        background-color: #F8F9FA;
        border-left: 5px solid #4B89DC;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    
    .resource-link {
        background-color: #E9ECEF;
        padding: 5px 10px;
        border-radius: 5px;
        margin: 5px 0;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# Ensure data file exists
DATA_FILE = "python_learning_progress.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({
            "progress": {},
            "notes": {},
            "uploads": {},
            "time_spent": {},
            "resources_used": {}
        }, f, indent=4)

# Initialize data
try:
    dh.initialize_data()
except Exception as e:
    st.error(f"Error initializing data: {e}")
    st.info("Please refresh the page to try again.")

# Main app layout
def main():
    # Apply custom CSS
    local_css()
    
    # Sidebar
    with st.sidebar:
        st.title("🐍 Python Learning")
        st.subheader("21-Day Challenge")
        
        # Current progress stats
        completion_percentage = dh.get_completion_percentage()
        current_day = utils.get_current_day()
        current_streak = utils.calculate_learning_streak()
        total_study_time = utils.get_total_study_time()
        
        # Display current stats
        st.metric("Overall Progress", f"{completion_percentage:.1f}%")
        st.metric("Current Day", f"Day {current_day}")
        st.metric("Learning Streak", f"{current_streak} days")
        st.metric("Total Study Time", utils.format_time_display(total_study_time))
        
        # Navigation options
        st.subheader("Navigation")
        page = st.radio(
            "Go to:",
            ["Dashboard", "Day Tracker", "Weekly View", "Notes & Reflections"]
        )
        
        # Additional resources
        st.subheader("Additional Resources")
        st.markdown("""
        - [Python Documentation](https://docs.python.org/3/)
        - [Real Python Tutorials](https://realpython.com/)
        - [Python Discord Community](https://discord.com/invite/python)
        """)
        
        # Show curriculum tools
        with st.expander("Learning Tools"):
            for tool in curr.get_additional_tools():
                st.markdown(f"- {tool}")
    
    # Main content area
    st.title("Python Learning Tracker")
    
    # Display different pages based on selection
    if page == "Dashboard":
        show_dashboard()
    elif page == "Day Tracker":
        show_day_tracker()
    elif page == "Weekly View":
        show_weekly_view()
    elif page == "Notes & Reflections":
        show_notes_page()

def show_dashboard():
    """Display the main dashboard with progress visualizations."""
    st.header("Learning Dashboard")
    
    # Top stats in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        completion_percentage = dh.get_completion_percentage()
        st.plotly_chart(viz.create_completion_gauge(completion_percentage), use_container_width=True)
    
    with col2:
        weekly_progress = dh.get_weekly_progress()
        total_by_week = [7, 7, 7]  # 7 days each week
        weekly_completion = [
            f"Week {i+1}: {completed}/{total}" 
            for i, (completed, total) in enumerate(zip(weekly_progress, total_by_week))
        ]
        st.subheader("Weekly Completion")
        for week_stat in weekly_completion:
            st.markdown(f"- {week_stat}")
    
    with col3:
        current_day = utils.get_current_day()
        if current_day <= 21:
            day_info = utils.get_day_info(current_day)
            if day_info:
                st.subheader("Current Topic")
                st.markdown(f"**Day {current_day}: {day_info['topic']}**")
                st.markdown(f"*{day_info['practice']}*")
            else:
                st.subheader("Current Day")
                st.markdown(f"**Day {current_day}**")
                st.markdown("*Topic information not available*")
        else:
            st.subheader("Congratulations!")
            st.markdown("You've completed the 21-day Python curriculum! 🎉")
    
    # Progress heatmap
    st.subheader("Progress Tracker")
    progress_data = dh.get_all_progress_data()
    st.plotly_chart(viz.create_progress_heatmap(progress_data), use_container_width=True)
    
    # Weekly stats
    col1, col2 = st.columns(2)
    
    with col1:
        weekly_progress = dh.get_weekly_progress()
        st.plotly_chart(viz.create_weekly_progress_chart(weekly_progress), use_container_width=True)
    
    with col2:
        weekly_time = dh.get_time_spent_by_week()
        st.plotly_chart(viz.create_weekly_time_chart(weekly_time), use_container_width=True)
    
    # Time spent breakdown
    st.subheader("Time Investment")
    st.plotly_chart(viz.create_time_spent_chart(progress_data), use_container_width=True)
    
    # Calendar view
    st.subheader("Activity Calendar")
    st.plotly_chart(viz.create_streak_calendar(progress_data), use_container_width=True)
    
    # Upcoming days
    st.subheader("Coming Up Next")
    upcoming = utils.get_upcoming_days(current_day)
    
    if upcoming:
        for day in upcoming:
            try:
                with st.expander(f"Day {day['day']}: {day['topic']}"):
                    st.markdown(f"""<div class="day-card">
                    <p><strong>Week {day['week']}:</strong> {day['week_title']}</p>
                    <p><strong>Practice:</strong> {day['practice']}</p>
                    <p><strong>Resources:</strong></p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    resources = day['resources']
                    for resource in resources:
                        if isinstance(resource, dict) and 'url' in resource:
                            st.markdown(f"""<div class="resource-link"><a href="{resource['url']}" target="_blank">{resource['name']} 🔗</a></div>""", unsafe_allow_html=True)
                        else:
                            resource_name = resource['name'] if isinstance(resource, dict) else resource
                            st.markdown(f"- {resource_name}")
            except (KeyError, TypeError):
                # Skip days with missing data
                continue
    else:
        st.info("No upcoming days available")

def show_day_tracker():
    """Display the day tracker to mark completion and log time."""
    st.header("Day Tracker")
    
    # Day selection
    day_number = st.number_input("Select Day:", min_value=1, max_value=21, value=utils.get_current_day())
    
    # Get day info
    day_info = utils.get_day_info(day_number)
    
    if not day_info:
        st.error("Day information not found!")
        return
    
    # Display day details
    st.subheader(f"Day {day_number}: {day_info['topic']}")
    st.markdown(f"**Week {day_info['week']}: {day_info['week_title']}**")
    
    # Display completion status
    try:
        progress_data = dh.get_all_progress_data()
        day_data = progress_data[day_number-1] if day_number <= len(progress_data) else {"completed": False, "time_spent_minutes": 0}
        is_completed = day_data.get('completed', False)
        
        # Columns for layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Practice Exercise")
            st.markdown(f"{day_info['practice']}")
            
            st.markdown("### Resources")
            resources = day_info.get('resources', [])
            resources_used = dh.get_resources_used(day_number)
            
            for resource in resources:
                resource_name = resource['name'] if isinstance(resource, dict) else resource
                resource_key = resource_name  # Use the name as the key for checkbox
                
                # Check if this resource was used
                is_checked = resource_name in resources_used
                
                # Create a row with checkbox and link
                col1, col2 = st.columns([1, 3])
                with col1:
                    if st.checkbox("", value=is_checked, key=f"resource_{day_number}_{resource_key}"):
                        if not is_checked:
                            dh.mark_resource_used(day_number, resource_name)
                    else:
                        if is_checked:
                            # Remove the resource from used resources
                            data = dh.load_data()
                            if str(day_number) in data["resources_used"]:
                                if resource_name in data["resources_used"][str(day_number)]:
                                    data["resources_used"][str(day_number)].remove(resource_name)
                                    dh.save_data(data)
                
                with col2:
                    if isinstance(resource, dict) and 'url' in resource:
                        st.markdown(f"""<div class="resource-link"><a href="{resource['url']}" target="_blank">{resource_name} 🔗</a></div>""", unsafe_allow_html=True)
                    else:
                        st.text(resource_name)
        
        with col2:
            # Completion tracking
            st.markdown("### Progress Tracking")
            completed = st.checkbox("Mark as completed", value=is_completed)
            
            if completed != is_completed:
                dh.mark_day_complete(day_number, completed)
                st.success(f"Day {day_number} marked as {'completed' if completed else 'incomplete'}!")
                st.rerun()
            
            # Time tracking
            st.markdown("### Time Spent")
            
            # Get current time spent in minutes
            time_spent_min = day_data.get('time_spent_minutes', 0)
            hours = time_spent_min // 60
            minutes = time_spent_min % 60
    except Exception as e:
        st.error(f"Error loading progress data: {e}")
        st.info("Using default values instead.")
        is_completed = False
        hours = 0
        minutes = 0
        
        col1, col2 = st.columns(2)
        with col1:
            hours_input = st.number_input("Hours:", min_value=0, value=int(hours), key=f"hours_{day_number}")
        with col2:
            minutes_input = st.number_input("Minutes:", min_value=0, max_value=59, value=int(minutes), key=f"minutes_{day_number}")
        
        if hours_input != hours or minutes_input != minutes:
            dh.update_time_spent(day_number, hours_input, minutes_input)
            st.success(f"Time updated to {hours_input} hours and {minutes_input} minutes!")
            st.rerun()
    
    # Notes section
    st.markdown("### Notes & Reflections")
    current_note = dh.get_note(day_number)
    note = st.text_area("Your notes for this day:", value=current_note, height=200, key=f"note_{day_number}")
    
    if note != current_note:
        dh.save_note(day_number, note)
        st.success("Notes saved successfully!")
    
    # Exercise Upload
    st.markdown("### Upload Exercise Solution")
    uploaded_file = st.file_uploader("Upload your solution (Python file):", type=["py"], key=f"upload_{day_number}")
    
    if uploaded_file:
        # Read and display the content
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        code = stringio.read()
        
        st.code(code, language="python")
        
        # Save the uploaded file information
        data = dh.load_data()
        if "uploads" not in data:
            data["uploads"] = {}
        
        data["uploads"][str(day_number)] = {
            "filename": uploaded_file.name,
            "upload_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        dh.save_data(data)
        st.success(f"Solution for Day {day_number} uploaded successfully!")

def show_weekly_view():
    """Display a view of each week's curriculum."""
    st.header("Weekly Curriculum View")
    
    # Get curriculum data
    curriculum_data = curr.get_curriculum_data()
    
    # Create tabs for each week
    week_tabs = st.tabs([f"Week {week['week']}: {week['title']}" for week in curriculum_data])
    
    # Fill each week's tab
    for i, week_tab in enumerate(week_tabs):
        with week_tab:
            week_data = curriculum_data[i]
            st.subheader(f"Week {week_data['week']}: {week_data['title']}")
            
            # Display each day in the week as an expander
            for day in week_data['days']:
                day_num = day['day']
                # Get completion status
                try:
                    progress_data = dh.get_all_progress_data()
                    if day_num <= len(progress_data):
                        day_progress = progress_data[day_num-1]
                        is_completed = day_progress.get('completed', False)
                        completion_date = day_progress.get('completion_date', None) if is_completed else None
                    else:
                        is_completed = False
                        completion_date = None
                except Exception:
                    is_completed = False
                    completion_date = None
                
                # Create an expander for each day
                status_icon = "✅" if is_completed else "❌"
                with st.expander(f"Day {day_num}: {day['topic']} {status_icon}"):
                    st.markdown(f"**Practice Exercise:** {day['practice']}")
                    
                    # Resources with links
                    st.markdown("**Resources:**")
                    resources = day.get('resources', [])
                    for resource in resources:
                        if isinstance(resource, dict) and 'url' in resource:
                            st.markdown(f"""<div class="resource-link"><a href="{resource['url']}" target="_blank">{resource['name']} 🔗</a></div>""", unsafe_allow_html=True)
                        else:
                            resource_name = resource['name'] if isinstance(resource, dict) else resource
                            st.markdown(f"- {resource_name}")
                    
                    # Show completion status
                    if is_completed:
                        st.success(f"Completed on: {completion_date}")
                    else:
                        st.info("Not completed yet")
                
            # Create a table for the overview
            week_df = []
            for day in week_data['days']:
                day_num = day['day']
                # Get completion status again
                try:
                    progress_data = dh.get_all_progress_data()
                    if day_num <= len(progress_data):
                        day_progress = progress_data[day_num-1]
                        is_completed = day_progress.get('completed', False)
                    else:
                        is_completed = False
                except Exception:
                    is_completed = False
                
                week_df.append({
                    "Day": day_num,
                    "Topic": day['topic'],
                    "Status": "✅ Completed" if is_completed else "❌ Incomplete"
                })
            
            st.subheader("Week Overview")
            st.table(pd.DataFrame(week_df))
            
            # Display progress for this week
            week_progress = dh.get_weekly_progress()[i]
            st.progress(week_progress / 7)
            st.caption(f"Week {i+1} Progress: {week_progress}/7 days completed")

def show_notes_page():
    """Display all notes in one place."""
    st.header("Learning Notes & Reflections")
    
    # Get all data
    data = dh.load_data()
    notes = data.get("notes", {})
    
    if not notes:
        st.info("You haven't added any notes yet. Go to the Day Tracker to add notes for specific days.")
        return
    
    # Sort days by number
    sorted_days = sorted([int(day) for day in notes.keys()])
    
    for day in sorted_days:
        day_info = utils.get_day_info(day)
        if not day_info:
            continue
            
        with st.expander(f"Day {day}: {day_info['topic']}"):
            st.markdown(notes[str(day)])
            st.caption(f"Week {day_info['week']}: {day_info['week_title']}")
    
    # Export option
    if st.button("Export All Notes"):
        notes_text = ""
        for day in sorted_days:
            day_info = utils.get_day_info(day)
            if day_info:
                notes_text += f"# Day {day}: {day_info['topic']}\n"
                notes_text += f"Week {day_info['week']}: {day_info['week_title']}\n\n"
                notes_text += f"{notes[str(day)]}\n\n"
                notes_text += "-" * 50 + "\n\n"
        
        # Create download link
        b64 = base64.b64encode(notes_text.encode()).decode()
        href = f'<a href="data:text/plain;base64,{b64}" download="python_learning_notes.txt">Download Notes</a>'
        st.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
