# 날씨 정보 제공 패키지

## 목적
이 패키지는 사용자가 `OpenWeatherMap API`의 일기예보 정보를 간편하게 조회할 수 있도록 돕기 위해 개발되었습니다. 

## 사용하기
이 패키지는 Python 3.11에서 동작을 확인했습니다.

1. [openweathermap api key](https://openweathermap.org/api) 발급
2. openai api key 발급
3. 프로젝트 루트 혹은 특정 위치에 .env 파일 생성
```bash
OPENWEATHERMAP_API_KEY=""
OPENAI_API_KEY=""
```
4. 패키지 설치
```bash
pip install ask_weather
```
5. 실행
```python
from ask_weather.agent import WeatherAgent
# WeatherAgent 인스턴스 생성
agent = WeatherAgent(
    env_path=".env api key file path", # (default. ".env")
    model="only support openai models", # (default. "gpt-4o-mini")
    temperature=0,
    verbose=False,
    max_iterations=10,
    max_execution_time=100000,
    handle_parsing_errors=False,
    return_intermediate_steps=False
)
# 위치와 날짜에 대한 질의
location = "Seoul"
date = "2024-10-15"
query = f"{date}의 {location} 날씨가 궁금해요."
result = agent.query(query)
print(result)
```

### source에서 패키지 설치
```bash
# Poetry로 패키지 설치
poetry install
# poetry env use python3.11
```

### 테스트하기
```bash
poetry run pytest
```

### package 만들기
1. [pypi](https://pypi.org/) 회원가입 후 api key 발급
2. `poetry config pypi-token.pypi api_key` 실행
3. `poetry build`로 whl 파일 생성
4. `poetry publish --build`로 프로젝트 배포

## TODO
[] 과거 시간의 기상 상황 검색
[] weather api dictionary 정보 다양하게 활용


### reference
이 프로젝트는 [위키독스 LangChain 가이드](https://wikidocs.net/261571)를 참고했습니다.