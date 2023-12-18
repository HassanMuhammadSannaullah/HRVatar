# # import g4f
# # import requests


# # # project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# # # sys.path.append(project_dir)


# # def askGPT3(query):
# #     if type(query) is str:
# #         response = requests.post(
# #             "https://ipvikas-weask-chatgpt.hf.space/run/predict_1",
# #             json={
# #                 "data": [
# #                     query,
# #                 ]
# #             },
# #         )
# #         print(response)
# #         # data = response["data"]
# #         # return data[0] if data[0] else None
# #     #     resp = g4f.ChatCompletion.create(
# #     #         model="gpt-4",
# #     #         messages=[{"role": "user", "content": f"{query}"}],
# #     #     )
# #     #     response = ""
# #     #     for res in resp:
# #     #         response = response + res
# #     #     return response

# #     # return None

# from gradio_client import Client


# def askGPT3(query):
#     client = Client(
#         # "https://openskyml-pigeon-chat.hf.space/"
#         "https://openskyml-opensky-llm-chatgpt-ui.hf.space/"
#     )
#     result = client.predict(
#         query, api_name="/chat"  # str in 'Message' Textbox component
#     )
#     return result


# if __name__ == "__main__":
#     print(askGPT3("Hello world"))

import requests


def askGPT3(query):
    url = "https://api.cloudflare.com/client/v4/accounts/cbc0d16e16b5cb63d91f6907226a2230/ai/run/@cf/meta/llama-2-7b-chat-int8"

    # Setting up headers and data
    headers = {
        "Authorization": "Bearer 44doE7sfRlo6whMDajL4SGqm_7OO6QVrQuxVyyHP",
        "Content-Type": "application/json",
    }
    data = {
        "messages": [
            {
                "role": "system",
                "content": f"Write a response to the user queries and follow their given tag instructions",
            },
            {
                "role": "user",
                "content": f"{query}",
            },
        ]
    }

    # Making the API request
    response = requests.post(url, headers=headers, json=data)
    if response.json()["success"]:
        # print("\n\nFrom chatgpt:\n")
        print(response.json()["result"]["response"])
        return response.json()["result"]["response"]
    else:
        print("response failed from gpt")
        return None


if __name__ == "__main__":
    print(askGPT3("why dont you give me response"))
