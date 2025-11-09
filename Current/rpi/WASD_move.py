# Python Script for Two DC Motors (L298N) using WASD for Real-Time Control
# (Corrected direction logic)

import RPi.GPIO as GPIO
import time
import sys
import tty
import termios

# --- Motor 1 (Left Motor) Setup ---
in1 = 24  # Motor 1 Direction Pin 1
in2 = 23  # Motor 1 Direction Pin 2
en1 = 25  # Motor 1 Speed (PWM)

# --- Motor 2 (Right Motor) Setup ---
in3 = 16  # Motor 2 Direction Pin 1
in4 = 20  # Motor 2 Direction Pin 2
en2 = 21  # Motor 2 Speed (PWM)

DEFAULT_SPEED = 100 # Default PWM duty cycle (50%)

# Function to capture a single keypress without pressing Enter
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Function to set both motors' directions
def set_motors(motor1_dir1, motor1_dir2, motor2_dir1, motor2_dir2):
    GPIO.output(in1, motor1_dir1)
    GPIO.output(in2, motor1_dir2)
    GPIO.output(in3, motor2_dir1)
    GPIO.output(in4, motor2_dir2)

# --- Setup GPIO ---
GPIO.setmode(GPIO.BCM)

# Motor 1 Setup
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en1, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)

# Motor 2 Setup
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(en2, GPIO.OUT)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)

# Setup PWM
p1 = GPIO.PWM(en1, 1000)
p2 = GPIO.PWM(en2, 1000)

p1.start(DEFAULT_SPEED)
p2.start(DEFAULT_SPEED)

print("\n")
print("----------------------------------------------------------")
print("WASD Real-Time Motor Control (Corrected Logic)")
print("----------------------------------------------------------")
print("W: Forward")
print("S: Backward")
print("A: Turn Left")
print("D: Turn Right")
print("SPACE: Stop")
print("Q/E: Exit Program")
print("----------------------------------------------------------")
print(f"Default Speed: {DEFAULT_SPEED}%")
print("Press a key to begin...")

try:
    while True:
        key = getch()
        
        if key == 'w' or key == 'W':
            # FORWARD: M1 Bwd, M2 Bwd (Switched from original code)
            # This makes the motors spin in the correct direction for forward movement
            set_motors(GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.HIGH)
            print("Action: FORWARD")
            
        elif key == 's' or key == 'S':
            # BACKWARD: M1 Fwd, M2 Fwd (Switched from original code)
            # This makes the motors spin in the correct direction for backward movement
            set_motors(GPIO.HIGH, GPIO.LOW, GPIO.HIGH, GPIO.LOW)
            print("Action: BACKWARD")
            
        elif key == 'a' or key == 'A':
            # TURN LEFT: M1 Fwd, M2 Bwd (Switched M1 and M2 logic from original code)
            # To turn left, the Left motor should go Forward and the Right motor Backward (or vice-versa for pivot)
            # M1 (Left) is IN1/IN2. M2 (Right) is IN3/IN4.
            set_motors(GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH)
            print("Action: TURN LEFT")
            
        elif key == 'd' or key == 'D':
            # TURN RIGHT: M1 Bwd, M2 Fwd (Switched M1 and M2 logic from original code)
            # To turn right, the Left motor should go Backward and the Right motor Forward (or vice-versa for pivot)
            set_motors(GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW)
            print("Action: TURN RIGHT")
            
        elif key == ' ': # Spacebar
            # Stop: M1 Stop, M2 Stop
            set_motors(GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW)
            print("Action: STOP")
            
        elif key in ('q', 'Q', 'e', 'E', '\x03'): # 'e', 'q', or Ctrl+C (\x03)
            set_motors(GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW)
            print("\nExiting program.")
            break
            
except Exception as e:
    print(f"\nAn error occurred: {e}")

finally:
    GPIO.cleanup()
    print("GPIO Clean up complete.")
