import os
import csv
import speech_recognition as sr


def get_audio_files(directory):
    audio_files = []
    for file_name in os.listdir(directory):
        if file_name.endswith('.wav'):
            audio_files.append(os.path.join(directory, file_name))
    return audio_files


def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    audio_data = sr.AudioFile(file_path)
    results = []

    with audio_data as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio, show_all=False)
            results.append((0.0, text))
        except sr.UnknownValueError:
            results.append((0.0, '음성 인식 실패'))
        except sr.RequestError as e:
            results.append((0.0, 'API 요청 실패: {0}'.format(e)))
    return results


def save_transcription(file_path, transcription):
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    csv_file = base_name + '.csv'
    with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'Text'])
        for time, text in transcription:
            writer.writerow([time, text])


def search_keyword_in_csv(directory, keyword):
    for file_name in os.listdir(directory):
        if file_name.endswith('.csv'):
            with open(os.path.join(directory, file_name), mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    if keyword in row[1]:
                        print(f'[파일: {file_name}] 시간: {row[0]} 텍스트: {row[1]}')


def main():
    directory = 'audio'
    audio_files = get_audio_files(directory)

    for file_path in audio_files:
        transcription = transcribe_audio(file_path)
        save_transcription(file_path, transcription)

    keyword = input('검색할 키워드를 입력하세요 (Enter로 생략): ')
    if keyword:
        search_keyword_in_csv(directory, keyword)


if __name__ == '__main__':
    main()
