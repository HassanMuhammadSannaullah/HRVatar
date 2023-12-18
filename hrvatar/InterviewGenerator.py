from hrvatar.SpeechProcessor.TTS import text_to_speech
from hrvatar.wav2lip.Wav2Lip import Processor
from hrvatar.AI.queryAI import askGPT3
import re
import time
import os


def _generateQuestions(description, QuestionCount):
    print("Starting to generate Interview Questions")
    query = f"""Generate {QuestionCount} interview questions to ask a candidate for the following job:
        {description}

        Write <question> in start of each question in your response and </question> in end
        """
    text = askGPT3(query)
    questions = re.findall(r"<question>(.*?)</question>", text)
    print("Completed Interview Question sGeneration")
    return questions


def generateInterview(job_description, QuestionCount, image_path, voice_gender="male"):
    questions = _generateQuestions(job_description, QuestionCount)

    questions_speech_path = []
    print("Generating Speech of Interview Questions")
    for question in questions:
        print(question)
        questions_speech_path.append(text_to_speech(question, voice_gender))
        time.sleep(1)
    print("Generating Speech of Interview Questions completed")

    interview_vid_paths = []
    print("Generatring Videos of lip sync")
    for wav_path in questions_speech_path:
        processor = Processor()
        interview_vid_paths.append(processor.run(image_path, wav_path))
        os.remove(wav_path)
    print("Generating video of lip sync complete")

    return questions, interview_vid_paths


# if __name__ == "__main__":
#     print(_generateQuestions("A brilliant python developer", 2))
