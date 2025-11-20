import smtplib
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"

# CSV 읽기
def load_receivers(csv_file):
    receivers = []
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            receivers.append({"name": row["이름"], "email": row["이메일"]})
    return receivers


# 개별 HTML 메일 전송
def send_mail_html_individual(receivers):
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        for person in receivers:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "Message from Dr. Han"
            msg["From"] = SENDER_EMAIL
            msg["To"] = person["email"]

            html_content = f"""
            <html>
                <body>
                    <p>{person['name']}님,<br><br>
                    Dr. Han!!<br>
                    We received your message, but we couldn't understand the situation.<br>
                    We all froze and cried after hugging each other.<br>
                    We are so grateful that you are alive, and we will do our best too.<br><br>
                    Just in case your condition is not good, we are sending this message in English.
                    </p>
                </body>
            </html>
            """

            msg.attach(MIMEText(html_content, "html"))
            server.sendmail(SENDER_EMAIL, person["email"], msg.as_string())

            print(f"메일 전송 완료 → {person['name']} ({person['email']})")


# 실행
receivers = load_receivers("mail_target_list.csv")
send_mail_html_individual(receivers)
