import itertools
import time

from multiprocessing.dummy import Pool as Threadpool
from os.path import abspath, exists
from socket import *


MAX_SOCKETS = 10
SERVER_NAME = '10.12.1.244'
SERVER_PORT = 80


def main():
    pool = Threadpool(MAX_SOCKETS)

    f_path = abspath("passwords")
    if exists(f_path):
        with open("passwords") as f:
            # Yeah, this is a weird one.  zip_longest takes an unpacked list (*list_var).
            # We want n copies of a single (list_var * n) list because we're going to call n copies of the same iter.
            # In order to serialize n sockets.
            for words in itertools.zip_longest(*[f]*MAX_SOCKETS):

                attempts = []
                for w in words:
                    attempts.append(w.strip())

                send_payload(server_name, server_port)
    else:
        print("failed to find path")

    print("Stopping service ...\n")
    time.sleep(10)
    client_socket.close()
    print("Service stopped!")


def send_payload(payload):
    # Create a TCP client socket
    # (AF_INET is used for IPv4 protocols)
    # (SOCK_STREAM is used for TCP)
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((SERVER_NAME, SERVER_PORT))

    client_socket.send(payload.encode())
    client_socket.close()



# def send_by_byte(output: str, s: socket):
#     for i in range(0, len(output)):
#         s.send(output[i].encode())
#     #s.send('\r\n'.encode())
#
#     return


if __name__ == '__main__':
    main()
