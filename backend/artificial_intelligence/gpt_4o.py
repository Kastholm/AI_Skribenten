import os
from dotenv import load_dotenv
from openai import OpenAI

class gpt4o():

    def __init__(self):
        load_dotenv()
        self.gpt_key = os.getenv("GPT_KEY")
        if self.gpt_key:
            self.client = OpenAI(
                api_key=self.gpt_key,
            )
        else:
            print("None or not usable API key provided")

    def send_prompt(self, element, prompt, model="gpt-4o-mini"):
        if self.client:
            try: 
                if element == "Text":
                    response = self.client.responses.create(
                        model=model,
                        instructions="You are awesome",
                        input=prompt,
                    )
                    return response.output_text
                elif element == "Image":
                    response = self.client.images.generate(
                        model="dall-e-3",
                        prompt=prompt,
                        n=1,
                        size="1024x1024"
                    )
                    return response
            except Exception as e:
                print(f"Error: {e}")
        else:
            print("No client available")


            '''
            Hent site desc, vis på frontend. Denne sendes videre til artikel skrivning.
            
            '''