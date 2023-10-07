from GPTResParser.AI.queryAI import askGPT3
from GPTResParser.SpeechProcessor.STT import speech_to_text
import re


def GPTRateAnswers(questions, answers):
    output = []
    for question, answer in zip(questions, answers):
        query = f"""
             for the following question \n {question}
                and the following answer from the candidate \n{answer}

                rate the answer from 1 to 10. give answer in <score></score> tag
                
                You must always rate the answer, even if it is irrelevant. if answer is irrelevant rate 0
                
                0 is worst and 10 is best"""
        result = askGPT3(query)
        score = re.findall(r"<score>(.*?)</score>", result)
        output.append(score[0])
    return output


def EvaluateAudio(questions, answer_audio_paths):
    scores = []
    answers_text = []
    # convert audos to text
    for audio in answer_audio_paths:
        answers_text.append(speech_to_text(audio))
    print(answers_text)
    GPT_Scores = GPTRateAnswers(questions, answers_text)
    scores = GPT_Scores
    return scores
