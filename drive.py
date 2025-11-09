#Start programming the actual movement of the robot.

# This code is for one motor
# Test this code on rpi
import RPi.GPIO as GPIO
import time

class DriveMotor:
    def __init__(self, IN1, IN2, ENA):
        # Define Motor Pins (example)
        self.IN1 = IN1
        self.IN2 = IN2
        self.ENA = ENA

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(IN1, GPIO.OUT)
        GPIO.setup(IN2, GPIO.OUT)
        GPIO.setup(ENA, GPIO.OUT)

        self.pwm = GPIO.PWM(ENA, 1000)  # PWM at 1kHz frequency
        self.pwm.start(0)  # Start PWM with 0% duty cycle

    def motor_forward(self, speed):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        self.pwm.ChangeDutyCycle(speed)

    def motor_backward(self, speed):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(speed)

    def motor_stop(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)

if __name__ == "__main__":   
    try:
        DriveMotor.motor_forward(80)  # Run forward at 80% speed
        time.sleep(3)
        DriveMotor.motor_backward(80)  # Run backward at 80% speed
        time.sleep(3)
        DriveMotor.motor_stop()
    finally:
        DriveMotor.pwm.stop()
        GPIO.cleanup()
