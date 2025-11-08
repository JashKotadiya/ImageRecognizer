import google.generativeai as genai
from PIL import Image

# Configure with your API key
genai.configure(api_key="AIzaSyCJmPxUv36qoucvBFQ7-TWDW8kGjRkc_Go")

# Load the multimodal model
model = genai.GenerativeModel("gemini-2.5-flash")

# Open an image (any supported format)
img = Image.open("C:/Users/Tanda/Downloads/download.jpg")

# Ask the model about it
response = model.generate_content(["What is in this image? Only give one word", img])

print(response.text)
