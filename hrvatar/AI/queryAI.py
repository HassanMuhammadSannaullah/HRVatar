# import g4f
# import requests


# # project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # sys.path.append(project_dir)


# def askGPT3(query):
#     if type(query) is str:
#         response = requests.post(
#             "https://ipvikas-weask-chatgpt.hf.space/run/predict_1",
#             json={
#                 "data": [
#                     query,
#                 ]
#             },
#         )
#         print(response)
#         # data = response["data"]
#         # return data[0] if data[0] else None
#     #     resp = g4f.ChatCompletion.create(
#     #         model="gpt-4",
#     #         messages=[{"role": "user", "content": f"{query}"}],
#     #     )
#     #     response = ""
#     #     for res in resp:
#     #         response = response + res
#     #     return response

#     # return None

from gradio_client import Client


def askGPT3(query):
    client = Client("https://openskyml-opensky-llm-chatgpt-ui.hf.space/")
    result = client.predict(
        query, api_name="/chat"  # str in 'Message' Textbox component
    )
    return result


if __name__ == "__main__":
    print(askGPT3("Hello world"))
