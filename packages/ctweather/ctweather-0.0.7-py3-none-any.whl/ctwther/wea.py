import spacy
from googletrans import Translator
import requests
import json
from datetime import date, datetime



# OpenWeatherMap API KEY

api_key='5c6f3029dfd62ba47cd3c799b1f8e8d4'

# 내일모레 인식이 부정확할시 
t_ref = ['내일모레','모레']

def test(text):

    
    ktx= text
    cities, times = extract_city_time(ktx)
    

    if len(cities)>0 and len(times)>0:
        ci = trans_ko_to_en(cities[0])
        ti = times[0]
        weathers=get_weather(ci, ti)        
    
        if len(weathers)>0:
           temp_i = str(weathers['main']['temp'])
           humid_i = str(weathers['main']['humidity'])
           weather_i = weathers['weather'][0]['description']
           w_text = trans_en_to_ko(weather_i)
    
           print(ti, cities[0],'날씨는 다음과 같습니다.')
           print('날씨:', w_text,'(',weather_i,')')
           print('온도:', temp_i,'도')
           print('습도:', humid_i,'%')


def get_weather(city_name, c_time):
    weather_info={}
    
    try:
        # OpenWeatherMap API 
        api = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={api_key}&units=metric"
        r = requests.get(api)
        wd = json.loads(r.text)
        if wd['cod']=='200':

            dd = datetime.today()
            dh = dd.hour
            
            
            if c_time =='오늘':
               # temp_info = wd['list'][0]['main']['temp']
               # humid_info = wd['list'][0]['main']['humidity']
               # weather_info = wd['list'][0]['weather'][0]['main']
               wd_info = wd['list'][2]

            elif c_time=='내일':
                # 다음날 09시 기준
                wd_info = wd['list'][6]

            elif c_time == '내일모레':
                 # 다다음날 09시 기준
                wd_info = wd['list'][14]

            else:
                print('말씀하신 날짜의 날씨 정보를 가져올 수 없습니다')
                raise OWAError
            
            weather_info = wd_info
            
        else:
            raise OWAError
             
                                                   

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")
    except (OWAError) as e:
        print('에러발생:',e)      
    

    return weather_info
        

def trans_ko_to_en(text):
    # Translator 객체 생성
    translator = Translator()
    
    # 한글에서 영어로 번역
    translated = translator.translate(text, src='ko', dest='en')
    
    return translated.text

def trans_en_to_ko(text):
    # Translator 객체 생성
    translator = Translator()
    
    # 한글에서 영어로 번역
    translated = translator.translate(text, src='en', dest='ko')
    
    return translated.text

def extract_city_time(text):
    
    try:
        nlp = spacy.load("ko_core_news_sm")
        doc = nlp(text)
        # 도시 및 시간에 관련된 엔티티 추출
        cities = [ent.text for ent in doc.ents if ent.label_ == "LC"]
        timee = [ent.text for ent in doc.ents if ent.label_ == "DT"]
        if len(timee)==0:
            if text.find(t_ref[0])>= 0:
                timee.append(t_ref[0])
            elif text.find(t_ref[1])>= 0:
                timee.append(t_ref[0])
        if len(cities)==0 and len(timee)==0:
            raise CityTimeError
        if len(cities)==0 :
            raise CityError
        if len(timee)==0 :
            raise TimeError 
         
    except (CityTimeError, CityError,TimeError) as e:
        print('에러발생:',e)      
    
    return cities, timee


class CityTimeError(Exception):    # Exception을 상속받아서 새로운 예외를 만듦
    def __init__(self):
        super().__init__('도시 또는 시간을 모두 인식하지 못했습니다.')

class CityError(Exception):    
    def __init__(self):
        super().__init__('도시 이름을 인식하지 못했습니다 큰 도시 이름을  입력해주세요.')

class TimeError(Exception):    
    def __init__(self):
        super().__init__('시간을 인식하지 못했습니다 오늘, 내일, 내일모레로 입력해주세요.')   

class OWAError(Exception):
    def __init__(self):
        super().__init__('오픈 웨더 맵 날씨 정보를 가져오지 못했습니다. 좀 더 큰 도시나 주/국가로 시도해보세요')  

