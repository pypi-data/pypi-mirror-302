import spacy
from googletrans import Translator
import requests
import json
from datetime import date, datetime
import err_df


# OpenWeatherMap API KEY

f=open("owm_apikey.txt",'r')
line = f.read()
api_key= line
f.close()


# OpenWeatherMap API 
api ='http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={key}&units=metric'

# 내일모레 인식이 부정확할시 
t_ref = ['내일모레','모레']


def get_weather(city_name, c_time):
    weather_info={}
    
    try:
        
        url = api.format(city=city_name, key=api_key)
        r = requests.get(url)
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
                raise err_df.OWAError
            
            weather_info = wd_info
            
        else:
            raise err_df.OWAError
             
                                                   

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Something went wrong: {err}")
    except (err_df.OWAError) as e:
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
            raise err_df.CityTimeError
        if len(cities)==0 :
            raise err_df.CityError
        if len(timee)==0 :
            raise err_df.TimeError 
         
    except (err_df.CityTimeError, err_df.CityError,err_df.TimeError) as e:
        print('에러발생:',e)      
    
    return cities, timee
