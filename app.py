import streamlit as st
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os
import cv2
import tempfile

# --- Load environment variables ---
load_dotenv()
apiKey = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=apiKey)

# --- Load Gemini model ---
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="Gemini Object Finder", layout="centered")
st.title("🎯 Gemini Object Recognition App")
st.write("Use your webcam to detect and identify objects using Gemini AI.")

# --- Input target description ---
targetObject = st.text_input("Describe the object you're looking for (e.g., 'red bottle', 'silver jewelry')")

# --- Webcam capture section ---
camera = st.camera_input("Capture Image")

if camera is not None and targetObject:
    st.write("Analyzing image...")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(camera.getvalue())
        img = Image.open(tmp.name)

    # --- Ask Gemini to describe and compare ---
    with st.spinner("Sending image to Gemini..."):
        description_response = model.generate_content([
            "Describe the main object(s) or living thing(s) you see in less than 10 words.",
            img
        ])
        match_response = model.generate_content([
            f"On a scale of 0–100, how much does this image match the description '{targetObject}'? "
            "Respond only with a percentage number.",
            img
        ])

    st.subheader("🔍 Gemini’s Description:")
    st.write(description_response.text)

    st.subheader("🎯 Match Confidence:")
    try:
        confidence = int(''.join(filter(str.isdigit, match_response.text)))
        st.progress(confidence / 100)
        st.write(f"**{confidence}% Match** with '{targetObject}'")
        if confidence > 75:
            st.success("✅ Likely a match!")
        else:
            st.warning("⚠️ Not a strong match.")
    except:
        st.write(match_response.text)
else:
    st.info("👆 Please describe your target and capture an image.")
