import socket
import os

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
        
        msg = bytearray()
        while True:
                packet = active_socket.recv(buffer_size)
                
                if packet[-10:] == eof_token.encode():
                    msg += packet[:-10]
                    break
                msg += packet
                

        return msg

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

                self.client_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((host, port))
                print('Connected to server at IP:', host, 'and Port:', port)

                self.eof_token=self.client_socket.recv(1024).decode()
                print('Handshake Done. EOF is:', self.eof_token)


                cwd=self.receive_message_ending_with_token(self.client_socket,1024,self.eof_token)
                print(f'current working directory of server : {cwd.decode()}')



                return self.client_socket,self.eof_token



    def issue_cd(self, command_and_arg, client_socket, eof_token):
        """
        Sends the full cd command entered by the user to the server. The server changes its cwd accordingly and sends back
        the new cwd info.
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param command_and_arg: full command (with argument) provided by the user.
        :param client_socket: the active client socket object.
        :param eof_token: a token to indicate the end of the message.
        """
        command_and_arg+=eof_token
    
        self.client_socket.sendall(command_and_arg.encode())

        new_dir=self.receive_message_ending_with_token(client_socket,1024,eof_token)
        print(f' New working directory changed to : {new_dir.decode()}')

        


    def issue_mkdir(self, command_and_arg, client_socket, eof_token):
        """
        Sends the full mkdir command entered by the user to the server. The server creates the sub directory and sends back
        the new cwd info.
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param command_and_arg: full command (with argument) provided by the user.
        :param client_socket: the active client socket object.
        :param eof_token: a token to indicate the end of the message.
        """
        command_and_arg+=eof_token
        client_socket.sendall(command_and_arg.encode())

        new_dir=self.receive_message_ending_with_token(client_socket,1024,eof_token)
        print(f' {new_dir.decode()}')
     


    def issue_rm(self, command_and_arg, client_socket, eof_token):
        """
        Sends the full rm command entered by the user to the server. The server removes the file or directory and sends back
        the new cwd info.
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param command_and_arg: full command (with argument) provided by the user.
        :param client_socket: the active client socket object.
        :param eof_token: a token to indicate the end of the message.
        """
        command_and_arg+=eof_token
        client_socket.sendall(command_and_arg.encode())

        remove_dir=self.receive_message_ending_with_token(client_socket,1024,eof_token)
        print(f' {remove_dir.decode()}')
  

    def issue_ul(self, command_and_arg, client_socket, eof_token):
        """
        Sends the full ul command entered by the user to the server. Then, it reads the file to be uploaded as binary
        and sends it to the server. The server creates the file on its end and sends back the new cwd info.
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param command_and_arg: full command (with argument) provided by the user.
        :param client_socket: the active client socket object.
        :param eof_token: a token to indicate the end of the message.
        """
        file_name=command_and_arg.split()[1]
        command_and_arg+=eof_token
        client_socket.sendall(command_and_arg.encode()) #Sending command

        current_working_directory=os.getcwd()
        file_path=current_working_directory+'/'+file_name
        with open(file_path, 'rb') as f:
                file_content = f.read()

        file_content+=eof_token.encode()
        client_socket.sendall(file_content) #Sending file

        ack_msg=self.receive_message_ending_with_token(client_socket,1024,eof_token) #Recieved once file succesffully uploaded
        print(f' {ack_msg.decode()}')



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
        file_name=command_and_arg.split()[1]
        command_and_arg+=eof_token
        client_socket.sendall(command_and_arg.encode())

        file_content=self.receive_message_ending_with_token(client_socket,1024,eof_token)
        
        file_path=os.getcwd()+'/'+file_name
        with open(file_path, 'wb') as f:
            f.write(file_content)
        print(f'Downloaded file {file_name}')    



 

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
        command_and_arg+=eof_token
        client_socket.sendall(command_and_arg.encode())

        msg=self.receive_message_ending_with_token(client_socket,1024,eof_token)
        print(f' {msg.decode()}')



    def issue_mv(self,command_and_arg, client_socket, eof_token):
        """
        Sends the full mv command entered by the user to the server. The server moves the file to the specified directory and sends back
        the updated. This command can also act as renaming the file in the same directory. 
        Use the helper method: receive_message_ending_with_token() to receive the message from the server.
        :param command_and_arg: full command (with argument) provided by the user.
        :param client_socket: the active client socket object.
        :param eof_token: a token to indicate the end of the message.
        """
        command_and_arg+=eof_token
        client_socket.sendall(command_and_arg.encode())

        msg=self.receive_message_ending_with_token(client_socket,1024,eof_token)
        print(f' {msg.decode()}')

        

    

    def start(self):
        """
        1) Initialization
        2) Accepts user input and issue commands until exit.
        """
        client_socket,eof_token=self.initialize(self.host,self.port)
       
        while True:
            command = input('Enter your input command: ')
            str=command.split()[0]
            match str:
                case "cd":
                    self.issue_cd(command,client_socket,eof_token)

                case "mkdir":
                    self.issue_mkdir(command,client_socket,eof_token)

                case "rm":
                    self.issue_rm(command,client_socket,eof_token)
                
                case "mv":
                    self.issue_mv(command,client_socket,eof_token)

                case "dl":
                    self.issue_dl(command,client_socket,eof_token)

                case "ul":
                    self.issue_ul(command,client_socket,eof_token)

                case "info":
                    self.issue_info(command,client_socket,eof_token)

                case "exit":
                    
                    client_socket.sendall((command+eof_token).encode())
                    print("Exiting the system")
                    break
                case _:
                    print("Enter a valid command")

            cwd=self.receive_message_ending_with_token(client_socket,1024,eof_token) ## Display current directory info
            print(f'current working directory of server : {cwd.decode()}')

        print('Exiting the application.')
        self.client_socket.close()


def run_client():
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server

    client = Client(HOST, PORT)
    client.start()


if __name__ == '__main__':
    run_client()
