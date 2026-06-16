from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)

app.secret_key = "volunteerhub_secret_key"

# ---------------- MYSQL CONNECTION ----------------

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dhara@123",
    database="volunteerhub_db"
)

cursor = db.cursor()

# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")

# ---------------- REGISTER PAGE ----------------

@app.route("/register")
def register():
    return render_template("register.html")

# ---------------- LOGIN PAGE ----------------

@app.route("/login")
def login():
    return render_template("login.html")

# ---------------- ADMIN LOGIN PAGE ----------------

@app.route("/admin-login")
def admin_login_page():
    return render_template("admin_login.html")

# ---------------- REGISTER USER ----------------

@app.route("/register_user", methods=["POST"])
def register_user():

    fullname = request.form["fullname"]
    email = request.form["email"]
    phone = request.form["phone"]
    age = request.form["age"]
    gender = request.form["gender"]
    skills = request.form["skills"]
    address = request.form["address"]
    password = request.form["password"]

    sql = """
    INSERT INTO volunteers
    (fullname,email,phone,age,gender,skills,address,password)
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        fullname,
        email,
        phone,
        age,
        gender,
        skills,
        address,
        password
    )

    cursor.execute(sql, values)
    db.commit()

    return redirect("/login")

# ---------------- USER LOGIN ----------------

@app.route("/login_user", methods=["POST"])
def login_user():

    email = request.form["email"]
    password = request.form["password"]

    sql = """
    SELECT * FROM volunteers
    WHERE email=%s AND password=%s
    """

    cursor.execute(sql, (email, password))

    user = cursor.fetchone()

    if user:

        session["email"] = email

        return redirect("/dashboard")

    return """
    <h2>Invalid Email or Password</h2>
    <br>
    <a href='/login'>Try Again</a>
    """

# ---------------- USER DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "email" not in session:
        return redirect("/login")

    cursor.execute(
        "SELECT fullname,email FROM volunteers WHERE email=%s",
        (session["email"],)
    )

    user = cursor.fetchone()

    return render_template(
        "dashboard.html",
        user=user
    )

# ---------------- USER LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

# ---------------- ADMIN LOGIN ----------------

@app.route("/admin_login", methods=["POST"])
def admin_login():

    username = request.form["username"]
    password = request.form["password"]

    cursor.execute(
        """
        SELECT * FROM admins
        WHERE username=%s AND password=%s
        """,
        (username, password)
    )

    admin = cursor.fetchone()

    if admin:

        session["admin"] = username

        return redirect("/admin")

    return """
    <h2>Invalid Admin Credentials</h2>
    <br>
    <a href='/admin-login'>Try Again</a>
    """

# ---------------- ADMIN DASHBOARD ----------------

@app.route("/admin")
def admin():

    if "admin" not in session:
        return redirect("/admin-login")

    cursor.execute("SELECT * FROM volunteers")

    volunteers = cursor.fetchall()

    return render_template(
        "admin.html",
        volunteers=volunteers
    )

# ---------------- ADMIN LOGOUT ----------------

@app.route("/admin_logout")
def admin_logout():

    session.pop("admin", None)

    return redirect("/admin-login")

@app.route("/volunteers")
def volunteers():

    if "admin" not in session:
        return redirect("/admin-login")

    cursor.execute("SELECT * FROM volunteers")

    volunteers = cursor.fetchall()

    return render_template(
        "volunteers.html",
        volunteers=volunteers
    )
@app.route("/delete/<int:id>")
def delete(id):

    cursor.execute(
        "DELETE FROM volunteers WHERE id=%s",
        (id,)
    )

    db.commit()

    return redirect("/volunteers")
@app.route("/create_event", methods=["POST"])
def create_event():

    event_name = request.form["event_name"]
    event_date = request.form["event_date"]
    location = request.form["location"]
    description = request.form["description"]

    cursor.execute(
        """
        INSERT INTO events
        (event_name,event_date,location,description)
        VALUES(%s,%s,%s,%s)
        """,
        (event_name,event_date,location,description)
    )

    db.commit()

    return redirect("/admin")

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)