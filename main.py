from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
)
from utils import (
    get_db_connection,
    account_exist_html,
    get_candidateRequirements,
    job_id_exists,
    Evaluate,
)
import base64
import os
from GPTResParser.InterviewGenerator import generateInterview
from GPTResParser.InterviewProcessor import EvaluateAudio
from GPTResParser.ResumeParser import Parse
from GPTResParser.JobPoster import PostJob
import threading
from werkzeug.utils import secure_filename
import pydub
import traceback

app = Flask(__name__)
app.static_folder = "static"
app.secret_key = "your_secret_key_here"
app.static_url_path = "/static"
UPLOAD_FOLDER = os.getcwd()  # Use the current working directory
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def mainPage():
    return render_template("mainPage.html")


@app.route("/company/signup")
def CompanySignUp():
    return render_template("CompanySignUp.html")


@app.route("/candidate/signup")
def CandidateSignUp():
    return render_template("CandidateSignUp.html")


@app.route("/process_signup", methods=["GET", "POST"])
def ProcessSignUp():
    if request.method == "POST":
        signup_type = request.form["signup_type"]
        if signup_type == "candidate":
            # Fetch Data from Form
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            password = request.form["password"]

            # Fetach Data from Database
            db = get_db_connection()
            cursor = db.cursor()
            fetch = cursor.execute(
                f"SELECT COUNT(*) AS email_count FROM candidateaccounts WHERE email = '{email}';"
            )
            fetch = cursor.fetchall()

            if fetch[0][0] == 0:
                query = "INSERT INTO candidateaccounts (FirstName, LastName, Email, Password) VALUES (%s, %s, %s, %s);"
                values = (first_name, last_name, email, password)
                cursor.execute(query, values)
                db.commit()
                db.close()
                return redirect(url_for("CandidateDashboard"))
            else:
                return account_exist_html

        elif signup_type == "company":
            company_name = request.form["company_name"]
            email = request.form["email"]
            password = request.form["password"]
            hrName = request.form["hr_full_name"]

            # Fetach Data from Database
            db = get_db_connection()
            cursor = db.cursor()
            fetch = cursor.execute(
                f"SELECT COUNT(*) AS email_count FROM companyaccounts WHERE Email = '{email}';"
            )
            fetch = cursor.fetchall()

            if fetch[0][0] == 0:
                query = "INSERT INTO companyaccounts (HRName, CompanyName, Email, Password) VALUES (%s, %s, %s, %s);"
                values = (hrName, company_name, email, password)
                cursor.execute(query, values)
                db.commit()
                db.close()
                if validateLogin("company", email, password):
                    return redirect(url_for("CompanyDashboard"))
                else:
                    return "Could Not Create Account Try Later Please"
            else:
                return account_exist_html

        else:
            return "Invalid signup type"

    else:
        return "BAD REQUEST"


@app.route("/login")
def login():
    return render_template("login.html")


def validateLogin(loginType, username, password):
    db = get_db_connection()
    cursor = db.cursor()

    if loginType == "candidate":
        cursor.execute("SELECT * FROM CandidateAccounts WHERE Email = %s", (username,))
        result = cursor.fetchone()
        if result and result[-2] == password:
            session["logged_in"] = True
            session["userdata"] = {
                "FirstName": result[1],
                "LastName": result[2],
                "email": result[3],
            }
            session["login_type"] = "candidate"
            session["CandidateID"] = result[0]
            db.close()
            return True
    elif loginType == "company":
        cursor.execute("SELECT * FROM CompanyAccounts WHERE Email = %s", (username,))
        result = cursor.fetchone()
        if result and result[-2] == password:
            session["logged_in"] = True
            session["userdata"] = {
                "HRName": result[1],
                "CompanyName": result[2],
                "email": result[3],
            }
            session["login_type"] = "company"
            session["CompanyID"] = result[0]
            db.close()
            return True

    db.close()
    return False


@app.route("/process_login")
def process_login():
    username = request.args.get("username")
    password = request.args.get("password")
    login_type = request.args.get("login_type")

    if validateLogin(login_type, username, password):
        if login_type == "company":
            return redirect(url_for("CompanyDashboard"))
        else:
            return redirect(url_for("CandidateDashboard"))
    else:
        flash("Invalid credentials or login type", "error")
        return redirect(url_for("login"))


