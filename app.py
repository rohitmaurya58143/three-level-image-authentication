from flask import Flask, render_template, request

from database import create_database, add_user, get_user
from password_auth import hash_password, check_password
from image_auth import check_image_password
from otp_auth import generate_otp, verify_otp, can_resend_otp, resend_otp
from email_service import send_otp_email
from attempts import record_failure, reset_attempts, reset_level


app = Flask(__name__)


# Home page
@app.route("/")
def home():

    return render_template("index.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():

    # Show login page
    if request.method == "GET":

        return render_template("login.html")

    # Get login details
    username = request.form["username"]
    password = request.form["password"]

    # Find user
    user = get_user(username)

    if user is None:

        return render_template(
            "login.html",
            error="User not found!",
            username=username
        )

    # Check password
    if check_password(password, user[2]):

        # Fresh start for the next levels
        reset_attempts(username)

        return render_template(
            "image_login.html",
            username=username
        )

    # Wrong password
    attempts_used, attempts_left = record_failure(username, "login")

    if attempts_left <= 0:

        reset_attempts(username)

        return render_template(
            "login.html",
            error="Too many failed attempts. Please start again."
        )

    return render_template(
        "login.html",
        error=f"Wrong password. {attempts_left} attempt(s) left.",
        username=username
    )


# Register
@app.route("/register", methods=["GET", "POST"])
def register():

    # Show register page
    if request.method == "GET":

        return render_template("register.html")

    # Get registration details
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    image_password = request.form["image_password"]

    # Hash password
    hashed_password = hash_password(password)

    # Add user
    add_user(
        username,
        email,
        hashed_password,
        image_password
    )

    return "Registration successful!"


# Level 2 - Image Authentication
@app.route("/image-login", methods=["POST"])
def image_login():

    username = request.form["username"]

    selected_images = request.form["image_password"]

    selected_images = selected_images.split(",")

    user = get_user(username)

    if user is None:

        return render_template(
            "login.html",
            error="User not found! Please login again."
        )

    # Check image password
    if check_image_password(user[3], selected_images):

        reset_level(username, "image")

        # Generate OTP
        otp = generate_otp(username)

        email = user[1]

        # Send OTP
        if send_otp_email(email, otp):

            return render_template(
                "otp.html",
                username=username
            )

        return render_template(
            "image_login.html",
            username=username,
            error="OTP could not be sent! Please try again."
        )

    # Wrong image sequence
    attempts_used, attempts_left = record_failure(username, "image")

    if attempts_left <= 0:

        reset_attempts(username)

        return render_template(
            "login.html",
            error="Too many failed attempts. Please start again from Level 1."
        )

    return render_template(
        "image_login.html",
        username=username,
        error=f"Wrong image sequence. {attempts_left} attempt(s) left."
    )


# Resend OTP
@app.route("/resend-otp", methods=["POST"])
def resend_otp_page():

    username = request.form["username"]

    allowed, remaining = can_resend_otp(username)

    if not allowed:

        return render_template(
            "otp.html",
            username=username,
            error=f"Please wait {remaining} seconds before requesting a new code."
        )

    user = get_user(username)

    if user is None:

        return render_template(
            "login.html",
            error="User not found! Please login again."
        )

    otp = resend_otp(username)

    # A fresh code gets fresh attempts
    reset_level(username, "otp")

    email = user[1]

    if send_otp_email(email, otp):

        return render_template(
            "otp.html",
            username=username
        )

    return render_template(
        "otp.html",
        username=username,
        error="OTP could not be sent! Please try again."
    )


# Level 3 - OTP Authentication
@app.route("/verify-otp", methods=["POST"])
def verify_otp_page():

    username = request.form["username"]

    entered_otp = request.form["otp"]

    # Check OTP
    if verify_otp(username, entered_otp):

        reset_attempts(username)

        return render_template("success.html", username=username)

    # Wrong or expired OTP
    attempts_used, attempts_left = record_failure(username, "otp")

    if attempts_left <= 0:

        reset_attempts(username)

        return render_template(
            "login.html",
            error="Too many failed attempts. Please start again from Level 1."
        )

    return render_template(
        "otp.html",
        username=username,
        error=f"Wrong or expired code. {attempts_left} attempt(s) left."
    )


# Run application
if __name__ == "__main__":

    create_database()

    app.run(debug=True)