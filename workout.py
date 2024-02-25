import streamlit as st
import json
import time

# Define the file path (hardcoded)
file_path = 'exercises.json'

def load_json_data(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {'exercises': []}
    return data

def save_json_data(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def add_exercise(name, category, description):
    data = load_json_data(file_path)
    new_exercise = {
        'name': name,
        'category': category,
        'description': description
    }
    data['exercises'].append(new_exercise)
    save_json_data(file_path, data)

def display_exercise_selection(exercises):
    selected_exercises = []
    for exercise in exercises:
        if st.checkbox(exercise['name']):
            selected_exercises.append(exercise)
    return selected_exercises

def display_workout(selected_exercises):
    for exercise in selected_exercises:
        st.write(f"Performing exercise: {exercise['name']} - {exercise['category']}")
        st.write(f"Description: {exercise['description']}")
        sets = st.slider(f"How many Sets for {exercise['name']}?", 1, 5, 3)
        reps = st.slider(f"How many Reps for {exercise['name']}?", 5, 15, 9)
        if st.button("Start"):
            set_test = st.header(f"Set: 1")
            rep_text = st.subheader(f"Rep: 1")
            for j in range(sets):
                set_test.header(f"Set: {j}")
                for i in range(reps):
                    rep_text.subheader(f"Repetition: {i}")
                    time.sleep(3)  # Sleep for 3 seconds

# Load the JSON data using the function
data = load_json_data(file_path)

# Streamlit app to add exercises
st.sidebar.title('Add Exercise')

name = st.sidebar.text_input('Exercise Name')
category = st.sidebar.selectbox('Category', ['Strength Training', 'Stretching'])
description = st.sidebar.text_area('Description')

if st.sidebar.button('Add Exercise'):
    add_exercise(name, category, description)
    st.sidebar.success('Exercise added successfully!')

# Display the current exercises
st.title('Current Exercises')

if 'exercises' in data:
    exercises = data['exercises']
    categories = set([exercise['category'] for exercise in exercises])

    selected_category = st.selectbox('Select Workout Type', list(categories))
    selected_exercises = [exercise for exercise in exercises if exercise['category'] == selected_category]

    if len(selected_exercises) > 0:
        st.write("Select the exercises you want to include in your workout:")
        selected_exercises = display_exercise_selection(selected_exercises)

        if st.button('Start Workout'):
            st.success('Workout started!')
            display_workout(selected_exercises)
    else:
        st.write('No exercises found in this category.')
else:
    st.write('No exercises found.')
