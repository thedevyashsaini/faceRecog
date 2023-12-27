# Client Script

import socket
import threading
import sys
import datetime
from colorama import Fore, Style, Back
import getopt
import json

class ChatClient:
    def __init__(self, mode, room_id, room_pin, username):
        if not mode:
            m = input("Enter mode (join/create): ").lower()
            if m in ["join","create"]:
                self.mode = m
            else:
                 raise Exception(f"invalid value for mode ({m})")
        else:
            self.mode = mode

        if not room_id:
            self.room_id = input("Enter room ID: ")
        else:
            self.room_id = room_id

        if not room_pin:
            self.room_pin = input("Enter room PIN: ")
        else:
            self.room_pin = room_pin

        if not username:
            self.username = input("Enter your username: ")
        else:
            self.username = username

    def start(self):
        print("  * Setting up client")
        server, port = self.getServer()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"  * Connecting to {server}:{port}\n{Fore.YELLOW}{Style.DIM}Press CTRL+C to quit{Style.RESET_ALL}")
        client_socket.connect((server, int(port)))
        addr = client_socket.getsockname()
        print(f"  * Client {addr[0]}\n  * PORT: {addr[1]}\n")
        client_socket.send(json.dumps([self.mode, self.room_id, self.room_pin, self.username]).encode('utf-8'))
        res = json.loads(client_socket.recv(1024).decode('utf-8'))
        if not res["success"]:
             raise Exception(res["msg"])
        print(f"\r[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] {Fore.GREEN}\"{e}\"{Style.RESET_ALL} --")
        receive_thread = threading.Thread(target=self.receive_messages, args=(client_socket,))
        receive_thread.start()
        receive_thread.join()

        while True:
            message = input()
            client_socket.send(message.encode('utf-8'))

    def receive_messages(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                print(message)
            except socket.error as e:
                print("Error receiving message:", str(e))
                sys.exit()
    
    def getServer(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_socket.bind(('', 5556))
        while True:
            data, addr = client_socket.recvfrom(1024)
            server_ip, server_port = data.decode().split(':')
            client_socket.close()
            return server_ip, server_port

if __name__ == "__main__":
    try:
        args = sys.argv[1:]
        mode = ""
        room_id = ""
        room_pin = ""
        username = ""

        argv = sys.argv[1:]
        try:
            arguments, values = getopt.getopt(argv, "m:r:p:u:", ["mode=","room=","pin=","user="])
        except getopt.error as err:
            raise Exception(str(err))
        recArgs = {}
        for opt, arg in arguments:
            if opt in ("-m", "--mode") and arg and not mode:
                    if arg in ["join","create"]:
                        mode = arg
                    else:
                        raise Exception(f"invalid argument value provided ({opt}, {arg})")
            elif opt in ("-r", "--room") and arg and not room_id:
                    room_id = arg
            elif opt in ("-p", "--pin") and arg and not room_pin:
                    room_pin = arg
            elif opt in ("-u", "--user") and arg and not username:
                    username = arg
            else:
                raise Exception(f"option ({opt}, {arg}) cannot have multiple values")
        client = ChatClient(mode, room_id, room_pin, username)
        client.start()
    except Exception as e:
        print(f"\r[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] {Fore.RED}\"{e}\"{Style.RESET_ALL} --")
        sys.exit(1)