######################################## COMPANY DASHBOARD ##################################################################


@app.route("/company/dashboard")
def CompanyDashboard():
    if (
        "logged_in" in session
        and session["logged_in"] == True
        and session["login_type"] == "company"
    ):
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT profileimage FROM companyaccounts WHERE companyid = %s",
            (session["CompanyID"],),
        )

        company_data = cursor.fetchone()

        if company_data and company_data[0]:
            # Assuming 'profile_image' is a BLOB (binary) column in your database
            image_binary = company_data[0]
            image_base64 = base64.b64encode(image_binary).decode("utf-8")
            image_url = f"data:image/jpeg;base64,{image_base64}"  # Assuming the image is in JPEG format; adjust if needed
        else:
            image_url = "/static/images/avatar.png"  # Default image URL

        connection.close()
        cursor.close()
        return render_template(
            "CompanyDashboard.html",
            name=session["userdata"]["HRName"],
            image_url=image_url,
        )

    else:
        flash("Please Login First", "info")
        return redirect(url_for("login"))


@app.route("/company/dashboard/add_job", methods=["POST"])
def add_job():
    try:
        if (
            "logged_in" in session
            and session["logged_in"] == True
            and session["login_type"] == "company"
        ):
            # Get the form data from the POST request
            # company_name = request.form.get('companyName')
            data = request.json  # Retrieve the JSON data from the request

            # Extract the form fields from the JSON data
            job_name = data.get("jobName")
            job_description = data.get("jobDescription")
            candidate_info = data.get("candidateInfo")

            # Connect to the database
            connection = get_db_connection()
            cursor = connection.cursor()

            # Insert the job data into the 'jobs' table
            sql_query = "INSERT INTO jobs (CompanyID, JobPosition, Description, CandidateRequirement) VALUES (%s, %s, %s, %s)"
            cursor.execute(
                sql_query,
                (session["CompanyID"], job_name, job_description, candidate_info),
            )

            # Commit the changes a
            connection.commit()

            # get the job id
            # Check if the record exists in the database
            sql_query = "SELECT JobID FROM jobs WHERE CompanyID = %s AND JobPosition = %s AND Description = %s AND CandidateRequirement = %s"
            cursor.execute(
                sql_query,
                (session["CompanyID"], job_name, job_description, candidate_info),
            )

            # Fetch the matching ID if it exists
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            job_id = None
            job_apply_link = ""
            if result:
                job_id = result[0]
                job_apply_link = f"127.0.0.1:5000/candidate/{job_id}/upload_resume"
                print(job_apply_link)

            # Post Job on Job Board
            job_description = f"{job_apply_link}\n" + job_description
            job_link = PostJob(job_name, candidate_info, job_description, "Pakistan")

            response_data = {
                "message": "Job posted successfully!",
                "job_link": job_link,
            }

            return (
                jsonify(response_data),
                200,
            )
        else:
            return "401: Unauthorised Access Denied"

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Posting failed."}), 500


@app.route("/company/dashboard/get_jobs_data", methods=["POST"])
def get_jobs_data():
    try:
        if (
            "logged_in" in session
            and session["logged_in"] == True
            and session["login_type"] == "company"
        ):
            # Connect to the database
            connection = get_db_connection()
            cursor = connection.cursor()

            # Query to fetch all jobs from the 'jobs' table
            sql_query = "SELECT JobPosition, Description, CandidateRequirement, PostedOnLinkedIn, StillHiring FROM jobs where CompanyID= %s"
            cursor.execute(sql_query, (session["CompanyID"],))

            # Fetch all job records from the query result
            jobs_data = cursor.fetchall()

            # Convert the fetched data to a list of dictionaries
            jobs_list = []
            for job in jobs_data:
                job_dict = {
                    "JobPosition": job[0],
                    "Description": job[1],
                    "CandidateMustHave": job[2],
                    "PostedOnLinkedIn": job[3],
                    "StillHiring": job[4],
                }
                jobs_list.append(job_dict)

            # Close the cursor and the connection
            cursor.close()
            connection.close()

            # Return the jobs list as a JSON response
            return jsonify({"jobs": jobs_list}), 200
        else:
            return "401: Unauthorised Access Denied"

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Failed to fetch jobs data."}), 500


