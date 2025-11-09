import socket

def send_command(command, host='172.31.192.171', port=65432):
    """
    Send a single command to the robot server.
    
    :param command: Command as string ('1', '2', '3', '4', or 'stop')
    :param host: Server hostname or IP address
    :param port: Server port number
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(command.encode('utf-8'))
        data = s.recv(1024)
        print('Received from server:', data.decode('utf-8'))

if __name__ == '__main__':
    print("Robot Control Client")
    print("Commands: 1 = forward, 2 = backward, 3 = left, 4 = right, stop = stop motors, q = quit")
    while True:
        cmd = input("Enter command: ").strip()
        if cmd == 'q':
            break
        elif cmd in ['1', '2', '3', '4', 'stop']:
            send_command(cmd)
        else:
            print("Invalid command.")
