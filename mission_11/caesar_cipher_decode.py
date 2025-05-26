def caesar_cipher_decode(target_text):
    decoded_results = []
    for shift in range(26):
        decoded = ''
        for char in target_text:
            if 'A' <= char <= 'Z':
                decoded += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            elif 'a' <= char <= 'z':
                decoded += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            else:
                decoded += char
        print(f'[{shift}] {decoded}')
        decoded_results.append((shift, decoded))
    return decoded_results

def read_password_file(file_path):
    try:
        with open(file_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f'[오류] 파일을 찾을 수 없습니다: {file_path}')
        return ''
    except Exception as e:
        print(f'[예외 발생] {e}')
        return ''

def save_result_to_file(result_text, file_path='mission\result.txt'):
    try:
        with open(file_path, 'w') as f:
            f.write(result_text)
        print(f'[저장 완료] result.txt에 저장되었습니다.')
    except Exception as e:
        print(f'[저장 실패] {e}')

if __name__ == '__main__':
    password_path = 'mission_11\password.txt'
    encrypted_text = read_password_file(password_path)

    if encrypted_text:
        print('[해독 시도]')
        results = caesar_cipher_decode(encrypted_text)

        selected_shift = input('\n정상적으로 해독된 번호를 입력하세요: ')
        if selected_shift.isdigit():
            shift_index = int(selected_shift)
            if 0 <= shift_index < 26:
                final_result = results[shift_index][1]
                save_result_to_file(final_result)
            else:
                print('[오류] 0~25 사이의 숫자를 입력하세요.')
        else:
            print('[오류] 숫자를 입력해야 합니다.')
