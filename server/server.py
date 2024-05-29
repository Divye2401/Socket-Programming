import socket
import random
from threading import Thread
import os
import shutil
from pathlib import Path
import time
import string

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



                self.server_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
                self.server_socket.bind((self.host, self.port))
                self.server_socket.listen()

                print(f"Server listening on {self.host}:{self.port}")
                
                while True:
                    client_socket, client_address = self.server_socket.accept()
                    print(f"Accepted connection from {client_address}")
                    eof_token = self.generate_random_eof_token()
                    client_socket.sendall(eof_token.encode())
                    
                    try:
                        
                        client_thread = ClientThread(self,client_socket,client_address,eof_token)
                        client_thread.start()
                        client_thread.join()
                    except Exception as e:
                        print(f"Error: {e}")
                    finally:
                        print("Connection closed.")
                        client_socket.close()

           

        




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

     #   print(dirs)
     #   print(files)
        dir_info = f"Current Directory: {working_directory}:\n|{dirs}{files}"
        return dir_info

    def generate_random_eof_token(self):
        """Helper method to generates a random token that starts with '<' and ends with '>'.
        The total length of the token (including '<' and '>') should be 10.
        Examples: '<1f56xc5d>', '<KfOVnVMV>'
        return: the generated token.
        """
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k = 8))
        token='<'+str(random_str)+'>'
        
        return token
        

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
        msg = bytearray()
        while True:
                packet = active_socket.recv(buffer_size)
                if packet[-10:] == eof_token.encode():
                    msg += packet[:-10]
                    break
                msg += packet

        return msg




    def handle_cd(self, current_working_directory, new_working_directory):
            """
            Handles the client cd commands. Reads the client command and changes the current_working_directory variable
            accordingly. Returns the absolute path of the new current working directory.
            :param current_working_directory: string of current working directory
            :param new_working_directory: name of the sub directory or '..' for parent
            :return: absolute path of new current working directory
            """
            os.chdir(new_working_directory)
            return os.getcwd()

    def handle_mkdir(self, current_working_directory, directory_name):
            """
            Handles the client mkdir commands. Creates a new sub directory with the given name in the current working directory.
            :param current_working_directory: string of current working directory
            :param directory_name: name of new sub directory
            """
            pathto_newdir=current_working_directory+'/'+directory_name
            os.makedirs(pathto_newdir)

    def handle_rm(self, current_working_directory, object_name):
            """
            Handles the client rm commands. Removes the given file or sub directory. Uses the appropriate removal method
            based on the object type (directory/file).
            :param current_working_directory: string of current working directory
            :param object_name: name of sub directory or file to remove
            """
            removedir=current_working_directory+'/'+object_name
            if object_name.find(".") == -1: # IF object is a directory
                shutil.rmtree(removedir)
            else:
                os.remove(removedir)

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
            file_content=self.receive_message_ending_with_token(service_socket,1024,eof_token)
            file_path=os.getcwd()+'/'+file_name
            with open(file_path, 'wb') as f:
                    f.write(file_content)
            
           

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
            file_path=current_working_directory+'/'+file_name
            with open(file_path, 'rb') as f:
                file_content = f.read()

            file_content+=eof_token.encode()
            service_socket.sendall(file_content)


    def handle_info(
        self, current_working_directory, file_name, service_socket, eof_token
    ):
            """
            Handles the client info commands. Reads the size of a given file. 
            :param current_working_directory: string of current working directory
            :param file_name: name of sub directory or file to remove
            :param service_socket: active service socket with the client
            :param eof_token: a token to indicate the end of the message.
            """
            file_path=current_working_directory+'/'+file_name
            with open(file_path, 'rb') as f:
                file_content = f.read()

            file_size=str(len(file_content))
            msg='The size of file '+file_name+' is '+file_size+' bytes'+eof_token
            service_socket.sendall(msg.encode())
    
    def handle_mv(self,current_working_directory, file_name, destination_name):
            """
            Handles the client mv commands. First, it looks for the file in the current directory, then it moves or renames 
            to the destination file depending on the nature of the request.
            :param current_working_directory: string of current working directory
            :param file_name: name of the file tp be moved / renamed
            :param destination_name: destination directory or new filename
            """
            orig_dir=current_working_directory+'/'+file_name
            new_dir=destination_name+'/'+file_name
            shutil.move(orig_dir,new_dir)

    


