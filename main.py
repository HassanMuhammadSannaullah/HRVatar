from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from utils import get_db_connection, account_exist_html

app = Flask(__name__)
app.static_folder = "static"
app.secret_key = "your_secret_key_here"


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
                return redirect(url_for("dashboard", name=first_name.replace(" ", "")))
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
                if validateLogin('company',email,password):
                    return redirect(
                        url_for("CompanyDashboard")
                    )
                else:
                    return 'Could Not Create Account Try Later Please'
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

    if loginType=='candidate':
        cursor.execute("SELECT * FROM CandidateAccounts WHERE Email = %s", (username,))
        result = cursor.fetchone()
        if result and result[-1] == password:
            session['logged_in']=True
            session['userdata']={'FirstName':result[1], 'LastName':result[2], 'email':result[3]}
            session['login_type']='candidate'
            session['CandidateID']=result[0]
            db.close()
            return True
    elif loginType=='company':
        cursor.execute("SELECT * FROM CompanyAccounts WHERE Email = %s", (username,))
        result = cursor.fetchone()
        if result and result[-1] == password:
            session['logged_in']=True
            session['userdata']={'HRName':result[1], 'CompanyName':result[2], 'email':result[3]}
            session['login_type']='company'
            session['CompanyID']=result[0]
            db.close()
            return True
        
    db.close()
    return False    


@app.route("/process_login")
def process_login():
    username = request.args.get("username")
    password = request.args.get("password")
    login_type = request.args.get("login_type")
    
    
    if validateLogin(login_type,username,password):
        if login_type=='company':
            return redirect(url_for('CompanyDashboard'))
        else:
            return f"Login Ok {login_type}"
    else:
        flash("Invalid credentials or login type", "error")
        return redirect(url_for("login"))





@app.route("/company/dashboard")
def CompanyDashboard():
    if 'logged_in' in session and session['logged_in']==True and session['login_type']=='company':
        return render_template('CompanyDashboard.html', name=session['userdata']['HRName'])
    else:
        return redirect(url_for('login'))

@app.route('/company/dashboard/add_job', methods=['POST'])
def add_job():
    try:
        if 'logged_in' in session and session['logged_in']==True and session['login_type']=='company':
            # Get the form data from the POST request
            #company_name = request.form.get('companyName')
            data = request.json  # Retrieve the JSON data from the request
            
            # Extract the form fields from the JSON data
            job_name = data.get('jobName')
            job_description = data.get('jobDescription')
            candidate_info = data.get('candidateInfo')

            # Connect to the database
            connection = get_db_connection()
            cursor = connection.cursor()

            # Insert the job data into the 'jobs' table
            sql_query = "INSERT INTO jobs (CompanyID, JobPosition, Description, CandidateRequirement) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql_query, (session['CompanyID'], job_name, job_description, candidate_info))

            # Commit the changes and close the connection
            connection.commit()
            cursor.close()
            connection.close()

            return jsonify({"message": "Job posted successfully!"}), 200
        else:
            return '401: Unauthorised Access Denied'

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Posting failed."}), 500
    
@app.route("/company/dashboard/get_jobs_data", methods=["POST"])
def get_jobs_data():
    try:
        if 'logged_in' in session and session['logged_in']==True and session['login_type']=='company':
            # Connect to the database
            connection = get_db_connection()
            cursor = connection.cursor()

            # Query to fetch all jobs from the 'jobs' table
            sql_query = "SELECT JobPosition, Description, CandidateRequirement, PostedOnLinkedIn, StillHiring FROM jobs where CompanyID= %s"
            cursor.execute(sql_query,(session['CompanyID'],))

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
                    "StillHiring": job[4]
                }
                jobs_list.append(job_dict)

            # Close the cursor and the connection
            cursor.close()
            connection.close()

            # Return the jobs list as a JSON response
            return jsonify({"jobs": jobs_list}), 200
        else:
            return '401: Unauthorised Access Denied'

    except Exception as e:
        print("Error:", e)
        return jsonify({"message": "Failed to fetch jobs data."}), 500

@app.route('/logout')
def logout():
    session.clear()  # Clear the session, effectively logging the user out
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
