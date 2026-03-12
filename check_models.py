import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load your key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Here are the models you can use for text generation:")
print("-" * 50)

# Loop through and print the actual names
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)