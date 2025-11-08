import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os

load_dotenv()
apiKey = os.getenv("GOOGLE_API_KEY")

# Configure with your API key
genai.configure(api_key=apiKey)

# Load the multimodal model
model = genai.GenerativeModel("gemini-2.5-flash")

# Open an image (any supported format)
img = Image.open(r"C:\Users\kirkw\My Files\Personal\jawStarePfp.jpg")

# Ask the model about it
response = model.generate_content(["What is in this image? Only give one word", img])

print(response.text)
