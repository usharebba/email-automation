from flask import Flask, render_template, request, redirect, flash
import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "supersecret"

# 🔹 Configure your email account here
SMTP_SERVER = "smtp.gmail.com"   # change for Outlook/SES/etc
SMTP_PORT = 465
EMAIL_ADDRESS = "ushasreechandrarebba@gmail.com"
EMAIL_PASSWORD = "vyhu qulw ysaj znzr"   # for Gmail use App Password

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        to_email = request.form["to_email"]
        subject = request.form["subject"]
        body = request.form["body"]
        file = request.files.get("resume")

        try:
            # setup email
            msg = MIMEMultipart()
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            filepath = None
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)

                with open(filepath, "rb") as f:
                    mime = MIMEBase("application", "octet-stream")
                    mime.set_payload(f.read())
                    encoders.encode_base64(mime)
                    mime.add_header("Content-Disposition", f"attachment; filename={filename}")
                    msg.attach(mime)

            # send email
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)

            # cleanup
            if filepath and os.path.exists(filepath):
                os.remove(filepath)

            flash("✅ Email sent successfully!", "success")

        except Exception as e:
            flash(f"❌ Failed to send email: {str(e)}", "danger")

        return redirect("/")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
