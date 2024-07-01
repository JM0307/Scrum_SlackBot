
import datetime
import requests
from datetime import datetime
from pytimekr import pytimekr
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Slack API 토큰과 채널 설정
slack_token = "slack-token"
channel_id = "#슬랙봇-테스트"
client = WebClient(token=slack_token)

# OpenWeatherMap API 설정
weather_api_key = "98b326cee46af63557c52d73cea1c871"
location = "Seoul,KR"

# 대한민국 공휴일 설정
now = datetime.now()
day = now.weekday()
today = now.today().strftime("%Y. %m. %d") 

def get_weather_emoji():
    # OpenWeatherMap API를 호출하여 현재 날씨 정보를 가져옵니다.
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={weather_api_key}&lang=kr"
    response = requests.get(url)
    data = response.json()
    
    weather_main = data['weather'][0]['main'].lower()

    # 날씨 상태에 따른 이모지 설정
    if 'clear' in weather_main:
        return "☀️"
    elif 'clouds' in weather_main:
        return "☁️"
    elif 'rain' in weather_main:
        return "🌧️"
    elif 'snow' in weather_main:
        return "❄️"
    elif 'thunderstorm' in weather_main:
        return "⛈️"
    elif 'drizzle' in weather_main:
        return "🌦️"
    elif 'mist' in weather_main:
        return "🌫️"
    else:
        return "🌥️"

def send_slack_message(): 
    weather_emoji = get_weather_emoji()

    try:
        response = client.chat_postMessage(
            channel=channel_id,
            text=f"*[{weather_emoji}{datetime.strftime(datetime.now(),'%Y. %m. %d')} 데일리 스크럼]*\n" +
            "스레드 댓글에 작성해 주세요."
        
        )
        print(response)
    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")

def main():
    list = pytimekr.holidays()
    holiday = False

    for i in list:
        if(today == str(i)):
            holiday = True

    if day > 4 or holiday:
        print("행복한 휴일 보내세요!")
    else:
        send_slack_message()

if __name__ == "__main__":
    main()
