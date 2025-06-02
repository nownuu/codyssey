import os
import wave
import datetime
import pyaudio


def get_record_filename():
    now = datetime.datetime.now()
    filename = now.strftime('%Y%m%d-%H%M%S') + '.wav'
    return os.path.join('records', filename)


def ensure_records_directory():
    if not os.path.exists('records'):
        os.makedirs('records')


def record_audio(duration_seconds=5):
    chunk = 1024
    format_type = pyaudio.paInt16
    channels = 1
    rate = 44100

    audio = pyaudio.PyAudio()

    stream = audio.open(format=format_type,
                        channels=channels,
                        rate=rate,
                        input=True,
                        frames_per_buffer=chunk)

    print('Recording started...')
    frames = []

    for _ in range(0, int(rate / chunk * duration_seconds)):
        data = stream.read(chunk)
        frames.append(data)

    print('Recording finished.')

    stream.stop_stream()
    stream.close()
    audio.terminate()

    ensure_records_directory()
    file_path = get_record_filename()

    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(audio.get_sample_size(format_type))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))

    print('Saved recording to:', file_path)


if __name__ == '__main__':
    record_audio()
