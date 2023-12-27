# Server Script 

import socket
import threading
import sys
import getopt
from colorama import Fore, Style, Back
import datetime
import time
import json

PORT = 5555

class ChatServer:
    def __init__(self, force_mode, room_id, room_pin):
        self.force_mode = force_mode
        self.room_id = room_id
        self.room_pin = room_pin
        self.rooms = {}
        # self.lock = threading.Lock()
        self.meta  = {}


    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        external_ip = s.getsockname()[0]
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        def broadcast():
            while True:
                message = f"{external_ip}:{PORT}"
                try:
                    s.sendto(message.encode(), ('<broadcast>', int(PORT)+1))
                except Exception as e:
                    raise Exception(e)
                time.sleep(2)
        b = threading.Thread(target=broadcast, daemon=True)
        b.start()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((external_ip, PORT))
        server_socket.listen()

        print(f"  * Setting up server\n  * Running on {external_ip}:{PORT}\n{Fore.YELLOW}{Style.DIM}Press CTRL+C to quit{Style.RESET_ALL}")
        if self.force_mode:
            print(f"  * Forced mode active\n  * Room ID: {self.room_id}\n")
        else: print()

        while True:
            try:
                client_socket, addr = server_socket.accept()
                print(f"\r[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] {Fore.GREEN}\"new client connection\" {Fore.BLUE}{addr}{Style.RESET_ALL} --")
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket,addr,))
                client_thread.start()
                # client_thread.join()
            except KeyboardInterrupt:
                raise Exception("server closed forcefully")

    def handle_client(self, client_socket, addr):
        try:
            mode, room_id, room_pin, username = json.loads(client_socket.recv(1024).decode('utf-8'))
            if self.force_mode and mode == 'create':
                client_socket.send(json.dumps({'success': False, 'msg': 'room creation not allowed since the server is running in forced mode'}).encode())
                raise Exception(f"invalid room creation request")
            elif mode == 'join':
                res, msg = self.handle_join_room(client_socket, username, room_id, room_pin)
                if not res:
                    client_socket.send(json.dumps({'success': False, 'msg': msg}).encode())
                else:
                    client_socket.send(json.dumps({'success': True}).encode())
            else:
                res = self.handle_create_room(client_socket, username, room_id, room_pin)
                if not res:
                    client_socket.send(json.dumps({'success': False, 'msg': msg}).encode())
                else:
                    client_socket.send(json.dumps({'success': True}).encode())
        except ConnectionResetError:
            print(f"\r[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] {Fore.RED}\"client socket disconnected\" {Fore.BLUE}{addr}{Style.RESET_ALL} --")
        except Exception as e:
            print(f"\r[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] {Fore.RED}\"{e}\" {Fore.BLUE}{addr}{Style.RESET_ALL} --")

    def get_client_mode_and_room(self, client_socket):
        mode = client_socket.recv(1024).decode('utf-8')
        room_id = client_socket.recv(1024).decode('utf-8')
        room_pin = client_socket.recv(1024).decode('utf-8')

        if self.force_mode and (room_id != self.room_id or room_pin != self.room_pin):
            client_socket.send("Room creation not allowed. Forced mode active.".encode('utf-8'))
            sys.exit()

        return mode, room_id, room_pin

    def handle_create_room(self, client_socket, room_id, room_pin):
        with self.lock:
            if not self.force_mode and room_id not in self.clients:
                self.clients[room_id] = []
                self.send_message_to_room(room_id, f"Room '{room_id}' created.")
            else:
                client_socket.send("Room creation not allowed.".encode('utf-8'))

    def handle_join_room(self, client_socket, room_id, room_pin):
        with self.lock:
            if room_id in self.clients and room_pin == self.room_pin:
                self.clients[room_id].append(client_socket)
                self.send_message_to_room(room_id, f"User '{client_socket.getpeername()[0]}' joined the room.")
            else:
                client_socket.send("Invalid room ID or room PIN.".encode('utf-8'))
                sys.exit()

    def send_message_to_room(self, room_id, message):
        with self.lock:
            for client in self.clients[room_id]:
                client.send(message.encode('utf-8'))

if __name__ == "__main__":
    try:
        force_mode = False
        room_id = ""
        room_pin = ""

        argv = sys.argv[1:]
        try:
            arguments, values = getopt.getopt(argv, "f:p:", ["force=","pin="])
        except getopt.error as err:
            raise Exception(str(err))
        recArgs = {}
        for opt, arg in arguments:
            if opt in ("-f", "--force") and arg and not room_id:
                    room_id = arg
            elif opt in ("-p", "--pin") and arg and not room_pin:
                    room_pin = arg
            else:
                raise Exception(f"option ({opt}, {arg}) cannot have multiple values")

        if room_id and room_pin:
            force_mode = True
        server = ChatServer(force_mode, room_id, room_pin)
        server.start()
    except Exception as e:
        print(f"\r[{datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}] {Fore.RED}\"{e}\"{Style.RESET_ALL} --")
        sys.exit(1)

# import socket
# import threading

# HOST = "192.168.1.18"
# PORT = 55555  # Port to listen on (non-privileged ports are > 1023)

# def main():
#         conn, addr = s.accept()
#         with conn:
#             print(f"Connected by {addr}")
#             def receive():
#                 while True:
#                     try:
#                         data = conn.recv(1024)
#                     except ConnectionResetError:
#                         s.close()
#                         print("\rConnection closed.")
#                         return
#                     print("\rClient: "+data.decode("utf-8")+"\nServer: ", end="")
#             threading.Thread(target=receive, dae+mon=True).start()
#             while True:
#                 msg = input("Server: ")
#                 if msg.lower() == "q":
#                     s.close()
#                     print("\rConnection closed.")
#                     return
#                 try:
#                     conn.sendall(msg.encode("utf-8"))
#                 except BrokenPipeError:
#                     s.close()
#                     return

# if __name__ == "__main__":
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.bind((HOST, PORT))
#         print("listening...")
#         s.listen()
#         main()