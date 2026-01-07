import streamlit as st
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from tempfile import NamedTemporaryFile

# ---------------- CONFIG ----------------
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_ADDRESS = "ushasreechandrarebba@gmail.com"
EMAIL_PASSWORD = "vyhu qulw ysaj znzr"   # ⚠️ move to secrets in production

# ---------------- UI ----------------
st.set_page_config(page_title="Cold Email Sender", layout="centered")

st.title("📧 Cold Emailing with Resume")
st.write("Send professional emails with resume attachment")

with st.form("email_form"):
    to_email = st.text_input("Recipient Email")
    subject = st.text_input("Subject")
    body = st.text_area("Message Body", height=150)
    resume = st.file_uploader("Upload Resume", type=["pdf", "doc", "docx"])
    submit = st.form_submit_button("Send Email")

# ---------------- LOGIC ----------------
if submit:
    if not to_email or not subject or not body:
        st.warning("⚠️ Please fill all required fields")
    else:
        try:
            msg = MIMEMultipart()
            msg["From"] = EMAIL_ADDRESS
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            # handle attachment
            if resume:
                with NamedTemporaryFile(delete=False) as tmp:
                    tmp.write(resume.read())
                    tmp_path = tmp.name

                with open(tmp_path, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename={resume.name}",
                    )
                    msg.attach(part)

                os.remove(tmp_path)

            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)

            st.success("✅ Email sent successfully!")

        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")
