import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


async def stream_response(prompt: str):
    response = model.generate_content(prompt,stream=True)
    for chunk in response:
        if chunk.text:
            yield chunk.text