@app.route("/company/upload_profile_image", methods=["POST"])
def upload_profile_image_company():
    try:
        file = request.files["image"]
        if file:
            # Process and save the image to the database
            connection = get_db_connection()
            cursor = connection.cursor()

            candidate_id = 1  # Change this to the candidate's actual ID
            image_data = file.read()  # Read the image binary data

            # Insert or update the image in the database
            cursor.execute(
                "UPDATE companyaccounts SET profileimage = %s WHERE companyid = %s",
                (image_data, session["CompanyID"]),
            )
            connection.commit()
            connection.close()
            cursor.close()

            image_url = (
                f"data:image/jpeg;base64,{base64.b64encode(image_data).decode('utf-8')}"
            )
            return jsonify({"success": True, "image_url": image_url})

        return jsonify({"success": False, "error": "No file uploaded."})
    except Exception as e:
        print("Image upload error:", str(e))
        return jsonify({"success": False, "error": "Image upload failed."})


##############################################  CANDIDATE DASHBOARD #######################################################


@app.route("/candidate/dashboard")
def CandidateDashboard():
    if "redirect_interview" in session:
        redirect_url = session["redirect_interview"]
        session.pop("redirect_interview")
        session["resume_passed"] = True
        return redirect(redirect_url)

    if (
        "logged_in" in session
        and session["logged_in"] == True
        and session["login_type"] == "candidate"
    ):
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT profileimage FROM candidateaccounts WHERE candidateid = %s",
            (session["CandidateID"],),
        )

        candidate_data = cursor.fetchone()
        connection.close()

        if candidate_data and candidate_data[0]:
            # Assuming 'profile_image' is a BLOB (binary) column in your database
            image_binary = candidate_data[0]
            image_base64 = base64.b64encode(image_binary).decode("utf-8")
            image_url = f"data:image/jpeg;base64,{image_base64}"  # Assuming the image is in JPEG format; adjust if needed
        else:
            image_url = "/static/images/avatar.png"  # Default image URL

        connection.close()
        cursor.close()

        return render_template(
            "CandidateDashboard.html",
            name=session["userdata"]["FirstName"],
            image_url=image_url,
        )
    else:
        flash("Please Login First", "info")
        return redirect(url_for("login"))


@app.route("/candidate/upload_profile_image", methods=["POST"])
def upload_profile_image_candidate():
    try:
        file = request.files["image"]
        if file:
            # Process and save the image to the database
            connection = get_db_connection()
            cursor = connection.cursor()

            candidate_id = 1  # Change this to the candidate's actual ID
            image_data = file.read()  # Read the image binary data

            # Insert or update the image in the database
            cursor.execute(
                "UPDATE candidateaccounts SET profileimage = %s WHERE candidateid = %s",
                (image_data, session["CandidateID"]),
            )
            connection.commit()
            connection.close()
            cursor.close()

            image_url = (
                f"data:image/jpeg;base64,{base64.b64encode(image_data).decode('utf-8')}"
            )
            return jsonify({"success": True, "image_url": image_url})

        return jsonify({"success": False, "error": "No file uploaded."})
    except Exception as e:
        print("Image upload error:", str(e))
        return jsonify({"success": False, "error": "Image upload failed."})


##################################################### RESUME HANDLING ##########################################################


@app.route("/candidate/<int:job_id>/upload_resume")
def UploadResume(job_id):
    if not job_id_exists(job_id):
        return "The JOB does Not Exist"
    return render_template("UploadResume.html", JobID=job_id)


@app.route("/candidate/process_resume", methods=["POST"])
def ProcessResume():
    try:
        uploaded_file = request.files["file"]
        job_id = request.form["job_id"]
        job_id = int(job_id.strip())
        print(uploaded_file.filename)
        if not uploaded_file:
            response = {"message": "No file uploaded"}
            return jsonify(response), 400

        # Define the directory to save the resumes
        resume_dir = os.path.join("temp", "resumes")
        os.makedirs(resume_dir, exist_ok=True)

        # Create a temporary file path
        temp_file_path = os.path.join(resume_dir, uploaded_file.filename)

        # Save the uploaded file to the specified location
        uploaded_file.save(temp_file_path)

        # Instantiate the Parse class with the temporary file path
        parser = Parse(temp_file_path)

        if parser.resume_txt:
            job_requirements = get_candidateRequirements(job_id)

            applicable, reason = parser.check_applicable_for_job(job_requirements)
            print(applicable, reason)
            if applicable.strip().lower() == "yes":
                print(f"Job Id {job_id}")
                # Delete the temporary file after processing
                session["resume_passed"] = True
                os.remove(temp_file_path)
                response = {"message": "File uploaded and processed successfully"}
                return jsonify(response), 200
            else:
                response = {"message": "Did Not meet requirements"}
                session["resume_passed"] = False
                os.remove(temp_file_path)
                return jsonify(response), 500
        else:
            response = {"message": "Failed to process the uploaded file"}

            # Delete the temporary file if processing fails
            os.remove(temp_file_path)

            return jsonify(response), 500
    except Exception as e:
        # Handle any errors that occur during file upload or processing.
        response = {"message": "Failed to upload"}
        print(str(e))
        return jsonify(response), 500


