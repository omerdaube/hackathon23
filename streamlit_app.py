import os
import streamlit as st
import torch
import torchaudio
from transformers import Wav2Vec2ForCTC, Wav2Vec2Tokenizer

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

# Define a function to transcribe a WAV file to text using the Wav2Vec2 model
def transcribe_audio(wav_file):
    # Load the Wav2Vec2 model and tokenizer
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")
    tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-large-960h-lv60-self")
    # Read the contents of the WAV file as a tensor
    waveform, sample_rate = torchaudio.load(wav_file)
    # Resample the waveform if necessary
    if sample_rate != 16000:
        resampler = torchaudio.transforms.Resample(sample_rate, 16000)
        waveform = resampler(waveform)
    # Convert the waveform to a 1D tensor of floats between -1 and 1
    waveform = waveform[0].numpy() / 32768.0
    # Encode the waveform using the Wav2Vec2 tokenizer
    input_values = tokenizer(waveform, return_tensors="pt").input_values
    # Transcribe the encoded waveform using the Wav2Vec2 model
    with torch.no_grad():
        logits = model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = tokenizer.batch_decode(predicted_ids)[0]
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
    # Transcribe the audio file to text using the Wav2Vec2 model when it's uploaded
    if uploaded_wav is not None:
        transcribe_audio(uploaded_wav)

if __name__ == '__main__':
    main()
