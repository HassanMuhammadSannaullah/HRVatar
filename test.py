# from utils import Evaluate
# import threading


# questions = ["What do you know about webscraping and what tools do you use for it?"]
# audio_paths = ["temp\\tempAudioResponses\\audio_1.wav"]
# video_paths = ["temp\\tempAudioResponses\\video_1.mp4"]
# evaluate_thread = threading.Thread(
#     target=Evaluate,
#     args=(questions, audio_paths, video_paths),
# )
# evaluate_thread.start()
# evaluate_thread.join()


from gradio_client import Client

client = Client("https://nijisakai-gradio-lipsync-wav2lip.hf.space/")
result = client.predict(
    "me.jpg",  # str (filepath or URL to file)
    "temp\\tempwav\\20231003183421.wav",  # str (filepath or URL to file)
    "wav2lip",  # str in 'Checkpoint' Radio component
    0,  # int | float (numeric value between 0 and 50)
    0,  # int | float (numeric value between 0 and 50)
    0,  # int | float (numeric value between 0 and 50)
    0,  # int | float (numeric value between 0 and 50)
    1,  # int | float (numeric value between 1 and 4)
    fn_index=0,
)
print(result)
