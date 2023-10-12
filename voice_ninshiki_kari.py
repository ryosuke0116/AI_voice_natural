import speech_recognition as sr
import pyttsx3
import datetime
import locale
import requests
from bs4 import BeautifulSoup

SAMPLERATE = 44100
def GetYahooWeather(AreaCode):
    """
    Yahoo天気予報をスクレイピングする関数。

    Parameters
    ----------
    AreaCode : int
        対象となる数値を指定。
    
    Returns
    -------
    str
    """
    url = "https://weather.yahoo.co.jp/weather/jp/13/" + str(AreaCode) + ".html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    rs = soup.find(class_='forecastCity')
    rs = [i.strip() for i in rs.text.splitlines()]
    rs = [i for i in rs if i != ""]
    weather_message = rs[0] + "の天気は" + rs[1] + "、明日の天気は" + rs[19] + "です。"
    return weather_message

def callback(in_data, frame_count, time_info, status):
    global sprec 
    try:
        audiodata = speech_recognition.AudioData(in_data,SAMPLERATE,2)
        sprec_text = sprec.recognize_google(audiodata, language='ja-JP')
        print(sprec_text)
    except speech_recognition.UnknownValueError:
        pass
    except speech_recognition.RequestError as e:
        pass
    finally:
        return (None, pyaudio.paContinue)
    
def change_voice(engine, voice_name):
    available_voices = engine.getProperty('voices')
    for voice in available_voices:
        if voice.name == voice_name:
            engine.setProperty('voice', voice.id)
            return True
    raise RuntimeError("Voice '{}' not found".format(voice_name))

locale.setlocale(locale.LC_TIME, 'ja_JP')

robot_ear = sr.Recognizer()
robot_mouth = pyttsx3.init()
robot_brain = ""

# 利用可能な声の名前を設定
selected_voice_name = "Microsoft Haruka Desktop - Japanese"

# 利用可能な声のリストを表示するためのコード
voices = robot_mouth.getProperty('voices')
for voice in voices:
    print("Voice: %s" % voice.name)

# 選択した声を設定
change_voice(robot_mouth, selected_voice_name)


def main():
    global sprec 
    sprec = speech_recognition.Recognizer()  # インスタンスを生成
    # Audio インスタンス取得
    audio = pyaudio.PyAudio() 
    stream = audio.open( format = pyaudio.paInt16,
                        rate = SAMPLERATE,
                        channels = 1, 
                        input_device_index = 1,
                        input = True, 
                        frames_per_buffer = SAMPLERATE*2, # 2秒周期でコールバック
                        stream_callback=callback)
    stream.start_stream()
    while stream.is_active():
        time.sleep(0.1)
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    

    
if __name__ == '__main__':
    main()