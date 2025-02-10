import streamlit as st
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment variable or Streamlit secrets
ELEVENLABS_API_KEY = "sk_1dcdbd4432f66ad33a606f02574996f1e67c7b84d63eeecb"

# Supported languages (you can expand this list)
LANGUAGES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Hindi": "hi"
}

def get_available_voices():
    """Fetch available voices from ElevenLabs API"""
    url = "https://api.elevenlabs.io/v1/voices"
    
    headers = {
        "Accept": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()['voices']
        else:
            st.error(f"Error fetching voices: {response.status_code}")
            return []
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return []

def generate_speech(text, voice_id, model_id="eleven_monolingual_v1"):
    """Generate speech from text using ElevenLabs API"""
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    data = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            return response.content
        else:
            st.error(f"Error: {response.status_code}")
            st.error(response.text)
            return None
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def main():
    st.title("ElevenLabs Text-to-Speech")
    
    # Sidebar
    st.sidebar.header("Settings")

    # Language selection
    selected_language = st.sidebar.selectbox("Select Language", options=list(LANGUAGES.keys()))

    # Get available voices
    voices = get_available_voices()
    voice_options = {voice['name']: voice['voice_id'] for voice in voices}
    
    # Voice selection
    selected_voice_name = st.sidebar.selectbox(
        "Select Voice",
        options=list(voice_options.keys())
    )
    
    # Text input
    text_input = st.text_area(
        f"Enter text in {selected_language}:",
        height=150
    )
    
    # Generate button
    if st.button("Generate Speech"):
        if text_input.strip():
            with st.spinner("Generating speech..."):
                voice_id = voice_options[selected_voice_name]
                audio_content = generate_speech(text_input, voice_id)
                
                if audio_content:
                    st.audio(audio_content, format='audio/mp3')
                    
                    # Add download button
                    st.download_button(
                        label="Download audio",
                        data=audio_content,
                        file_name="generated_speech.mp3",
                        mime="audio/mp3"
                    )
        else:
            st.warning("Please enter some text to convert to speech.")

if __name__ == "__main__":
    main()
