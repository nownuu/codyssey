from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # index.html 파일 읽기
        try:
            with open('index.html', 'rb') as file:
                content = file.read()

            # 응답 코드와 헤더 전송
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            # 파일 내용 전송
            self.wfile.write(content)

            # 서버 콘솔에 접속 정보 출력
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            client_ip = self.client_address[0]
            print(f'[{current_time}] Client connected from {client_ip}')

        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')


def run(server_class=HTTPServer, handler_class=MyHandler):
    server_address = ('', 8080)  # 모든 인터페이스에서 8080 포트 사용
    httpd = server_class(server_address, handler_class)
    print('Starting server on port 8080...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