####################################################### INTERVIEW  ############################################################


@app.route("/candidate/<int:JobID>/interview")
def interview(JobID):
    if "resume_passed" in session and session["resume_passed"]:
        session.pop("resume_passed")
        if not job_id_exists(JobID):
            return "The JOB does Not Exist"

        if (
            "logged_in" in session
            and session["logged_in"] == True
            and session["login_type"] == "candidate"
        ):
            image_static_url = "/static/images/avatar.png"
            return render_template("InterviewPage.html", image_url=image_static_url)
        else:
            flash("Please Login/SignUp First to Give Your Interview")
            print(request.url)
            session["redirect_interview"] = request.url
            return redirect(url_for("login"))
    else:
        return "401 Unauthorized Accesss"


@app.route("/candidate/GetInterviewVideos", methods=["POST"])
def getVideos():
    data = request.json
    jobID = data.get("JobID")

    # database tasks
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch the companyid from the jobs table where jobid matches
    cursor.execute(
        "SELECT companyid, description FROM jobs WHERE jobid = %s",
        (jobID,),
    )
    result = cursor.fetchone()

    if result is None:
        return jsonify({"Database error": "Could not find record for this jobid"}), 500

    company_id = result[0]
    job_description = result[1]

    # Fetch the profileimage from the candidateaccounts table where companyid matches
    cursor.execute(
        "SELECT profileimage FROM companyaccounts WHERE companyid = %s", (company_id,)
    )
    profile_image = cursor.fetchone()[0]

    if profile_image is None:
        return (
            jsonify(
                {
                    "ProfileImage error": f"Could not find Profile Image for company id {company_id}"
                }
            ),
            500,
        )

    temp_image_path = os.path.join(
        "temp", "tempImages", f"profile_image_{company_id}.jpg"
    )
    with open(temp_image_path, "wb") as temp_file:
        temp_file.write(profile_image)

    ####   Generate Interview
    questions, paths = generateInterview(job_description, 1, temp_image_path, "male")
    paths = ["/" + path.replace(os.sep, "/") for path in paths]
    print(paths)
    session["interview_questions"] = questions
    session["interview_videos"] = paths
    os.remove(temp_image_path)
    return jsonify({"videoPaths": paths})


@app.route("/candidate/recieve_response", methods=["POST"])
def recieveResponses():
    print("called api")
    try:
        for path in session["interview_videos"]:
            os.remove(os.path.normpath(path))

        video_files = {}
        audio_files = {}

        for key, file in request.files.items():
            if key.startswith("video_"):
                video_files[key] = file
            elif key.startswith("audio_"):
                audio_files[key] = file
        print("audio_files: ", audio_files)

        # Create a temporary directory
        temp_dir = os.path.join("temp", "tempAudioResponses")
        video_paths = []
        audio_paths = []

        # Save video files to the temporary directory
        for key, file in video_files.items():
            print(file.filename)
            video_path = os.path.join(temp_dir, file.filename)
            file.save(video_path)
            video_paths.append(video_path)

        for key, file in audio_files.items():
            print(file.filename)
            audio_path = os.path.join(temp_dir, file.filename)
            file.save(audio_path)
            audio_paths.append(audio_path)

        evaluate_thread = threading.Thread(
            target=Evaluate,
            args=(session["interview_questions"], audio_paths, video_paths),
        )
        evaluate_thread.start()

        return jsonify({"message": "Files received"})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "An error occurred"}), 500


#######################################################  LOG OUT   #############################################################


@app.route("/logout")
def logout():
    session.clear()  # Clear the session, effectively logging the user out
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
