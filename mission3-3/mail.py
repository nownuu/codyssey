import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def read_mail_targets(file_name):
    targets = []
    with open(file_name, 'r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            name = row['이름'].strip()
            email = row['이메일'].strip()
            targets.append((name, email))
    return targets

def send_html_mail(smtp_server, port, sender, password, subject, html_content, targets):
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender, password)
        for name, email in targets:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = email

            personalized_html = html_content.replace('{name}', name)
            mime_text = MIMEText(personalized_html, 'html')
            msg.attach(mime_text)

            server.sendmail(sender, email, msg.as_string())
            print(f'Mail sent to {name} <{email}>')

def main():
    smtp_server = 'smtp.gmail.com'
    port = 587
    sender = 'your_email@gmail.com'
    password = 'your_password'

    subject = 'Message from Mars - Dr. Han'
    html_content = '''
    <html>
      <body>
        <p>Dear {name},<br>
        We received your message and we all froze.<br>
        We cried and hugged, so grateful that you are alive.<br><br>
        <b>We will do our best too!</b><br>
        Just in case your condition is not good, we send this message in English.<br><br>
        With love,<br>
        Your Earth Team 🌍
        </p>
      </body>
    </html>
    '''

    targets = read_mail_targets('mail_target_list.csv')
    send_html_mail(smtp_server, port, sender, password, subject, html_content, targets)

if __name__ == '__main__':
    main()
