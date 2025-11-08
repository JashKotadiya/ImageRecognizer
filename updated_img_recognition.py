#Have Infrared sensor, along with a camera. We use computer vision (open cv)
#   Use the infrared sensor to check whether we are within 2 feet of a distance
#   stop the motor
#   Capture a frame from the camera
#   Send said frame to Gemini
#   Gemini identifies image, and provides a description
#   Send description to Gemini, along with user description
#   If the match is more than 85%, then the speaker blares (or something else happens)
#   Else, the robot will turn in some way, and continue