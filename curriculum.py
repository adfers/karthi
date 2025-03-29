"""
Module to handle the Python learning curriculum data.
"""

def get_curriculum_data():
    """Returns a structured representation of the 21-day Python learning curriculum."""
    
    curriculum = [
        {
            "week": 1,
            "title": "Python Basics",
            "days": [
                {
                    "day": 1,
                    "topic": "Variables & Data Types",
                    "resources": ["W3Schools", "Mosh's Video"],
                    "practice": "Write a script to store and print your name, age, and favorite number."
                },
                {
                    "day": 2,
                    "topic": "Operators & Expressions",
                    "resources": ["Programiz", "Corey Schafer's Video"],
                    "practice": "Write a calculator that adds, subtracts, multiplies, and divides two numbers."
                },
                {
                    "day": 3,
                    "topic": "If Statements & Conditions",
                    "resources": ["Real Python", "freeCodeCamp Video"],
                    "practice": "Create a program that checks if a number is positive, negative, or zero."
                },
                {
                    "day": 4,
                    "topic": "Loops (for, while)",
                    "resources": ["W3Schools Loops", "CS Dojo Video"],
                    "practice": "Print numbers from 1-10 using a loop. Print even numbers only."
                },
                {
                    "day": 5,
                    "topic": "Functions",
                    "resources": ["Python Functions (Programiz)", "Mosh's Video"],
                    "practice": "Write a function that takes a number and returns its square."
                },
                {
                    "day": 6,
                    "topic": "Lists & Strings",
                    "resources": ["W3Schools Lists", "Corey Schafer's Video"],
                    "practice": "Reverse a string and find the largest number in a list."
                },
                {
                    "day": 7,
                    "topic": "Mini Project (Basics)",
                    "resources": ["Use Replit to code"],
                    "practice": "Build a basic calculator or a number guessing game."
                }
            ]
        },
        {
            "week": 2,
            "title": "Intermediate Python",
            "days": [
                {
                    "day": 8,
                    "topic": "Dictionaries & Sets",
                    "resources": ["W3Schools Dictionaries", "Corey Schafer Video"],
                    "practice": "Count word frequency in a sentence using a dictionary."
                },
                {
                    "day": 9,
                    "topic": "File Handling",
                    "resources": ["Programiz", "Mosh's Video"],
                    "practice": "Read a file and count how many lines it has."
                },
                {
                    "day": 10,
                    "topic": "Error Handling (try-except)",
                    "resources": ["Real Python", "freeCodeCamp Video"],
                    "practice": "Create a program that handles division by zero errors."
                },
                {
                    "day": 11,
                    "topic": "Modules (math, random)",
                    "resources": ["Python Modules Guide", "Mosh's Video"],
                    "practice": "Generate a random password using random module."
                },
                {
                    "day": 12,
                    "topic": "OOP Basics (Classes & Objects)",
                    "resources": ["Real Python", "Mosh's Video"],
                    "practice": "Create a Car class with attributes like brand and speed."
                },
                {
                    "day": 13,
                    "topic": "APIs & JSON",
                    "resources": ["Requests Library (Real Python)", "Corey Schafer Video"],
                    "practice": "Fetch weather data from an API and display it."
                },
                {
                    "day": 14,
                    "topic": "Mini Project",
                    "resources": ["Use Replit or Jupyter Notebook"],
                    "practice": "Build a To-Do List App or Weather App using API."
                }
            ]
        },
        {
            "week": 3,
            "title": "Advanced & Final Project",
            "days": [
                {
                    "day": 15,
                    "topic": "Recap & Debugging",
                    "resources": ["Use Pythontutor to visualize code execution"],
                    "practice": "Debug old programs and improve efficiency."
                },
                {
                    "day": 16,
                    "topic": "Data Structures (Stacks, Queues)",
                    "resources": ["Real Python"],
                    "practice": "Implement a simple stack and queue in Python."
                },
                {
                    "day": 17,
                    "topic": "Algorithms (Sorting & Searching)",
                    "resources": ["Khan Academy"],
                    "practice": "Implement Bubble Sort and Binary Search."
                },
                {
                    "day": 18,
                    "topic": "Python Libraries (pandas, matplotlib)",
                    "resources": ["Pandas Docs", "Matplotlib Tutorial"],
                    "practice": "Read a CSV file using Pandas and create a basic graph."
                },
                {
                    "day": 19,
                    "topic": "Final Project Brainstorming",
                    "resources": ["Use Google Colab"],
                    "practice": "Plan a final project (Choose from ideas below)."
                },
                {
                    "day": 20,
                    "topic": "Final Project (Day 1)",
                    "resources": ["Use Replit or Jupyter Notebook"],
                    "practice": "Build a project like: Password Manager, Budget Tracker, or Simple Game."
                },
                {
                    "day": 21,
                    "topic": "Final Project (Day 2)",
                    "resources": ["Use Replit or Jupyter Notebook"],
                    "practice": "Complete your final project and showcase it."
                }
            ]
        }
    ]
    
    return curriculum

def get_additional_tools():
    """Returns the list of additional tools recommended for the learning journey."""
    
    tools = [
        "Online Coding Editors: Replit, Jupyter Notebook, Google Colab",
        "Practice & Challenges: HackerRank, LeetCode",
        "Debugging & Visualization: Python Tutor"
    ]
    
    return tools

def get_days_count():
    """Returns the total number of days in the curriculum."""
    return 21

def get_week_count():
    """Returns the total number of weeks in the curriculum."""
    return 3
