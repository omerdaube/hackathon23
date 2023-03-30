import os
import streamlit as st
import numpy as np
import soundfile as sf
import requests

# Define a function to read the uploaded file and display checkboxes for each line
def process_file(uploaded_file):
    if uploaded_file is not None:
        # Read the contents of the file as a string
        contents = uploaded_file.getvalue().decode('utf-8')
        # Split the contents into lines
        lines = contents.split('\n')
        # Display a checkbox for each line, marking the ones with "YES" after the comma
        for line in lines:
            if "," in line:
                parts = line.split(",")
                if len(parts) == 2 and parts[1].strip() == "YES":
                    checkbox_value = st.checkbox(parts[0].strip(), value=True)
                else:
                    checkbox_value = st.checkbox(parts[0].strip(), value=False)
            else:
                checkbox_value = st.checkbox(line, value=False)

# Define a function to transcribe a WAV file to text using the Whisper API
def transcribe_audio(wav_file):
    # Set the API endpoint and access token
    endpoint = "https://api.openai.com/v1/speeches/transcribe"
    access_token = "<YOUR ACCESS TOKEN HERE>"
    # Read the contents of the WAV file as a binary string
    audio_data = wav_file.getvalue()
    # Set the API headers and parameters
    headers = {"Content-Type": "audio/wav", "Authorization": f"Bearer {access_token}"}
    params = {"engine": "whisper"}
    # Send a POST request to the API endpoint with the audio data and parameters
    response = requests.post(endpoint, headers=headers, params=params, data=audio_data)
    # Parse the API response to get the transcribed text
    transcription = response.json()["text"]
    # Display the transcribed text in the app
    st.write(f"Transcribed text: {transcription}")

# Create the Streamlit app
def main():
    st.title("File Uploader and Checkbox Demo")
    # Add a file uploader for text files
    uploaded_file = st.file_uploader("Choose a text file")
    # Call the process_file function when the text file is uploaded
    process_file(uploaded_file)
    # Add a file uploader for audio files
    uploaded_wav = st.file_uploader("Choose a WAV audio file", type=["wav"])
    # Transcribe the audio file to text using the Whisper API when it's uploaded
    if uploaded_wav is not None:
        transcribe_audio(uploaded_wav)

if __name__ == '__main__':
    main()
