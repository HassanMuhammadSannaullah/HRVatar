import os
import pyttsx3
from datetime import datetime


def text_to_speech(text, voice_gender="female"):
    engine = pyttsx3.init()

    # Define the voice IDs for David (male) and Zira (female)
    david_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
    zira_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

    # Set the voice based on the gender parameter
    if voice_gender.lower() == "male":
        engine.setProperty("voice", david_voice_id)
    elif voice_gender.lower() == "female":
        engine.setProperty("voice", zira_voice_id)
    else:
        print("Invalid gender parameter. Using the default voice.")

    engine.setProperty("rate", 160)

    # Create a directory named "temp" in the current location if it doesn't exist
    temp_dir = os.path.join("temp", "tempwav")
    # Generate a unique filename using the current datetime
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    temp_filename = f"{timestamp}.wav"

    # Build the full path to the temporary audio file
    temp_path = os.path.join(temp_dir, temp_filename)

    # Save the audio to the file
    engine.save_to_file(text, temp_path)
    engine.runAndWait()

    return temp_path


if __name__ == "__main__":
    text = "This is an example with a male voice."
    save_path = "output/male_voice.wav"
    text_to_speech(text, save_path, voice_gender="male")

    text = "This is an example with a female voice."
    save_path = "output/female_voice.wav"
    text_to_speech(text, save_path, voice_gender="female")
