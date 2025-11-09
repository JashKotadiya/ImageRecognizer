#Start programming the actual movement of the robot.

# This code is for one motor
import RPi.GPIO as GPIO
import time

# Define Motor Pins (example)
IN1 = 17
IN2 = 18
ENA = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)

pwm = GPIO.PWM(ENA, 1000)  # PWM at 1kHz frequency
pwm.start(0)  # Start PWM with 0% duty cycle

def motor_forward(speed):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(speed)

def motor_backward(speed):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    pwm.ChangeDutyCycle(speed)

def motor_stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    pwm.ChangeDutyCycle(0)

try:
    motor_forward(80)  # Run forward at 80% speed
    time.sleep(3)
    motor_backward(80)  # Run backward at 80% speed
    time.sleep(3)
    motor_stop()
finally:
    pwm.stop()
    GPIO.cleanup()
