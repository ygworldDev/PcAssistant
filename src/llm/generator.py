import os
from abc import ABC, abstractmethod
from src.common.constants import LLMType
from huggingface_hub import InferenceClient
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

class Generator(ABC):
    def __init__(self, generator) -> None:
        self.generator = generator

    @abstractmethod
    def generate(self, user_message):
        pass
    
# class OpenAI(Generator):
#     def __init__(self):
#         openai_api_key = os.getenv("OPENAI_API_KEY")
#         print(openai_api_key)
#         headers = {"Content-Type": "application/json", "Accept": "application/json"}
#         self.client = InferenceClient(token=openai_api_key, model="gpt-4", headers=headers)
#         # self.client = InferenceClient(api_key=open
#         super().__init__(OpenAI)
        
#     def generate(self, prompt):
#         print(f"OpenAI generate : {prompt}")
#         messages = [{"role": "user", "content": "What is the capital of France?"}]
#         temprature = 0.5
#         max_tokens = 100

#         response = self.client.chat_completion(messages=messages, temperature=temprature, max_tokens=max_tokens)
#         return response
    
class Gpt4(Generator):
    def __init__(self):
        super().__init__(Gpt4)

    def generate(self, messages: list):
        print(f"Gpt4 generate...")
        # messages=[
        #     {"role": "system", "content": "You are a helpful assistant."},
        #     {"role": "user","content": user_message}
        # ]

        # openai_api_key = os.getenv("OPENAI_API_KEY")

        self.client = OpenAI()

        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )

        response = completion.choices[0].message
        print(f"received_messaged : {response}")
        return response.content
    

class Llama3(Generator):
    def __init__(self):
        super().__init__(Llama3)

    def generate(self, user_message):
        print(f"Llama3 generate...")
        return 'Llama3'    
    
def create_generator(llm_type) -> Generator:
    if llm_type == LLMType.GPT_4:
        generator =  Gpt4()
    elif llm_type == LLMType.LLAMA3:
        generator = Llama3()
    else:
        return None
    return generator