from langchain_core.tools import tool
import os
import requests
from datetime import datetime, timedelta
from ask_weather.utils.logger import get_logger
from ask_weather.utils.file_utils import parse_json_input

logger = get_logger(__file__)


@tool
def get_weather(input_data) -> str:
    """
    주어진 위치와 날짜에 대한 날씨 정보를 조회합니다.

    Args:
        input_data (dict): 날씨 정보를 조회하기 위한 입력 데이터
            - geo_data (list): 위치 정보를 포함한 리스트
            - date (str): 조회할 날짜
            - hours (bool): 시간 정보 포함 여부로 hours가 true일 경우 date는 'YYYY-mm-dd HH:MM' 형식을 따라야 한다. false일 경우 date는 'YYYY-mm-dd' 형식으로 충분하다.

    Returns:
        str: 날씨 정보에 대한 설명 문자열 또는 오류 메시지
    """
    input_data = parse_json_input(input_data)
    logger.info(f"{[input_data]} type : {type(input_data)}")

    geo_data = input_data.get("geo_data", [])

    if not geo_data:
        return "위치를 찾을 수 없습니다."

    date = input_data.get("date", None)
    hours = input_data.get("hours", False)

    api_key = os.getenv("OPENWEATHERMAP_API_KEY")

    params = {"appid": api_key, "units": "metric"}

    weather_results = []
    for location_data in geo_data:
        lat = location_data["lat"]
        lon = location_data["lon"]
        full_location_name = f"{location_data.get('name', '')}, {location_data.get('state', '')}, {location_data.get('country', '')}"
        params.update({"lat": lat, "lon": lon})
        logger.info(f"{full_location_name} ({lat}, {lon})")

        # 날짜를 기준으로 API 호출 URL 설정
        base_url = ""
        if date:
            target_date = datetime.strptime(
                date, "%Y-%m-%d %H:%M" if hours else "%Y-%m-%d"
            )
            current_date = datetime.now()
            logger.info(f"target_date: {target_date} current_date: {current_date}")

            # 과거 데이터
            if target_date < current_date:
                weather_results.append(f"{full_location_name}: 과거의 날씨는 현재 지원하지 않습니다.")
                continue

            # 5일 예보 데이터
            elif target_date <= current_date + timedelta(days=5):
                base_url = "http://api.openweathermap.org/data/2.5/forecast"
                logger.info(f"5일 예보 데이터 호출 설정 - URL: {base_url}, 파라미터: {params}")

            # 16일 예보 데이터
            elif target_date <= current_date + timedelta(days=16):
                base_url = "https://pro.openweathermap.org/data/2.5/forecast/daily"
                params["cnt"] = (target_date - current_date).days + 1
                logger.info(f"16일 예보 데이터 호출 설정 - URL: {base_url}, 파라미터: {params}")

            # 30일 예보 데이터
            elif target_date <= current_date + timedelta(days=30):
                base_url = "https://pro.openweathermap.org/data/2.5/forecast/climate"
                logger.info(f"30일 예보 데이터 호출 설정 - URL: {base_url}, 파라미터: {params}")
        else:
            base_url = "http://api.openweathermap.org/data/2.5/weather"
            logger.info(f"현재 날씨 데이터 호출 설정 - URL: {base_url}, 파라미터: {params}")

        try:
            logger.debug(f"API 요청 - URL: {base_url}, 파라미터: {params}")
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"API 요청 성공 - 상태 코드: {response.status_code}")
            logger.debug(f"data: {data}")

            found_data = data
            if "list" in data:
                minimum_timedelta = timedelta(days=32)

                if date:
                    for entry in data["list"]:
                        entry_date = datetime.strptime(
                            entry["dt_txt"], "%Y-%m-%d %H:%M:%S"
                        )
                        if abs(entry_date - target_date) < minimum_timedelta:
                            found_data = entry
                            minimum_timedelta = abs(entry_date - target_date)
                            logger.debug(
                                f"set minimum_timedelta {minimum_timedelta}, found_data: {found_data}"
                            )

                if found_data:
                    logger.debug(f"final parsed data : {found_data}")
                    weather_description = found_data["weather"][0]["description"]
                    temperature = found_data["main"]["temp"]
                    nearest_timedelta = found_data.get(
                        "dt_txt", datetime.now().strftime("%H:00")
                    )
                    logger.debug(
                        f"{full_location_name}의 {nearest_timedelta} 날씨: {weather_description}, 온도: {temperature}°C"
                    )
                    weather_results.append(
                        f"{full_location_name}의 {nearest_timedelta} 날씨: {weather_description}, 온도: {temperature}°C"
                    )
                else:
                    logger.debug(f"{full_location_name}: 해당 날짜의 날씨 데이터를 찾을 수 없습니다.")
                    weather_results.append(
                        f"{full_location_name}: 해당 날짜의 날씨 데이터를 찾을 수 없습니다."
                    )
            else:
                weather_description = data["weather"][0]["description"]
                temperature = data["main"]["temp"]
                logger.debug(
                    f"{full_location_name}의 현재 날씨: {weather_description}, 온도: {temperature}°C"
                )
                weather_results.append(
                    f"{full_location_name}의 현재 날씨: {weather_description}, 온도: {temperature}°C"
                )

        except requests.exceptions.RequestException as e:
            logger.error(f"날씨 정보를 가져오는데 실패했습니다: {e}")
            weather_results.append(
                f"{full_location_name}: 날씨 정보를 가져오는데 실패했습니다. 오류: {str(e)}"
            )
        except Exception as e:
            logger.error(f"데이터를 파싱하는데 실패했습니다. {e}")

    logger.debug(f"response of weather api: {weather_results}")
    return "\n\n".join(weather_results)


