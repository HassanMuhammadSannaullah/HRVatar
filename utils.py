import mysql.connector
from hrvatar.InterviewProcessor import EvaluateAudio, EvaluateVideo
from gradio_client import Client
from PIL import Image


def get_db_connection():
    # Replace 'username', 'password', 'host', 'port', and 'database_name' with your actual MySQL credentials
    connection = mysql.connector.connect(
        user="root",
        password="hassansana",
        host="localhost",
        port="3306",
        database="HR_VATAR",
    )
    return connection


def job_id_exists(job_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Define the SQL query to check if the job ID exists in the jobs table
        query = "SELECT COUNT(*) FROM jobs WHERE jobid = %s"
        cursor.execute(query, (job_id,))
        result = cursor.fetchone()

        # Check if the count of rows with the given job ID is greater than 0
        if result and result[0] > 0:
            return True
        else:
            return False
    except mysql.connector.Error as error:
        print("Error:", error)
    finally:
        if connection:
            connection.close()


def get_candidateRequirements(job_id):
    try:
        # Establish a database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query the database to get the job description
        query = "SELECT candidaterequirement FROM jobs WHERE jobid = %s"
        cursor.execute(query, (job_id,))

        # Fetch the result
        candidate_requirements = cursor.fetchone()

        if candidate_requirements:
            return candidate_requirements[0]
        else:
            return None
    except Exception as e:
        print(f"Error retrieving from database: {str(e)}")
        return None
    finally:
        # Close the cursor and database connection
        cursor.close()
        connection.close()


# Perform evaludation a seprate thread
def Evaluate(questions, answer_audio_paths, answer_video_paths):
    print("in evaludation functions")
    audio_scores = EvaluateAudio(questions, answer_audio_paths)
    video_scores = EvaluateVideo(answer_video_paths)
    print(video_scores)
    # After processing, you can delete the temporary directory and its contents
    # to clean up the files.
    # for video_path in video_paths:
    #     os.remove(video_path)
    # for audio_path in audio_paths:
    #     os.remove(audio_path)


def process_profile_image(image_path):
    try:
        client = Client("https://alfasign-remove-background-on-image.hf.space/")
        result = client.predict(
            image_path,  # str (filepath or URL to image)in 'image' Image component
            api_name="/predict",
        )
        print(result)
        img = Image.open(result)

        new_image = Image.new("RGB", img.size, "white")

        # Paste the original image onto the new image, using the alpha channel (if present)
        new_image.paste(img, (0, 0), img)

        # Save the result
        new_image.save(result)
        return result
    except:
        return "Error"

account_exist_html = """<html>
                            <head>
                                <title>Account Already Exists</title>
                                <style>
                                    body {
                                        display: flex;
                                        justify-content: center;
                                        align-items: center;
                                        height: 100vh;
                                        margin: 0;
                                        font-family: Arial, sans-serif;
                                    }

                                    .message {
                                        text-align: center;
                                        font-weight: bold;
                                    }
                                </style>
                            </head>
                            <body>
                                <div class="message">
                                    <p>ACCOUNT ALREADY EXISTS. USE ANOTHER EMAIL.</p>
                                </div>
                            </body>
                            </html>"""


# if __name__ == "__main__":
#     print(get_job_description(int(" 15 ".strip())))
# connection = get_db_connection()

# db_connection = get_db_connection()

# email = "scientisthassan@gmail.com"
# cursor = db_connection.cursor()
# query = """
#         SELECT
#             J.JobId,
#             CA.CompanyName,
#             J.JobPosition,
#             J.Description,
#             J.CandidateRequirement
#         FROM
#             Jobs J
#         JOIN
#             CompanyAccounts CA
#         ON
#             J.CompanyId = CA.CompanyId
#         WHERE
#             J.JobPosition LIKE %s
#     """
# cursor.execute(
#     "SELECT profileimage FROM companyaccounts WHERE companyid = %s", (1,)
# )
# candidate_data = cursor.fetchone()
# print(candidate_data[0])

# cursor.close()
# db_connection.close()
