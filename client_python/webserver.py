import asyncio
import json.encoder
import websockets
import io

import socket
import _thread
import json
import sys
import time


class WebServer():
    def __init__(self, client):
        self.IP = "localhost"
        self.PORT = 6789
        self.USER = None
        self.client = client
        self.messages_en_attente = []

    async def register(self, websocket):
        if self.USER is None:
            self.USER = websocket

    async def unregister(self, websocket):
        self.USER = None

    async def main_server(self, websocket, path):
        if self.USER is not None:
            print("Un utilisateur a voulu se connecter alors que la place n'était pas libre")
            return
        await self.register(websocket)
        for mes in self.messages_en_attente:
            await self.USER.send(mes)
            time.sleep(0.1)
        try:
            async for message in websocket:
                cs = True
                try:
                    data = json.loads(message)
                    if data["type"] == "veut changer de page":
                        cs = False
                        await websocket.send(json.dumps({"type": "autorisation changement page"}))
                        await websocket.close()
                except Exception:
                    pass
                #
                if cs:
                    self.client.send(message)
        finally:
            await self.unregister(websocket)

    async def on_message(self, message):
        if self.USER is not None:
            await self.USER.send(message)
        else:
            self.messages_en_attente.append(message)

    def main(self):
        print("Websocket server starting...")
        self.start_server = websockets.serve(self.main_server, self.IP,
                                             self.PORT)
        print("Websocket server started.")
        asyncio.get_event_loop().run_until_complete(self.start_server)
        asyncio.get_event_loop().run_forever()
