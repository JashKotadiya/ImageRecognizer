import socket

def request_capture(server_ip, port, save_as="received.jpg"):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, port))

    # Send capture request
    s.sendall(b"capture\n")

    # Receive filesize
    filesize = int(s.recv(16).decode().strip())
    if filesize == 0:
        print("Server failed to capture image.")
        s.close()
        return

    bytes_received = 0
    with open(save_as, "wb") as f:
        while bytes_received < filesize:
            chunk = s.recv(min(4096, filesize - bytes_received))
            if not chunk:
                break
            f.write(chunk)
            bytes_received += len(chunk)

    print(f"Image received and saved as {save_as}")
    s.close()

# if __name__ == "__main__":
#     request_capture("172.31.192.171", 5001)
