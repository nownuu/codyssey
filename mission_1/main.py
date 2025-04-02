from datetime import datetime

def read_log_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f'파일을 찾을 수 없습니다: {filepath}')
        return []
    except Exception as e:
        print(f'파일을 읽는 중 오류 발생: {e}')
        return []

#  timestamp 정렬
def sort_logs_by_timestamp(log_lines):
    log_entries = []
    for line in log_lines[1:]:
        parts = line.strip().split(',')
        timestamp_str = parts[0]
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        log_entries.append((timestamp, line.strip()))
    
    log_entries.sort(key=lambda x: x[0], reverse=True)
    
    return [entry[1] for entry in log_entries]


#  markdown 생성
def analyze_logs(log_lines):
    report = []
    report.append('# 로그 분석\n')


    accident_logs = []
    problematic_logs = []  # 문제 리스트
    important_events = []  # 중요한 이벤트 리스트
    
    # 사고와 관련된 로그 (산소 탱크 불안정, 폭발)
    for line in log_lines:
        if 'oxygen tank' in line.lower(): #산소 탱크
            accident_logs.append(line.strip())
            problematic_logs.append(line.strip())
    
    # 중요한 이벤트
    for line in log_lines:
        if 'liftoff' in line.lower() or 'engine ignition' in line.lower() or 'satellite deployment' in line.lower():
            important_events.append(line.strip())

    # 사고 관련 로그 보고서에 추가
    if accident_logs:
        report.append('### 사고 발생 로그\n')
        report.append('- **발생 시각**: ' + ', '.join([log.split(',')[0] for log in accident_logs]) + '\n')
        report.append('- **이벤트 로그**:\n')
        for log in accident_logs:
            report.append(f'  - {log}\n')
    else:
        report.append('- 사고와 관련된 로그를 찾지 못했습니다.\n')

    # 주요 이벤트 관련 로그 보고서에 추가
    if important_events:
        report.append('### 주요 이벤트 로그\n')
        for event in important_events:
            report.append(f'  - {event}\n')

    return '\n'.join(report), problematic_logs

#  markdown 저장
def save_report(filepath, content):
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f'보고서 생성 완료: {filepath}')
    except Exception as e:
        print(f'보고서 저장 오류 : {e}')

def save_problematic_logs(filepath, problematic_logs):
    try:
        with open(filepath, 'w', encoding='utf-8') as file:
            for log in problematic_logs:
                file.write(log + '\n')
        print(f'문제 로그 파일 생성: {filepath}')
    except Exception as e:
        print(f'문제 로그를 저장 오류 : {e}')


# 시간 역순 로그 출력
def print_logs_in_reverse_order(log_lines):
    for log in log_lines:
        print(log)

if __name__ == '__main__':
    log_path = 'mission_computer_main.log'
    report_path = 'log_analysis.md'
    problematic_log_path = 'problematic_logs.txt'

    logs = read_log_file(log_path)
    sorted_logs = sort_logs_by_timestamp(logs)
    print_logs_in_reverse_order(sorted_logs)
    report_content, problematic_logs = analyze_logs(sorted_logs)
    save_report(report_path, report_content)
    save_problematic_logs(problematic_log_path, problematic_logs)
