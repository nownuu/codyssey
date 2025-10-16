import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 메일 전송 함수
def send_email(sender_email, receiver_email, password, subject, body):
    # SMTP 서버와 포트 설정
    smtp_server = 'smtp.gmail.com'
    port = 465  # SSL 포트
    context = ssl.create_default_context()

    try:
        # 이메일 메시지 만들기
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # SMTP 서버에 연결 및 로그인
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print('메일이 성공적으로 전송되었습니다.')

    except smtplib.SMTPAuthenticationError:
        print('인증 실패: 이메일 주소나 비밀번호가 잘못되었습니다.')
    except smtplib.SMTPException as e:
        print(f'메일 전송 중 오류가 발생했습니다: {e}')
    except Exception as e:
        print(f'예기치 못한 오류가 발생했습니다: {e}')

# 메일을 보내는 함수 호출 예시
def main():
    # 보내는 사람과 받는 사람 설정
    sender_email = 'your_email@gmail.com'
    receiver_email = 'receiver_email@example.com'
    password = 'your_email_password'  # Gmail 계정의 앱 비밀번호 사용 (2단계 인증을 사용하는 경우)
    
    # 메일 제목과 본문 내용
    subject = '메일 제목'
    body = '이것은 Python을 이용한 자동 메일입니다.'

    # 이메일 전송
    send_email(sender_email, receiver_email, password, subject, body)

if __name__ == '__main__':
    main()
