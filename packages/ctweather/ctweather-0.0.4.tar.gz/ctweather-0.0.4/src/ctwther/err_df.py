
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
