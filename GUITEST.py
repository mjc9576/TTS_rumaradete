import tkinter as tk
from tkinter import StringVar
import os
import json  # For reading JSON
from pydub import AudioSegment
import pygame  # For audio playback
import tempfile  # For temporary file handling

# Initialize pygame mixer
pygame.mixer.init()

# Load options from an external JSON file
def load_voice_options(json_file):
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading JSON file: {e}")
    else:
        print(f"JSON file {json_file} not found. Using default options.")
        return {}

# Filepath to the JSON file
voice_json_file = "VOICE/voices.json"

# Load options from the JSON file
options = load_voice_options(voice_json_file)
if not options:
    # Fallback to default options if JSON loading fails
    options = {"Michael": "VOICE/Michael", "Ava": "VOICE/Ava", "Michael(pause-less)": "VOICE/MICHAEL_DELAYLESS"}

# Function to combine MP3s
def combine_mp3s(input_string, path_string):
    fallback_path = "VOICE/EXTRA"  # Define the fallback directory
    combined_audio = AudioSegment.empty()
    
    for char in input_string:
        file_name = f"{char}.mp3"
        file_path = os.path.join(path_string, file_name)
        
        
        if os.path.exists(file_path):  # Check if the file exists in the resolved path
            try:
                audio = AudioSegment.from_file(file_path)
                combined_audio += audio
            except Exception as e:
                print(f"Error loading {file_name}: {e}")
        else:
            print(f"Warning: File {file_name} not found in both {path_string} and fallback path. Skipping.")
    
    if len(combined_audio) == 0:
        print("Error: No valid audio files were found to combine.")
        return None
    
    return combined_audio



# Function to play audio using a temporary file
def play_audio_temp(input_string, path_string):
    combined_audio = combine_mp3s(input_string, path_string)
    if combined_audio is None:
        return
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        temp_file_name = temp_file.name
        temp_file.close()
        combined_audio.export(temp_file_name, format="mp3")
        print(f"Combined audio exported to temporary file: {temp_file_name}")
        pygame.mixer.music.load(temp_file_name)
        pygame.mixer.music.play()
        print("Playing audio...")
        while pygame.mixer.music.get_busy():
            continue
        os.remove(temp_file_name)
        print(f"Temporary file deleted: {temp_file_name}")
    except Exception as e:
        print(f"Error handling temporary audio file: {e}")

# Function to save audio as a permanent file
def save_audio_legacy(input_string, path_string):
    combined_audio = combine_mp3s(input_string, path_string)
    if combined_audio is None:
        return
    try:
        output_file_name = f"{input_string}.mp3"
        combined_audio.export(output_file_name, format="mp3")
        print(f"Combined audio exported as {output_file_name}")
    except Exception as e:
        print(f"Error exporting combined audio: {e}")

# Create the main application window
root = tk.Tk()
root.title("ᓗᔕcᘓധ vocalizer")

# Create and place a text box
text_box = tk.Text(root, height=5, width=40)
text_box.pack(pady=10)

# Add a label for the dropdown menu
dropdown_label = tk.Label(root, text="Voice:")
dropdown_label.pack()

# Create a variable for the dropdown menu
dropdown_var = StringVar(root)
default_option = list(options.keys())[0] if options else "Michael"
dropdown_var.set(default_option)

# Create and place the dropdown menu
dropdown_menu = tk.OptionMenu(root, dropdown_var, *options.keys())
dropdown_menu.pack(pady=10)

# Function for the new button
def new_submit():
    text_content = text_box.get("1.0", tk.END).strip()
    dropdown_selection = dropdown_var.get()
    voice_path = options.get(dropdown_selection, "")
    print(f"New Submit - Text: {text_content}, Voice Path: {voice_path}")
    play_audio_temp(text_content, voice_path)

# Function for the legacy button
def legacy_submit():
    text_content = text_box.get("1.0", tk.END).strip()
    dropdown_selection = dropdown_var.get()
    voice_path = options.get(dropdown_selection, "")
    print(f"Legacy Submit - Text: {text_content}, Voice Path: {voice_path}")
    save_audio_legacy(text_content, voice_path)

# Add the new button to trigger the new functionality
new_button = tk.Button(root, text="Play", command=new_submit)
new_button.pack(pady=10)

# Add the legacy button to trigger the old functionality
legacy_button = tk.Button(root, text="Download", command=legacy_submit)
legacy_button.pack(pady=10)

# Run the application
root.mainloop()