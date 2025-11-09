import RPi.GPIO as GPIO
import socket
import time

# Motor pins setup
in1 = 16  # Motor 1 Direction Pin 1 (Left motor)
in2 = 20  # Motor 1 Direction Pin 2
en1 = 21  # Motor 1 Speed (PWM)

in3 = 24  # Motor 2 Direction Pin 1 (Right motor)
in4 = 23  # Motor 2 Direction Pin 2
en2 = 25  # Motor 2 Speed (PWM)

DEFAULT_SPEED = 80  # PWM duty cycle (0-100%)

def set_motors(motor1_dir1, motor1_dir2, motor2_dir1, motor2_dir2):
    GPIO.output(in1, motor1_dir1)
    GPIO.output(in2, motor1_dir2)
    GPIO.output(in3, motor2_dir1)
    GPIO.output(in4, motor2_dir2)

def stop_motors():
    set_motors(GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.LOW)

def main():
    GPIO.setmode(GPIO.BCM)
  
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    GPIO.setup(en1, GPIO.OUT)
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)

    GPIO.setup(in3, GPIO.OUT)
    GPIO.setup(in4, GPIO.OUT)
    GPIO.setup(en2, GPIO.OUT)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

    p1 = GPIO.PWM(en1, 100)
    p2 = GPIO.PWM(en2, 100)

    p1.start(DEFAULT_SPEED)
    p2.start(DEFAULT_SPEED)

    HOST = '0.0.0.0'  # Listen on all interfaces
    PORT = 65432      # Port number

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Server listening on {HOST}:{PORT}')

        try:
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f'Connected by {addr}')
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        command = data.decode('utf-8').strip()
                        print(f'Received command: {command}')

                        if command == '1':  # Forward (2 seconds)
                            set_motors(GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.HIGH)
                            conn.sendall(b'Moving forward for 2 seconds\n')
                            time.sleep(2)
                            stop_motors()

                        elif command == '2':  # Backward (2 seconds)
                            set_motors(GPIO.HIGH, GPIO.LOW, GPIO.HIGH, GPIO.LOW)
                            conn.sendall(b'Moving backward for 2 seconds\n')
                            time.sleep(2)
                            stop_motors()

                        elif command == '3':  # Left (0.6 seconds)
                            set_motors(GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH)
                            conn.sendall(b'Turning left for 0.6 seconds\n')
                            time.sleep(0.6)
                            stop_motors()

                        elif command == '4':  # Right (0.6 seconds)
                            set_motors(GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW)
                            conn.sendall(b'Turning right for 0.6 seconds\n')
                            time.sleep(0.8)
                            stop_motors()

                        elif command == 'stop':  # Stop immediately
                            stop_motors()
                            conn.sendall(b'Stopped\n')

                        else:
                            conn.sendall(b'Unknown command\n')

                    stop_motors()  # Stop motors when connection closes

        except KeyboardInterrupt:
            print("Server interrupted by user")

        finally:
            stop_motors()
            p1.stop()
            p2.stop()
            GPIO.cleanup()
            print("Cleaned up GPIO and stopped PWM")

if __name__ == '__main__':
    main()
