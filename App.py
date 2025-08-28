from flask import Flask, render_template, request
import re

app = Flask(__name__)

common_passwords = ["123456", "password", "qwerty", "123456789", "abc123", "111111"]

def check_password_strength(password):
    score = 0
    feedback = []

    # Length check
    if len(password) < 8:
        feedback.append("❌ Too short (minimum 8 characters)")
    elif len(password) >= 12:
        score += 2  # extra points for longer passwords
    else:
        score += 1

    # Uppercase, lowercase, digit, special char checks
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("❌ Add at least one uppercase letter")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Add at least one lowercase letter")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number")

    if re.search(r"[@$!%*?&]", password):
        score += 1
    else:
        feedback.append("❌ Add at least one special character (@, $, !, %, *, ?, &)")

    # Check for repeated characters
    if re.search(r"(.)\1{2,}", password):
        feedback.append("❌ Avoid repeated characters (like aaa111)")

    # Check for sequences (abc, 123, qwerty)
    if re.search(r"(0123|1234|2345|abcd|qwerty)", password.lower()):
        feedback.append("❌ Avoid simple sequences (1234, abcd, qwerty)")

    # Check against common passwords
    if password.lower() in common_passwords:
        feedback.append("❌ This is a very common password!")

    # Strength levels
    if score <= 3:
        strength = "Weak 🔴"
    elif score <= 5:
        strength = "Moderate 🟡"
    else:
        strength = "Strong 🟢"

    return strength, feedback


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    feedback = []
    pwd = ""
    if request.method == "POST":
        pwd = request.form["password"]
        result, feedback = check_password_strength(pwd)
    return render_template("index.html", result=result, feedback=feedback, pwd=pwd)


if __name__ == "__main__":
    app.run(debug=True)
