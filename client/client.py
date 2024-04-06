import socket


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = None
        self.eof_token = None

    def receive_message_ending_with_token(self, active_socket, buffer_size, eof_token):
        """
        Same implementation as in receive_message_ending_with_token() in server.py
        A helper method to receives a bytearray message of arbitrary size sent on the socket.
        This method returns the message WITHOUT the eof_token at the end of the last packet.
        :param active_socket: a socket object that is connected to the server
        :param buffer_size: the buffer size of each recv() call
        :param eof_token: a token that denotes the end of the message.
        :return: a bytearray message with the eof_token stripped from the end.
        """
        raise NotImplementedError('Your implementation here.')

    def initialize(self, host, port):
        """
        1) Creates a socket object and connects to the server.
        2) receives the random token (10 bytes) used to indicate end of messages.
        3) Displays the current working directory returned from the server (output of get_working_directory_info() at the server).
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param host: the ip address of the server
        :param port: the port number of the server
        :return: the created socket object
        :return: the eof_token
        """

        # print('Connected to server at IP:', host, 'and Port:', port)

        # print('Handshake Done. EOF is:', eof_token)

        raise NotImplementedError('Your implementation here.')



    def issue_cd(self, command_and_arg, client_socket, eof_token):
        """
        Sends the full cd command entered by the user to the server. The server changes its cwd accordingly and sends back
        the new cwd info.
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param command_and_arg: full command (with argument) provided by the user.
        :param client_socket: the active client socket object.
        :param eof_token: a token to indicate the end of the message.
        """
        raise NotImplementedError('Your implementation here.')

    def issue_mkdir(self, command_and_arg, client_socket, eof_token):
        """
        Sends the full mkdir command entered by the user to the server. The server creates the sub directory and sends back
        the new cwd info.
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param command_and_arg: full command (with argument) provided by the user.
        :param client_socket: the active client socket object.
        :param eof_token: a token to indicate the end of the message.
        """
        raise NotImplementedError('Your implementation here.')

    def issue_rm(self, command_and_arg, client_socket, eof_token):
        """
        Sends the full rm command entered by the user to the server. The server removes the file or directory and sends back
        the new cwd info.
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param command_and_arg: full command (with argument) provided by the user.
        :param client_socket: the active client socket object.
        :param eof_token: a token to indicate the end of the message.
        """
        raise NotImplementedError('Your implementation here.')

    def issue_ul(self, command_and_arg, client_socket, eof_token):
        """
        Sends the full ul command entered by the user to the server. Then, it reads the file to be uploaded as binary
        and sends it to the server. The server creates the file on its end and sends back the new cwd info.
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param command_and_arg: full command (with argument) provided by the user.
        :param client_socket: the active client socket object.
        :param eof_token: a token to indicate the end of the message.
        """
        raise NotImplementedError('Your implementation here.')

    def issue_dl(self, command_and_arg, client_socket, eof_token):
        """
        Sends the full dl command entered by the user to the server. Then, it receives the content of the file via the
        socket and re-creates the file in the local directory of the client. Finally, it receives the latest cwd info from
        the server.
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param command_and_arg: full command (with argument) provided by the user.
        :param client_socket: the active client socket object.
        :param eof_token: a token to indicate the end of the message.
        :return:
        """
        raise NotImplementedError('Your implementation here.')

    def issue_info(self,command_and_arg, client_socket, eof_token):
        """
        Sends the full info command entered by the user to the server. The server reads the file and sends back the size of
        the file.
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param command_and_arg: full command (with argument) provided by the user.
        :param client_socket: the active client socket object.
        :param eof_token: a token to indicate the end of the message.
        :return: the size of file in string
        """
        raise NotImplementedError('Your implementation here.')


    def issue_mv(self,command_and_arg, client_socket, eof_token):
        """
        Sends the full mv command entered by the user to the server. The server moves the file to the specified directory and sends back
        the updated. This command can also act as renaming the file in the same directory. 
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param command_and_arg: full command (with argument) provided by the user.
        :param client_socket: the active client socket object.
        :param eof_token: a token to indicate the end of the message.
        """
        raise NotImplementedError('Your implementation here.')

    def start(self):
        """
        1) Initialization
        2) Accepts user input and issue commands until exit.
        """
        # initialize

        raise NotImplementedError('Your implementation here.')
        # while True:
            # get user input

            # call the corresponding command function or exit

        # print('Exiting the application.')


def run_client():
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server

    client = Client(HOST, PORT)
    client.start()


if __name__ == '__main__':
    run_client()
