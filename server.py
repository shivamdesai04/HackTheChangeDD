

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import threading


HOST = '0.0.0.0'
PORT =  1234
CHAR_LIMIT = 2048
LISTENER_LIMIT = 5
active_clients = [] # List of all connected users



# Function to listen for upcoming messages from a client
def listen_for_messages(client,username):

    while 1:
        message = client.recv(CHAR_LIMIT).decode('utf-8')
        if message == 'quit':
            client.close()
            active_clients.remove(username)
            break
        elif message != '':
            final_msg = username + '-' + message
            send_messages_to_all(final_msg)
        else:
            print(f'The message sent from client {username} is empty')


def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1],message)
    
# Function to send message to a single client
def send_message_to_client(client, message):

    client.sendall(message.encode())


# Function to handle client
def client_handler(client):
    
    # Server will listen for client message that will
    # Contain the username

    while 1:

        username = client.recv(CHAR_LIMIT).decode('utf-8')
        if username != '':
            print(f"{username} has joined server!")
            active_clients.append((username, client))
            break
        else:
            print('Client username is empty!')    
            break
    Thread(target = listen_for_messages, args = (client, username, )).start()


# Main function
def main():
    # Creating the server socket class object

    server = socket(AF_INET, SOCK_STREAM)

    try:
        # Provide the server with an address in the form of 
        # host IP and port
        server.bind((HOST, PORT))
        print(f"Server is running on {HOST} {PORT}")
    except:
        print(f'Unable to bind to host: {HOST} and port: {PORT}')

    server.listen(LISTENER_LIMIT)

    while 1:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        Thread(target=client_handler,args=(client, )).start()

        #send_message_to_client(client,"Hello!")
# C:\Users\calga\OneDrive\Documents\GitHub\HackTheChangeDD
    server.close()


if __name__ == '__main__':
    main()





