import asyncio
import json.encoder
import websockets
import io

import socket
import _thread
import json
import sys

class WebServer():
    def __init__(self,client):
        self.IP = "localhost"
        self.PORT = 6789
        self.USER = None
        self.client=client

    async def register(self, websocket):
        if self.USER == None:
            self.USER = websocket

    async def unregister(self, websocket):
        self.USER = None

    async def main_server(self, websocket, path):
        if self.USER != None:
            print("Un utilisateur a voulu se connecter alors que la place n'était pas libre")
            return
        await self.register(websocket)
        try:
            async for message in websocket:
                self.client.send(message)
        finally:
            await self.unregister(websocket)

    async def on_message(self, message):
        await self.USER.send(message)

    def main(self):
        print("Websocket server starting...")
        self.start_server = websockets.serve(self.main_server, self.IP,
                                             self.PORT)
        print("Websocket server started.")
        asyncio.get_event_loop().run_until_complete(self.start_server)
        asyncio.get_event_loop().run_forever()
