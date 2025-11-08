from google import genai

#print("Hello world")

# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(api_key="AIzaSyCJmPxUv36qoucvBFQ7-TWDW8kGjRkc_Go")

response = client.models.generate_content(
    model="gemini-2.5-flash", contents="Explain how AI works in a few words"
)
print(response.text)