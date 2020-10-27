import asyncio
import json.encoder
import websockets
import io

import socket
import _thread
import json
import sys


class Client_socket:
    def __init__(self, parent_websocket, ws, port=9876):
        self.parent_websocket = parent_websocket
        self.ws = ws
        self.host = "localhost"
        self.port = port
        self.max_size = 1024
        self.client = None
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print((self.host, self.port))
        self.client.connect((self.host, self.port))
        _thread.start_new_thread(self.handle, ())

    def send(self, message):
        message = message.encode(encoding="utf-8")
        size = sys.getsizeof(message)
        if size > self.max_size:
            print(f"""ERREUR : Le message est trop long ! {+str(size)} bytes/
                    {str(self.max_size)} bytes""")
        else:
            self.client.send(message)

    def handle(self):
        while True:
            try:
                msg = self.client.recv(self.max_size)
                if len(msg) == 0:
                    raise UserWarning("message vide")
                self.parent_websocket.message_recu(ws, msg)
            except Exception as e:
                print(e)
                self.on_close()
                return


class WebServer():
    def __init__(self, port_client_socket=None):
        self.IP = "localhost"
        self.PORT = 6789
        self.USERS = set()
        self.port_client_socket = port_client_socket

    async def log(self, message):
        assert isinstance(message, str)
        print("log : " + message)
        f = io.open(self.logfile, "a", encoding="utf-8")
        f.write(message)
        f.close()

    async def register(self, websocket):
        self.USERS.add(websocket)
        # print(websocket," connected")

    async def unregister(self, websocket):
        self.USERS.remove(websocket)
        # print(websocket," disconnected")

    async def main_server(self, websocket, path):
        await self.register(websocket)
        if self.port_client_socket is None:
            client_sock = Client_socket(self, websocket)
        else:
            client_sock = Client_socket(self, websocket,
                                        port=self.port_client_socket)
        try:
            async for message in websocket:
                Client_socket.send(message)
        finally:
            await self.unregister(websocket)

    def message_recu(self, websocket, message):
        websocket.send(message)

    def main(self):
        print("Websocket server starting...")
        self.start_server = websockets.serve(self.main_server, self.IP,
                                             self.PORT)

        print("Websocket server started.")
        asyncio.get_event_loop().run_until_complete(self.start_server)
        asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    ws = WebServer()
    ws.main()
