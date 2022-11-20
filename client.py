
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import mysql.connector

HOST = '127.0.0.1' 
# Use the IPv4 address of the device hosting the server
# Findlay: 10.13.141.141
PORT =  1234
CHAR_LIMIT = 2048

mydb = mysql.connector.connect(
    host = '127.0.0.1',
    user = 'root',
    password = '27Eggs@home',
    database = 'COMMUNIFY')

mycursor = mydb.cursor()

def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(CHAR_LIMIT).decode('utf-8')
        if message != '':
            username = message.split('-')[0]
            content = message.split('-')[1]

            print(f"[{username}] {content}")
        else:
            print("Message received from server is empty!")


def send_message_to_server(client):

    while True:
        message = input("Message: ")
        if message != '':
            client.sendall(message.encode())
        else:
            print('Empty message!')    

def check_in_result(result, what, whatelse = ''):
    for i in result:
        if what in i:
            if whatelse != '' and whatelse not in i:
                return False
            return True
    return False

def collect_data(username):
    language = input("what language do you speak?")
    display_name = input("name name do you want to be seen as?")
    mycursor.execute(f"INSERT INTO UNIQUE_USER_DATA VALUES('{username}','{language}','{display_name}')")
    mydb.commit()

def comunicate_to_server(client):
    while True:
        sign_in = input('type 1 to sign in or 0 to log in: ') #given by a sign in button from front end
        username = input("Enter username: ")
        password = input("Enter password: ")
        while username == '' or password == '':
            print("username/password cannot be empty!")
            username = input(f"Enter username: ")
            password = input(f"Enter password: ")
        mycursor.execute('SELECT User_n,Pass_w FROM CLIENT_USER_PASS')
        myresult = mycursor.fetchall()
        if sign_in == '1':
            if not check_in_result(myresult, username):
                mycursor.execute(f"INSERT INTO CLIENT_USER_PASS VALUES('{username}','{password}')")
                mydb.commit()
                print(f"{username} has signed in!")
                collect_data(username)
                break
            else:
                print('Account with that username already created. Please log in.')
        else: 
            if check_in_result(myresult, username, password):
                print(f"{username} has logged in!")
                break
            else:
                print('Account not found. Please sign in.')
    mycursor.execute(f"SELECT Display_n FROM UNIQUE_USER_DATA where User_name = '{username}'")
    displayname = mycursor.fetchone()[0]
    client.sendall(displayname.encode())

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
