import streamlit as st
import json
import time
import pygame
import os
from gtts import gTTS

# Define the file path (hardcoded)
file_path = 'exercises.json'
def shout(number):
    pygame.init()
    tts = gTTS(text=str(number), lang='en', slow=False)
    tts.save(f"sounds/{number}.mp3")
    pygame.mixer.music.load(f"sounds/{number}.mp3")
    pygame.mixer.music.play()


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

def start_workout(set_text, rep_text, sets, reps, col2):
    # c = st.container()
    for j in range(1, sets+1):
        shout(f"Set {j}")
        time.sleep(15)
        set_text.text(f"Set: {j}")
        for i in range(1, reps+1):
            rep_text.text(f"Repetition: {i}")
            shout(f"Rep {i}")
            time.sleep(5)  # Sleep for 3 seconds

def display_workout(selected_exercises,sets,reps, col2):
    if sets is not 0 and reps is not 0:
        for exercise in selected_exercises:
            shout(f"Starting Excercise {exercise['name']}")
            time.sleep(2)
            col2.subheader(f"Excercise: {exercise['name']}")
            col2.write(f"Description: {exercise['description']}")
            set_text = col2.text(f"Set: 1")
            rep_text = col2.text(f"Rep: 1")
            start_workout(set_text, rep_text, sets, reps, col2)

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

col1, col2 = st.columns(2)
# Display the current exercises
col1.title('Current Exercises')

if 'exercises' in data:
    exercises = data['exercises']
    categories = set([exercise['category'] for exercise in exercises])

    selected_category = col1.selectbox('Select Workout Type', list(categories))
    selected_exercises = [exercise for exercise in exercises if exercise['category'] == selected_category]

    if len(selected_exercises) > 0:
        col1.write("Select the exercises you want to include in your workout:")
        selected_exercises = display_exercise_selection(selected_exercises)
        sets = int(col1.number_input("Sets?", value=0, placeholder="Type a number..."))
        reps = int(col1.number_input("Reps?", value=0, placeholder="Type a number..."))
        if col1.button('Start Workout'):
            col1.success('Workout started!')
            display_workout(selected_exercises,sets,reps, col2)
    else:
        col1.write('No exercises found in this category.')
else:
    col1.write('No exercises found.')
