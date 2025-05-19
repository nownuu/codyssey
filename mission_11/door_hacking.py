import zipfile
import itertools
import string
import time
from datetime import datetime
import threading
import queue
import zlib

zip_file_path = "mission_11\emergency_storage_key.zip"
password_file_path = "mission_11\password.txt"
num_threads = 8  # CPU 코어 수에 따라 조절
found_event = threading.Event()
password_queue = queue.Queue()
start_time = time.time()
start_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print(f"[시작 시간] {start_dt}")

# 전체 가능한 패스워드 생성기
def generate_passwords():
    chars = string.ascii_lowercase + string.digits
    for p in itertools.product(chars, repeat=6):
        yield ''.join(p)

# 작업자 스레드 정의
def worker(thread_id, file_list):
    while not found_event.is_set():
        try:
            password = password_queue.get(timeout=1)
        except queue.Empty:
            return
        try:
            with zipfile.ZipFile(zip_file_path) as zf:
                with zf.open(file_list[0], pwd=password.encode()) as file:
                    file.read(1)  # 암호 확인용 최소 IO
            # 암호가 맞으면
            found_event.set()
            elapsed = time.time() - start_time
            print(f"[성공] Thread-{thread_id} | 암호: '{password}' | 소요 시간: {elapsed:.2f}초")

            with open(password_file_path, "w") as f:
                f.write(password)
        except Exception as e:
            elapsed = time.time() - start_time
            print(f"[Thread-{thread_id}] 실패: {password} | 소요 시간: {elapsed:.2f}초")
        finally:
            password_queue.task_done()

def unlock_zip():
    try:
        with zipfile.ZipFile(zip_file_path) as zf:
            file_list = zf.namelist()
            # 패스워드 큐에 채워 넣기
            for password in generate_passwords():
                password_queue.put(password)

            # 스레드 시작
            threads = []
            for i in range(num_threads):
                t = threading.Thread(target=worker, args=(i + 1, file_list))
                t.start()
                threads.append(t)

            password_queue.join()  # 모든 작업 대기
            for t in threads:
                t.join()

            if not found_event.is_set():
                print("[실패] 암호를 찾지 못했습니다.")
    except FileNotFoundError:
        print(f"[오류] zip 파일을 찾을 수 없습니다: {zip_file_path}")
    except Exception as e:
        print(f"[예외 발생] {e}")

if __name__ == "__main__":
    unlock_zip()
