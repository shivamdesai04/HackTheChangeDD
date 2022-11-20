
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from deep_translator import GoogleTranslator
import sys
import mysql.connector
HOST = '127.0.0.1' 
# Use the IPv4 address of the device hosting the server
# Findlay: 10.13.61.145
PORT =  5500
CHAR_LIMIT = 2048
mydb = mysql.connector.connect(
    host = '127.0.0.1',
    user = 'Findlay',
    password = 'helloworld',
    database = 'COMMUNIFY')
mycursor = mydb.cursor()
def listen_for_messages_from_server(client):
    while True:
        message = client.recv(CHAR_LIMIT).decode('utf-8')
        #mycursor.execute(f"SELECT Language FROM UNIQUE_USER_DATA where User_name = '{message.split('-')[0]}'")
        #languageInfo = mycursor.fetchone()
        if message != '':
            username = message.split('-')[0]
            translated_content = GoogleTranslator(source ='auto' ,target='ru').translate(message.split('-')[1])
            

            print(f"[{username}] {translated_content}")
        else:
            #print("Message received from server is empty!")
            sys.exit('You have left the chat...')
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
    #language = input("what language do you speak?")
    while True:
        language = input("what language do you speak?").lower()
        if language in ['afrikaans', 'albanian', 'amharic', 'arabic', 'armenian', 'assamese', 'aymara', 'azerbaijani', 'bambara', 'basque', 'belarusian', 'bengali', 'bhojpuri', 'bosnian', 'bulgarian', 'catalan', 'cebuano', 'chichewa', 'chinese (simplified)', 'chinese (traditional)', 'corsican', 'croatian', 'czech', 'danish', 'dhivehi', 'dogri', 'dutch', 'english', 'esperanto', 'estonian', 'ewe', 'filipino', 'finnish', 'french', 'frisian', 'galician', 'georgian', 'german', 'greek', 'guarani', 'gujarati', 'haitian creole', 'hausa', 'hawaiian', 'hebrew', 'hindi', 'hmong', 'hungarian', 'icelandic', 'igbo', 'ilocano', 'indonesian', 'irish', 'italian', 'japanese', 'javanese', 'kannada', 'kazakh', 'khmer', 'kinyarwanda', 'konkani', 'korean', 'krio', 'kurdish (kurmanji)', 'kurdish (sorani)', 'kyrgyz', 'lao', 'latin', 'latvian', 'lingala', 'lithuanian', 'luganda', 'luxembourgish', 'macedonian', 'maithili', 'malagasy', 'malay', 'malayalam', 'maltese', 'maori', 'marathi', 'meiteilon (manipuri)', 'mizo', 'mongolian', 'myanmar', 'nepali', 'norwegian', 'odia (oriya)', 'oromo', 'pashto', 'persian', 'polish', 'portuguese', 'punjabi', 'quechua', 'romanian', 'russian', 'samoan', 'sanskrit', 'scots gaelic', 'sepedi', 'serbian', 'sesotho', 'shona', 'sindhi', 'sinhala', 'slovak', 'slovenian', 'somali', 'spanish', 'sundanese', 'swahili', 'swedish', 'tajik', 'tamil', 'tatar', 'telugu', 'thai', 'tigrinya', 'tsonga', 'turkish', 'turkmen', 'twi', 'ukrainian', 'urdu', 'uyghur', 'uzbek', 'vietnamese', 'welsh', 'xhosa', 'yiddish', 'yoruba', 'zulu']:
            break
        else:
            print('language not valid, please try again')
    mycursor.execute(f"INSERT INTO UNIQUE_USER_DATA VALUES('{username}','{language}')")
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
        loginInfo = mycursor.fetchall()
        if sign_in == '1':
            if not check_in_result(loginInfo, username):
                mycursor.execute(f"INSERT INTO CLIENT_USER_PASS VALUES('{username}','{password}')")
                mydb.commit()
                print(f"{username} has signed in!")
                collect_data(username)
                break
            else:
                print('Account with that username already created. Please log in.')
        else: 
            if check_in_result(loginInfo, username, password):
                print(f"{username} has logged in!")
                break
            else:
                print('Account not found. Please sign in.')
    
    client.sendall(username.encode())
    try:
        Thread(target=listen_for_messages_from_server,args=(client, )).start()
    except Exception as e:
        sys.exit('You have left the chat...')
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
    return 0
    
if __name__ == '__main__':
    main()
