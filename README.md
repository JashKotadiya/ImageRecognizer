# Object-Recognizing-Robot - aka ARGUS
Inspiration
We wanted to create a system that bridges human language and robotic perception — something that can understand what you’re looking for and help you find it. From losing keys at home to searching for tools in a workspace, the idea of a robot that can visually locate objects based on a natural-language description felt both futuristic and genuinely useful. That’s how ARGUS was born — an intelligent vision assistant powered by AI.

What it does
ARGUS allows users to describe an object in natural language — like “a silver watch”, “my blue water bottle”, or “a set of keys” — and then uses a camera feed to look for it. The system processes live images through Google Gemini, identifies visible objects, and compares them to the user’s description with a match confidence score.

The goal is to integrate this capability into a mobile robot, enabling it to physically scan its environment and navigate toward the desired object. In future versions, ARGUS will combine computer vision, robotics, and natural language understanding to make object-finding both intuitive and autonomous.

How we built it
Frontend/UI: Built in Streamlit for a clean and interactive interface, supporting both webcam capture and photo upload.

Backend & AI: Uses Google’s Gemini 2.5 Flash model via the google-generativeai library for visual analysis and matching.

Environment Handling: .env + python-dotenv for secure API key management.

Image Processing: Pillow (PIL) for handling captured frames.

Future Robotics Integration: Will use Raspberry Pi / Arduino for movement and pathfinding, enabling the robot to actively search for and approach target objects.

Challenges we ran into
Getting Gemini to interpret vague or abstract object descriptions accurately.
Integrating AI-generated confidence scores with visual feedback in real time.
Handling environment variables across devices and operating systems (especially with Streamlit).
Designing the system architecture so that it can easily connect to a future robotic platform for movement and vision alignment.

Accomplishments that we're proud of
Built a working prototype that can visually recognize and evaluate real-world objects using a natural-language description.
Created a stable Streamlit interface that combines camera capture, image upload, and AI-powered detection.
Established a scalable framework ready for robotics integration.
Learned how to optimize prompts for more consistent Gemini responses.
What we learned
How to leverage multimodal AI models (like Gemini) for real-time computer vision tasks.

How to design a software pipeline that’s future-proof for robotic hardware.

The importance of prompt clarity and consistency when using generative AI for structured outputs.

How to use Streamlit for rapid prototyping of AI tools.

What's next for ARGUS
Integrate with a mobile robot that uses ultrasonic sensors or computer vision for navigation.

Implement object localization — drawing bounding boxes or heatmaps around detected items.

Add voice command input and audio feedback for a hands-free experience.

Train or fine-tune a model for specific object categories to improve accuracy.

Deploy on a Raspberry Pi or Jetson Nano for fully portable AI vision.

Built With
arduino
dotenv
gemini
opencv
pillow
python
rasberrypi
streamlit
