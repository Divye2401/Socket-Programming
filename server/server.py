import socket
import random
from threading import Thread
import os
import shutil
from pathlib import Path
import time

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = None

    def start(self):
        """
        1) Create server, bind and start listening.
        2) Accept clinet connections and serve the requested commands.

        Note: Use ClientThread for each client connection.
        """
            # Create a socket

            # Bind the socket to the specified address and port

            # Listen for incoming connections

            # print(f"Server listening on {self.host}:{self.port}")

            # while True:
            # Accept incoming connections
            # print(f"Accepted connection from {client_address}")
            # send random eof token

            # try:
            #     # Handle the client requests using ClientThread
            # except Exception as e:
            #     print(f"Error: {e}")
            # finally:
            #     print("Connection closed.")
            #     client_socket.close()

        raise NotImplementedError("Your implementation here.")




    def get_working_directory_info(self, working_directory):
        """
        Creates a string representation of a working directory and its contents.
        :param working_directory: path to the directory
        :return: string of the directory and its contents.
        """
        dirs = "\n-- " + "\n-- ".join(
            [i.name for i in Path(working_directory).iterdir() if i.is_dir()]
        )
        files = "\n-- " + "\n-- ".join(
            [i.name for i in Path(working_directory).iterdir() if i.is_file()]
        )
        dir_info = f"Current Directory: {working_directory}:\n|{dirs}{files}"
        return dir_info

    def generate_random_eof_token(self):
        """Helper method to generates a random token that starts with '<' and ends with '>'.
        The total length of the token (including '<' and '>') should be 10.
        Examples: '<1f56xc5d>', '<KfOVnVMV>'
        return: the generated token.
        """
        raise NotImplementedError("Your implementation here.")

    def receive_message_ending_with_token(self, active_socket, buffer_size, eof_token):
        """
        Same implementation as in receive_message_ending_with_token() in client.py
        A helper method to receives a bytearray message of arbitrary size sent on the socket.
        This method returns the message WITHOUT the eof_token at the end of the last packet.
        :param active_socket: a socket object that is connected to the server
        :param buffer_size: the buffer size of each recv() call
        :param eof_token: a token that denotes the end of the message.
        :return: a bytearray message with the eof_token stripped from the end.
        """
        raise NotImplementedError("Your implementation here.")

    def handle_cd(self, current_working_directory, new_working_directory):
        """
        Handles the client cd commands. Reads the client command and changes the current_working_directory variable
        accordingly. Returns the absolute path of the new current working directory.
        :param current_working_directory: string of current working directory
        :param new_working_directory: name of the sub directory or '..' for parent
        :return: absolute path of new current working directory
        """
        raise NotImplementedError("Your implementation here.")

    def handle_mkdir(self, current_working_directory, directory_name):
        """
        Handles the client mkdir commands. Creates a new sub directory with the given name in the current working directory.
        :param current_working_directory: string of current working directory
        :param directory_name: name of new sub directory
        """
        raise NotImplementedError("Your implementation here.")

    def handle_rm(self, current_working_directory, object_name):
        """
        Handles the client rm commands. Removes the given file or sub directory. Uses the appropriate removal method
        based on the object type (directory/file).
        :param current_working_directory: string of current working directory
        :param object_name: name of sub directory or file to remove
        """
        raise NotImplementedError("Your implementation here.")

    def handle_ul(
        self, current_working_directory, file_name, service_socket, eof_token
    ):
        """
        Handles the client ul commands. First, it reads the payload, i.e. file content from the client, then creates the
        file in the current working directory.
        Use the helper method: receive_message_ending_with_token() to receive the message from the client.
        :param current_working_directory: string of current working directory
        :param file_name: name of the file to be created.
        :param service_socket: active socket with the client to read the payload/contents from.
        :param eof_token: a token to indicate the end of the message.
        """
        raise NotImplementedError("Your implementation here.")

    def handle_dl(
        self, current_working_directory, file_name, service_socket, eof_token
    ):
        """
        Handles the client dl commands. First, it loads the given file as binary, then sends it to the client via the
        given socket.
        :param current_working_directory: string of current working directory
        :param file_name: name of the file to be sent to client
        :param service_socket: active service socket with the client
        :param eof_token: a token to indicate the end of the message.
        """
        raise NotImplementedError("Your implementation here.")

    def handle_info(self,current_working_directory, file_name):
        """
        Handles the client info commands. Reads the size of a given file. 
        :param current_working_directory: string of current working directory
        :param file_name: name of sub directory or file to remove
        """
        raise NotImplementedError('Your implementation here.')
    
    def handle_mv(self,current_working_directory, file_name, destination_name):
        """
        Handles the client mv commands. First, it looks for the file in the current directory, then it moves or renames 
        to the destination file depending on the nature of the request.
        :param current_working_directory: string of current working directory
        :param file_name: name of the file tp be moved / renamed
        :param destination_name: destination directory or new filename
        """
        raise NotImplementedError('Your implementation here.')


class ClientThread(Thread):
    def __init__(self, server: Server, service_socket: socket.socket, address: str):
        Thread.__init__(self)
        self.server_obj = server
        self.service_socket = service_socket
        self.address = address

    def run(self):
        # print ("Connection from : ", self.address)
        raise NotImplementedError("Your implementation here.")

        # establish working directory

        # send the current dir info

        # while True:
        # get the command and arguments and call the corresponding method

        # sleep for 1 second

        # send current dir info

        # print('Connection closed from:', self.address)


def run_server():
    HOST = "127.0.0.1"
    PORT = 65432

    server = Server(HOST, PORT)
    server.start()


if __name__ == "__main__":
    run_server()
