
# Remote Terminal Application with Sockets

This project implements a simple version of an interactive remote terminal application using sockets in Python. The application follows a client-server architecture where a central server listens for connections from multiple clients. Upon connection, a client can send commands to the server, which executes them and sends back the result, including the Current Working Directory (CWD) with any changes.

## Overview

The system consists of two main components: the server and the client. Here's a brief overview of each:

### Server

- Initializes a socket and internal variables.
- Awaits connections from clients.
- Handles each client connection in a new thread.
- Sends a random token to the client for message termination.
- Sends the CWD information to the client before receiving each command.
- Maintains a CWD variable per client.
- Supports functionalities like changing directories, creating directories, removing files or directories, relocating files, downloading files, uploading files, fetching file information, and exiting the application.

### Client

- Initializes internal variables.
- Establishes a connection to the server socket.
- Receives the random token for message termination.
- Displays the received CWD information from the server.
- Sends commands to the server.
- Displays the updated CWD information and any other output received from the server.
- Gracefully terminates the connection upon receiving the exit command.

## Functionalities

Both the client and server support the following functionalities:

| Command | Functionality                             | Example       |
|---------|-------------------------------------------|---------------|
| cd      | Changes the current working directory     | cd products  |
| mkdir   | Creates a new directory                   | mkdir client_1_files |
| rm      | Removes a file or directory               | rm about.txt |
| mv      | Relocates or renames a file               | mv about.txt info/ <br> mv about.txt my.txt |
| dl      | Downloads a file from the server          | dl about.txt |
| ul      | Uploads a file to the server              | ul orca.jpg |
| info    | Reads file size from the server           | info image.jpg |
| exit    | Exits the application                     | exit          |

## File Structure

The project includes client and server templates along with sample files. Upon successful implementation, the server should create the following directory tree:

.
├── server.py
├── client.py
├── test.py
├── ...


## Implementation

The implementation involves filling in the missing code indicated by `NotImplementedError` in both the client and server templates. The provided `test.py` script validates the fundamental structure and functionality of the code.

## Note

Ensure that the communication between the server and client uses a buffer (packet) size of 1024 bytes for all messages. Successfully running the `test.py` script contributes to a portion of the overall grade, but the entire assignment is graded based on the complete implementation.

[Download Sample Files](sample_files.zip)

## References

- [Python Socket Programming Documentation](https://docs.python.org/3/library/socket.html)
