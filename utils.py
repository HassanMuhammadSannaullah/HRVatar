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
    connection = get_db_connection()

    db_connection = get_db_connection()
    
    email = "scientisthassan@gmail.com"
    cursor = db_connection.cursor()
    cursor.execute("SELECT JobPosition, Description, CandidateRequirement, PostedOnLinkedIn, StillHiring FROM jobs")
    candidates = cursor.fetchone()
    print(type(candidates[3]))
    
    cursor.close()
    db_connection.close()