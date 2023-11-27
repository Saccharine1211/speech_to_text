import speech_recognition as sr
import pyaudio

def list_microphones():
    """ 연결된 마이크 장치 목록을 출력하고 선택된 장치 인덱스를 반환합니다. """
    p = pyaudio.PyAudio()
    num_devices = p.get_device_count()
    
    print("연결된 오디오 장치 목록:")
    for i in range(num_devices):
        device_info = p.get_device_info_by_index(i)
        if device_info['maxInputChannels'] > 0:  # 입력 채널이 있는 장치만 출력
            print(f"장치 {i}: {device_info['name']}")
    
    p.terminate()
    
    # 사용자 입력을 받아 선택된 장치 인덱스 반환
    device_index = int(input("사용할 마이크 장치 번호를 입력하세요: "))
    return device_index

def recognize_speech(device_index, wake_word):
    """ 선택된 마이크 장치를 사용하여 wake word를 감지하고 음성 인식을 수행합니다. """
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=device_index) as source:
        recognizer.adjust_for_ambient_noise(source)  # 배경 소음 조정
        print(f"{wake_word}를 기다리는 중...")

        while True:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language='ko-KR')

                # Wake word 감지
                if wake_word in text:
                    print(f"{wake_word} 감지됨! 추가 음성을 말하세요...")
                    audio = recognizer.listen(source)
                    # 추가 음성 인식
                    text = recognizer.recognize_google(audio, language='ko-KR')
                    print("인식된 문장:", text)
                    break

            except sr.UnknownValueError:
                continue
            except sr.RequestError as e:
                print(f"구글 API에서 오류가 발생했습니다; {e}")
                break

# 마이크 장치 목록을 출력하고 사용자 입력을 받음
selected_device_index = list_microphones()

# 선택된 마이크를 사용하여 wake word 감지 및 음성 인식
wake_word = "안녕"  # Wake word 설정
recognize_speech(selected_device_index, wake_word)
