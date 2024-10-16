import wea

def test(text):

    
    ktx= text
    cities, times = wea.extract_city_time(ktx)
    

    if len(cities)>0 and len(times)>0:
        ci = wea.trans_ko_to_en(cities[0])
        ti = times[0]
        weathers=wea.get_weather(ci, ti)        
    
        if len(weathers)>0:
           temp_i = str(weathers['main']['temp'])
           humid_i = str(weathers['main']['humidity'])
           weather_i = weathers['weather'][0]['description']
           w_text = wea.trans_en_to_ko(weather_i)
    
           print(ti, cities[0],'날씨는 다음과 같습니다.')
           print('날씨:', w_text,'(',weather_i,')')
           print('온도:', temp_i,'도')
           print('습도:', humid_i,'%')



           

    




