import os
from langchain_core.tools import tool
from dotenv import load_dotenv
from ask_weather.utils.logger import get_logger
from ask_weather.utils.file_utils import load_prompt_template
from ask_weather.tools import (
    get_weather,
    get_current_datetime,
    get_system_prompt,
    get_location,
)
import yaml
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.prompts import PromptTemplate

logger = get_logger(__file__)


class WeatherAgent:
    def __init__(
        self,
        env_path=".env",
        model="gpt-4o-mini",
        temperature=0,
        prompt_path="prompts/weather_agent_prompt.yaml",
        verbose=False,
        max_iterations=10,
        max_execution_time=100000,
        handle_parsing_errors=False,
        return_intermediate_steps=False,
    ):
        if os.path.isfile(env_path):
            load_dotenv(dotenv_path=env_path)
            logger.info(f"successfully set env file")
        else:
            logger.error(f"환경 변수 파일을 찾을 수 없습니다: {env_path}")
            raise FileNotFoundError(f"{env_path} 파일이 존재하지 않습니다. 올바른 위치를 설정해주세요.")

        self.prompt_template = load_prompt_template(prompt_path)
        self.system_prompt = load_prompt_template(prompt_path, "system_prompt")
        logger.info(f"프롬프트 템플릿 로드 완료: {prompt_path}")

        self.agent_executor = self.get_weather_agent(
            model,
            temperature,
            verbose=verbose,
            max_iterations=max_iterations,
            max_execution_time=max_execution_time,
            handle_parsing_errors=handle_parsing_errors,
            return_intermediate_steps=return_intermediate_steps,
        )
        logger.info("initialized WeatherAgent")

    def get_weather_agent(
        self,
        model="gpt-4o-mini",
        temperature=0,
        verbose=False,
        max_iterations=10,
        max_execution_time=100000,
        handle_parsing_errors=False,
        return_intermediate_steps=False,
    ):
        llm = ChatOpenAI(model=model, temperature=temperature)
        prompt = PromptTemplate.from_template(self.prompt_template)
        agent = create_react_agent(llm, [get_weather, get_location], prompt)
        return AgentExecutor(
            agent=agent,
            tools=[get_weather, get_location],
            verbose=verbose,
            max_iterations=max_iterations,
            max_execution_time=max_execution_time,
            handle_parsing_errors=handle_parsing_errors,
            return_intermediate_steps=return_intermediate_steps,
        )

    def query(self, input_query, retry_count=1):
        for i in range(retry_count):
            try:
                response = self.agent_executor.invoke(
                    {
                        "input": input_query,
                        "system_prompt": get_system_prompt(self.system_prompt),
                    }
                )
                logger.info(f"response: {response}")
                return response["output"]
            except Exception as e:
                logger.error(f"Trial : {retry_count}, {e}")
        # TODO 실패 원인 케이스 정리
        return "날씨 정보를 가져오는데 실패했습니다."
