"""Fail a real localhost connection once, then make the same command succeed."""

import os
import socket
import subprocess
import sys


HOST = "127.0.0.1"
PORT = int(os.environ["LAB_PORT"])


def serve():
    with socket.socket() as listener:
        listener.bind((HOST, PORT))
        listener.listen(1)
        listener.settimeout(10)
        with listener.accept()[0] as connection:
            connection.sendall(b"ready\n")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        serve()
    else:
        try:
            with socket.create_connection((HOST, PORT), timeout=2) as connection:
                if connection.recv(64) != b"ready\n":
                    raise RuntimeError("unexpected local service response")
        except ConnectionRefusedError:
            subprocess.Popen(
                [sys.executable, __file__, "serve"],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            raise
        print("Local service responded on the unchanged command.")
