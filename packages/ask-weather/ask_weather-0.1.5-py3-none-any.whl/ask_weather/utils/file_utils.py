import yaml
from ask_weather.utils.logger import get_logger
import json

logger = get_logger(__file__)


def load_prompt_template(prompt_path, name="template"):
    """YAML 파일에서 프롬프트 템플릿을 로드합니다."""
    try:
        with open(prompt_path, "r") as file:
            prompt_data = yaml.safe_load(file)
            return prompt_data[name]
    except Exception as e:
        logger.error(f"프롬프트 템플릿을 로드하는데 실패했습니다: {e}")


def parse_json_input(input_data: str):
    if isinstance(input_data, str):
        try:
            input_data = input_data.replace("True", "true")
            input_data = input_data.replace("False", "false")
            input_data = json.loads(input_data)
        except Exception as e:
            logger.error(f"{repr(input_data)}를 딕셔너리로 변환하는데 실패했습니다. {e}")

    return input_data
