#Start programming the actual movement of the robot.

# This code is for one motor
# Test this code on rpi
import RPi.GPIO as GPIO
import time

class DriveMotor:
    def __init__(self, IN1, IN2, EN1, IN3, IN4, EN2):
        # Define Motor Pins (example)
        self.IN1 = IN1
        self.IN2 = IN2
        self.EN1 = EN1
        self.IN3 = IN3
        self.IN4 = IN4
        self.EN2 = EN2

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(IN1, GPIO.OUT)
        GPIO.setup(IN2, GPIO.OUT)
        GPIO.setup(EN1, GPIO.OUT)
        GPIO.setup(IN2, GPIO.OUT)
        GPIO.setup(IN3, GPIO.OUT)
        GPIO.setup(EN2, GPIO.OUT)

        self.pwm = GPIO.PWM(EN1, 100)  # PWM at 1kHz frequency
        self.pwm1 = GPIO.PWM(EN2, 100)
        self.pwm.start(0)  # Start PWM with 0% duty cycle
        self.pwm1.start(0)

    def forward(self, time1):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        time.sleep(time1)

    def reverse(self, time1):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        time.sleep(time1)
    
    def left(self):
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
    
    def right(self):
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)

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
    driveMotor = DriveMotor(16,20,21)
    driveMotor2 = DriveMotor(24,23,25) #
    try:
        driveMotor.motor_forward(80)
        driveMotor2.motor_forward(80) 
        time.sleep(3)
        driveMotor.motor_backward(80)
        driveMotor2.motor_backward(80)
        time.sleep(3)  
        driveMotor.motor_stop()
        driveMotor2.motor_stop()
        
    finally:
        driveMotor.pwm.stop()
        driveMotor2.pwm.stop()
        GPIO.cleanup()

   
    
