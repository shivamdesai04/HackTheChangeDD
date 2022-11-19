
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

HOST = '127.0.0.1' 
# Use the IPv4 address of the device hosting the server
# Findlay: 10.13.141.141

PORT =  1234

def main():
    
    # Creating a socket object
    client = socket(AF_INET, SOCK_STREAM)

    try:
        client.connect((HOST,PORT))
        print("Successfully connected to server")
    except:
        print(f"Unable to connect to server {HOST} {PORT}")


if __name__ == '__main__':
    main()

