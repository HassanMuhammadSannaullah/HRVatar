from hrvatar.AI.queryAI import askGPT3
from hrvatar.AI.EvaluateInterviewVideo import process_frames
from hrvatar.SpeechProcessor.STT import speech_to_text
import re
import os


def GPTRateAnswers(questions, answers):
    output = []
    for question, answer in zip(questions, answers):
        query = f"""
             for the following question \n {question}
                and the following answer from the candidate \n{answer}

                rate the answer from 1 to 10. write <score> in start of rating and </score> in end.
                
                You must always rate the answer, even if it is irrelevant. if answer is irrelevant rate 0
                
                0 is worst and 10 is best"""
        result = askGPT3(query)
        print("GPT ratings : ", result)
        score = re.findall(r"<score>(.*?)</score>", result)

        if score:  # Check if score is not empty
            output.append(score[0])
        else:
            output.append(0)
    return output


def EvaluateAudio(questions, answer_audio_paths):
    scores = []
    answers_text = []
    # convert audos to text
    for audio in answer_audio_paths:
        answers_text.append(speech_to_text(audio))
    print(answers_text)
    GPT_Scores = GPTRateAnswers(questions, answers_text)
    scores = GPT_Scores  # implement video and audio modekls to get confidence score and then return the total sum
    return scores


def EvaluateVideo(video_paths):
    model_path = os.path.join("resources", "models", "conf_unconf.h5")
    cv_classifier = os.path.join(
        "resources", "models", "haarcascade_frontalface_default.xml"
    )
    video_scores = []
    for video_path in video_paths:
        temp_score = 0
        result_first, result_mid = process_frames(video_path, model_path, cv_classifier)
        if result_first == 1:
            temp_score += 2
        if result_mid == 1:
            temp_score += 2

        video_scores.append(temp_score)
    return video_scores
