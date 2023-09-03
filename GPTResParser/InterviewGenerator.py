from GPTResParser.text_to_speech.TTS import text_to_speech
from GPTResParser.wav2lip.Wav2Lip import Processor
from GPTResParser.AI.queryAI import askGPT3
import re
import time
import os


def _generateQuestions(description, QuestionCount):
    query = f"""Generate {QuestionCount} interview questions to ask a candidate for the following job:
        {description}

        Write each question in <question></question> tags
        """
    text = askGPT3(query)
    questions = re.findall(r"<question>(.*?)</question>", text)
    return questions


def generateInterview(job_description, QuestionCount, image_path, voice_gender="male"):
    questions = _generateQuestions(job_description, QuestionCount)

    questions_speech_path = []
    for question in questions:
        questions_speech_path.append(text_to_speech(question, voice_gender))
        time.sleep(1)

    interview_vid_paths = []
    for wav_path in questions_speech_path:
        processor = Processor()
        interview_vid_paths.append(processor.run(image_path, wav_path))
        os.remove(wav_path)

    return interview_vid_paths


# if __name__ == "__main__":
#     print(_generateQuestions("A brilliant python developer", 2))
