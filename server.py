
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import threading


HOST = '0.0.0.0'
PORT =  5500
CHAR_LIMIT = 512
LISTENER_LIMIT = 10
active_clients = [] # List of all connected users


# Function to listen for upcoming messages from a client
def listen_for_messages(client,username):
    while True:
        message = client.recv(CHAR_LIMIT).decode('utf-8')
        if message == 'quit': 
            active_clients.remove((username, client,))
            client.close()
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
def wait_for_client(client):
    # Server will wait for client message that will
    # Contain the username
    while True:
        try:
            username = client.recv(CHAR_LIMIT).decode('utf-8')
            
            print(f"{username} has joined server!")
            active_clients.append((username, client))
            break
        except Exception as e:
            print("[EXCEPTION]",e)
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

    while True:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")
        
        Thread(target=wait_for_client,args=(client, )).start()
        
        #send_message_to_client(client,"Hello!")
    server.close()


if __name__ == '__main__':
    main()





