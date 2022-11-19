
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

HOST = '127.0.0.1' 
# Use the IPv4 address of the device hosting the server
# Findlay: 10.13.141.141
PORT =  1234

def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split('-')[0]
            content = message.split('-')[1]

            print(f"[{username}] {content}")
        else:
            print("Message received from server is empty!")


def send_message_to_server(client):

    while 1:
        message = input("Message: ")
        if message != '':
            client.sendall(message.encode())
        else:
            print('Empty message!')
            exit(0)    




def comunicate_to_server(client):

    username = input("Enter username: ")
    '''while username == '':
        username = input("Enter username")
        if username == '':
            print("Username cannot be empty!")'''
    if username != '':
        client.sendall(username.encode())
    else: 
        print("Username cannot be empty!")
        exit(0)
    Thread(target=listen_for_messages_from_server,args=(client, )).start()

    send_message_to_server(client)

# Main function
def main():
    
    # Creating a socket object
    client = socket(AF_INET, SOCK_STREAM)

    try:
        client.connect((HOST,PORT))
        print("Successfully connected to server")
    except:
        print(f"Unable to connect to server {HOST} {PORT}")

    comunicate_to_server(client)
if __name__ == '__main__':
    main()

