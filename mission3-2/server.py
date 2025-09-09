import socket
import threading
from typing import Dict, Tuple

HOST = '0.0.0.0'
PORT = 5000
ENCODING = 'utf-8'
EOL = '\n'


class ChatServer:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients: Dict[socket.socket, str] = {}
        self.lock = threading.Lock()

    def start(self) -> None:
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen()
        print(f'서버가 {self.host}:{self.port}에서 대기 중입니다. Ctrl+C로 종료하세요.')

        try:
            while True:
                conn, addr = self.server_sock.accept()
                thread = threading.Thread(
                    target=self.handle_client,
                    args=(conn, addr),
                    daemon=True,
                )
                thread.start()
        except KeyboardInterrupt:
            print('\n서버를 종료합니다.')
        finally:
            with self.lock:
                for sock in list(self.clients.keys()):
                    try:
                        sock.shutdown(socket.SHUT_RDWR)
                    except OSError:
                        pass
                    sock.close()
                self.clients.clear()
            self.server_sock.close()

    def handle_client(self, conn: socket.socket, addr: Tuple[str, int]) -> None:
        try:
            username = self._recv_line(conn)
            if not username:
                conn.close()
                return
            username = username.strip()

            with self.lock:
                self.clients[conn] = username
            print(f'접속: {addr} -> {username}')

            self.broadcast(f'시스템> {username}님이 입장하셨습니다.')

            while True:
                line = self._recv_line(conn)
                if not line:
                    break

                msg = line.rstrip(EOL)
                if msg == '/종료':
                    break

                self.broadcast(f'{username}> {msg}')

        except (ConnectionResetError, ConnectionAbortedError):
            pass
        finally:
            with self.lock:
                username = self.clients.pop(conn, None)
            try:
                conn.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            conn.close()

            if username:
                self.broadcast(f'시스템> {username}님이 퇴장하셨습니다.')
                print(f'퇴장: {addr} -> {username}')

    def broadcast(self, message: str) -> None:
        data = (message + EOL).encode(ENCODING)
        with self.lock:
            dead = []
            for sock in self.clients.keys():
                try:
                    sock.sendall(data)
                except OSError:
                    dead.append(sock)
            for sock in dead:
                self.clients.pop(sock, None)

    def _recv_line(self, conn: socket.socket) -> str:
        chunks = []
        while True:
            try:
                buf = conn.recv(1024)
            except OSError:
                return ''
            if not buf:
                return ''
            chunks.append(buf)
            if b'\n' in buf:
                break
        data = b''.join(chunks)
        return data.decode(ENCODING).split('\n', 1)[0] + '\n'


def main() -> None:
    server = ChatServer(HOST, PORT)
    server.start()


if __name__ == '__main__':
    main()
