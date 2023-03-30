import os
import streamlit as st
from google.cloud import speech_v1p1beta1 as speech

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

# Define a function to transcribe a WAV file to text using the Google Cloud Speech-to-Text API
def transcribe_audio(wav_file):
    # Create a client object for the Speech-to-Text API
    client = speech.SpeechClient()
    # Read the contents of the WAV file as bytes
    audio_content = wav_file.read()
    # Configure the recognition settings for the Speech-to-Text API
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    # Create a recognition audio object from the WAV file contents
    audio = speech.RecognitionAudio(content=audio_content)
    # Call the Speech-to-Text API to transcribe the audio
    response = client.recognize(request={"config": config, "audio": audio})
    # Extract the transcribed text from the response
    transcript = response.results[0].alternatives[0].transcript
    # Display the transcribed text in the app
    st.write(f"Transcribed text: {transcript}")

# Create the Streamlit app
def main():
    st.title("File Uploader and Checkbox Demo")
    # Add a file uploader for text files
    uploaded_file = st.file_uploader("Choose a text file")
    # Call the process_file function when the text file is uploaded
    process_file(uploaded_file)
    # Add a file uploader for audio files
    uploaded_wav = st.file_uploader("Choose a WAV audio file", type=["wav"])
    # Transcribe the audio file to text when it's uploaded
    if uploaded_wav is not None:
        transcribe_audio(uploaded_wav)

if __name__ == '__main__':
    main()
