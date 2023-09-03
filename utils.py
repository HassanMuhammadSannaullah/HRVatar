import mysql.connector


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


def get_job_description(job_id):
    try:
        # Establish a database connection
        connection = get_db_connection()
        cursor = connection.cursor()

        # Query the database to get the job description
        query = "SELECT description FROM jobs WHERE jobid = %s"
        cursor.execute(query, (job_id,))

        # Fetch the result
        job_description = cursor.fetchone()

        if job_description:
            return job_description[0]
        else:
            return None
    except Exception as e:
        print(f"Error retrieving from database: {str(e)}")
        return None
    finally:
        # Close the cursor and database connection
        cursor.close()
        connection.close()


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


if __name__ == "__main__":
    print(get_job_description(int(" 15 ".strip())))
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