class ClientThread(Thread):
    def __init__(self, server: Server, service_socket: socket.socket, address: str, eof_token: str):
        Thread.__init__(self)
        self.server_obj = server
        self.service_socket = service_socket
        self.address = address
        self.eof_token = eof_token

    def run(self):
        # print ("Connection from : ", self.address)
        # establish working directory
        # send the current dir info
        # while True:
        # get the command and arguments and call the corresponding method

        # sleep for 1 second

        # send current dir info

        # print('Connection closed from:', self.address)


        print ("Connection from : ", self.address)
        cwd=os.getcwd()
        cwd_info=self.server_obj.get_working_directory_info(cwd)
        cwd_info+=self.eof_token
        self.service_socket.sendall(cwd_info.encode())
        
        while True:
                
                command=self.server_obj.receive_message_ending_with_token(self.service_socket,1024,self.eof_token).decode()
                str=command.split()[0]
                match str:
                    case "cd":
                        current_working_directory=os.getcwd()
                        new_working_directory=command.split()[1]
                        updated_dir=self.server_obj.handle_cd(current_working_directory,new_working_directory)
                       
                        updated_dir+=self.eof_token
                        self.service_socket.sendall(updated_dir.encode())

                    case "mkdir":
                        current_working_directory=os.getcwd()
                        directory_name=command.split()[1]
                        self.server_obj.handle_mkdir(current_working_directory,directory_name)

                        msg='Created new directory at '+current_working_directory+'/'+directory_name+self.eof_token
                        self.service_socket.sendall(msg.encode())

                    case "rm":
                        current_working_directory=os.getcwd()
                        object_name=command.split()[1]
                        self.server_obj.handle_rm(current_working_directory,object_name)

                        msg='Removed object at '+current_working_directory+'/'+object_name+self.eof_token
                        self.service_socket.sendall(msg.encode())
                    
                    case "mv":
                        current_working_directory=os.getcwd()
                        file_name=command.split()[1]
                        destination_name=command.split()[2]
                        self.server_obj.handle_mv(current_working_directory,file_name,destination_name)

                        msg='Moved object at '+current_working_directory+'/'+file_name+'to location at'+destination_name+'/'+file_name+self.eof_token
                        self.service_socket.sendall(msg.encode())

                    case "dl":
                        current_working_directory=os.getcwd()
                        file_name=command.split()[1]
                        self.server_obj.handle_dl(current_working_directory,file_name,self.service_socket,self.eof_token)

                    case "ul":
                        current_working_directory=os.getcwd()
                        file_name=command.split()[1]
                        self.server_obj.handle_ul(current_working_directory,file_name,self.service_socket,self.eof_token)

                        msg='Uploaded file at '+current_working_directory+'/'+file_name+self.eof_token
                        self.service_socket.sendall(msg.encode())

                    case "info":
                        current_working_directory=os.getcwd()
                        file_name=command.split()[1]
                        self.server_obj.handle_info(current_working_directory,file_name,self.service_socket,self.eof_token)

                    case "exit":
                        
                        break
                    
                time.sleep(1)

           #     cwd=os.getcwd()              #Comment these 4 lines to get the proper output from TEST.py
            #    cwd_info=self.server_obj.get_working_directory_info(cwd)       # Because the test.py directly calls the functions 
            #    cwd_info+=self.eof_token                                       # instead of using the prompts from user
             #   self.service_socket.sendall(cwd_info.encode())                 # this messes with the output sent to the client

        print('Connection closed from:', self.address)
       


def run_server():
    HOST = "127.0.0.1"
    PORT = 65432

    server = Server(HOST, PORT)
    server.start()


if __name__ == "__main__":
    run_server()
