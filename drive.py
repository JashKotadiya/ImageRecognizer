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

        self.pwm = GPIO.PWM(ENA, 100)  # PWM at 1kHz frequency
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

   
    
