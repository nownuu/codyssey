import socket
import sys
import threading
from typing import Optional

ENCODING = 'utf-8'
EOL = '\n'


def recv_loop(sock: socket.socket) -> None:
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                print('서버 연결이 종료되었습니다.')
                break
            text = data.decode(ENCODING)
            for line in text.splitlines():
                print(line)
    except (ConnectionResetError, ConnectionAbortedError):
        print('서버와의 연결이 끊어졌습니다.')
    finally:
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        sock.close()


def main() -> None:
    host = '127.0.0.1'
    port = 5000

    if len(sys.argv) >= 2:
        host = sys.argv[1]
    if len(sys.argv) >= 3:
        try:
            port = int(sys.argv[2])
        except ValueError:
            print('포트는 정수여야 합니다. 예: python client.py 127.0.0.1 5000')
            return

    username: Optional[str] = None
    while not username:
        username = input('사용자 이름을 입력하세요: ').strip()
        if not username:
            print('빈 사용자 이름은 사용할 수 없습니다.')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except OSError as exc:
        print(f'서버에 연결할 수 없습니다: {exc}')
        sock.close()
        return

    sock.sendall((username + EOL).encode(ENCODING))

    t = threading.Thread(target=recv_loop, args=(sock,), daemon=True)
    t.start()

    print('채팅을 시작합니다. 종료하려면 \'/종료\'를 입력하세요.')
    try:
        while True:
            try:
                msg = input()
            except EOFError:
                msg = '/종료'

            if msg == '/종료':
                try:
                    sock.sendall((msg + EOL).encode(ENCODING))
                except OSError:
                    pass
                break

            try:
                sock.sendall((msg + EOL).encode(ENCODING))
            except OSError:
                print('메시지를 전송할 수 없습니다. 연결이 끊어졌을 수 있습니다.')
                break
    except KeyboardInterrupt:
        try:
            sock.sendall(('/종료' + EOL).encode(ENCODING))
        except OSError:
            pass
    finally:
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        sock.close()


if __name__ == '__main__':
    main()