@tool
def get_location(input_data) -> str:
    """
    주어진 위치에 대한 위도 및 경도 정보를 조회합니다.

    Args:
        input_data (dict): 위치 정보를 조회하기 위한 입력 데이터
            location (str): 위치 이름입니다. 예를 들어 "Seoul" 또는 "New York"과 같은 도시명을 사용합니다.
            limit (int): 결과를 가져올 위치의 최대 개수. 기본값은 1이며, 최소값도 1이어야 합니다.

    Returns:
        list: 위치 정보가 포함된 리스트. 각 항목은 위도(lat) 및 경도(lon)를 포함하는 사전 형식입니다.
              위치 정보를 찾을 수 없는 경우 빈 리스트를 반환합니다.

    Raises:
        requests.exceptions.RequestException: API 요청 실패 시 발생합니다.
        AssertionError: 잘못된 매개변수 또는 파라미터 키 오류 시 발생합니다.
    """
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")

    input_data = parse_json_input(input_data)
    location = input_data.get("location", "")
    limit = int(input_data.get("limit", 1))

    params = {"appid": api_key, "units": "metric"}

    assert limit > 0, f"{limit}은 최소한 1개 이상의 정수여야 합니다."
    # 위치의 위도와 경도 찾기
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    geo_params = {"q": location, "limit": limit, "appid": api_key}

    try:
        assert set(geo_params.keys()) == {
            "q",
            "limit",
            "appid",
        }, "unknown parameter {data} in geo_params".format(
            data=set(geo_params.keys()) - {"q", "limit", "appid"}
        )
        logger.debug(f"geo_url: {geo_url}")
        logger.debug(f"geo_params: {geo_params}")
        geo_response = requests.get(geo_url, params=geo_params)
        geo_response.raise_for_status()
        geo_data = geo_response.json()
        logger.debug(f"geo_data: {geo_data}")
    except requests.exceptions.RequestException as e:
        logger.error("위치 정보를 가져오는데 실패했습니다.")
        return list()

    if not geo_data:
        logger.error("위치를 찾을 수 없습니다.")

    return geo_data


def get_current_datetime(anything: str = "") -> str:
    """
    현재 날짜와 시간을 반환합니다.

    Returns:
        str: 'YYYY-MM-DD HH:MM:SS' 형식의 현재 날짜와 시간.
    """
    logger.info(f"datetime.now(): {datetime.now()}")
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S (%A)")


def get_system_prompt(prompt):
    return prompt.format(**{"now": get_current_datetime()})
