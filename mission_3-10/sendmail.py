import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_mail():
    # 1️⃣ Gmail 서버 정보
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    # 2️⃣ 계정 정보
    sender_email = 'your_email@gmail.com'
    sender_password = 'your_password'  # Gmail 보안 설정에서 앱 비밀번호 사용
    receiver_email = 'receiver@example.com'

    # 3️⃣ 메일 제목과 내용 설정
    subject = 'Test Email from Python'
    body = '이 메일은 Python의 smtplib을 사용해 보낸 테스트 메일입니다.'

    # 4️⃣ 메시지 생성
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # 5️⃣ SMTP 서버 연결 및 로그인
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # TLS 암호화 시작
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print('메일이 성공적으로 전송되었습니다.')

    except smtplib.SMTPAuthenticationError:
        print('인증 오류: 이메일 주소나 비밀번호를 확인하세요.')
    except smtplib.SMTPConnectError:
        print('연결 오류: SMTP 서버에 연결할 수 없습니다.')
    except Exception as e:
        print('메일 전송 중 오류 발생:', e)


if __name__ == '__main__':
    send_mail()
