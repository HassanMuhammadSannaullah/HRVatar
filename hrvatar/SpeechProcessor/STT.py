# from gradio_client import Client


# def speech_to_text(wav_path):
#     client = Client("https://sanchit-gandhi-whisper-jax.hf.space/")
#     result = client.predict(
#         wav_path,
#         "transcribe",  # str in 'Task' Radio component
#         False,  # bool in 'Return timestamps' Checkbox component
#         api_name="/predict_1",
#     )
#     return result[0]

from . import model


def speech_to_text(wav_path):
    result = model.transcribe(wav_path)
    return result["text"]
