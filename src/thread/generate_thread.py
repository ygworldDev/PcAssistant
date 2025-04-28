from PyQt5.QtCore import QThread, pyqtSignal
from src.llm.generator import Generator
from src.common.constants import Role 

class GenerateThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self, generator:Generator, chat_history:list, image:str):
        QThread.__init__(self)
        self.generator = generator
        self.chat_history = chat_history
        self.image = image

    def run(self):
        if self.image:
            last_item = self.chat_history[-1]
            if last_item["role"] != Role.USER:
                raise ValueError("The last item in chat history is not USER")
            
            image_message = [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": last_item["content"]
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{self.image}"
                            }
                        }
                    ]
                }
            ]
            received_message = self.generator.generate(image_message)
        else:
            received_message = self.generator.generate(self.chat_history)

        self.signal.emit(received_message)   