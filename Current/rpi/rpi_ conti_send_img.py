import subprocess
import socket
import os
from PIL import Image

def capture_image(input_filename="temp_image.jpg", output_filename="rotated_image.jpg"):
    try:
        subprocess.run(["rpicam-jpeg", "-o", input_filename, "-t 10"], check=True)
        img = Image.open(input_filename)
        img_rotated = img.rotate(180)
        img_rotated.save(output_filename)
        os.remove(input_filename)
        return output_filename
    except subprocess.CalledProcessError as e:
        print(f"Failed to capture image: {e}")
        return None

def send_file(conn, filename):
    filesize = os.path.getsize(filename)
    conn.sendall(f"{filesize:<16}".encode())
    with open(filename, "rb") as f:
        while True:
            bytes_read = f.read(4096)
            if not bytes_read:
                break
            conn.sendall(bytes_read)

def server_loop(host="0.0.0.0", port=5001):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)
    print(f"Server listening on {host}:{port}")

    try:
        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")

            try:
                while True:
                    # Receive client request command (simple protocol)
                    data = conn.recv(1024).decode().strip()
                    if not data:
                        break

                    if data.lower() == "capture":
                        print("Capture request received.")
                        img_file = capture_image()
                        if img_file:
                            send_file(conn, img_file)
                            print("Image sent.")
                        else:
                            # Send zero filesize to indicate failure
                            conn.sendall(f"{0:<16}".encode())
                    elif data.lower() == "exit":
                        print("Exit request received. Closing connection.")
                        break
                    else:
                        print(f"Unknown command: {data}")

            finally:
                conn.close()
                print("Connection closed.")

    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        s.close()

if __name__ == "__main__":
    server_loop()