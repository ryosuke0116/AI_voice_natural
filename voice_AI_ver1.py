import speech_recognition
import pyttsx3
import datetime
import locale
import requests
from bs4 import BeautifulSoup

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




locale.setlocale(locale.LC_TIME, 'ja_JP')

robot_ear = speech_recognition.Recognizer()
robot_mouth = pyttsx3.init()
robot_brain = ""

def change_voice(engine, language, gender='VoiceGenderFemale'):
  for voice in engine.getProperty('voices'):
    if language in voice.languages and gender == voice.gender:
      engine.setProperty('voice', voice.id)
      return True
  raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))

while True:
  with speech_recognition.Microphone() as mic:
    print("ロボット: 聞いています。")
    audio = robot_ear.record(mic, duration = 2)

  print("ロボット: ...")
  try:
    you = robot_ear.recognize_google(audio, language='ja_JP')
  except:
    you = "..."
  print("自分: " + you)

  if "..." in you:
    robot_brain = "聞き取れないのでもう一度話してください。"
  elif "こんにちは" in you:
    robot_brain = "こんにちは、ズオン。"
  elif "今日" in you:
    robot_brain = datetime.datetime.now().strftime("%B %d, %Y")
  elif "天気" in you:
    weather_info = GetYahooWeather(6310)
    print(weather_info)
  elif "バイバイ" in you:
    robot_brain = "また、ズオン。"
    print("ロボット: " + robot_brain)
    change_voice(robot_mouth, "ja_JP", "VoiceGenderFemale")
    robot_mouth.say(robot_brain)
    robot_mouth.runAndWait()
    break
  else:
    robot_brain = "はっきり発音してください。"

  print("ロボット: " + robot_brain)

  change_voice(robot_mouth, "ja_JP", "VoiceGenderFemale")
  robot_mouth.say(robot_brain)
  robot_mouth.runAndWait()
