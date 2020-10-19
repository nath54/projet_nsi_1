import asyncio
import json.encoder
import websockets
import io


class WebServer():
    def __init__(self):
        self.IP = "localhost"
        self.PORT = 6789
        self.USERS = set()

    async def log(self, message):
        assert isinstance(message, str)
        print("log : " + message)
        f = io.open(self.logfile, "a", encoding="utf-8")
        f.write(message)
        f.close()

    async def register(self, websocket):
        self.USERS.add(websocket)

    async def unregister(self, websocket):
        self.USERS.remove(websocket)

    async def main_server(self, websocket, path):
        # register(websocket) sends user_event() to websocket
        await self.register(websocket)
        try:
            async for message in websocket:
                # TODO
                pass

        finally:
            await self.unregister(websocket)

    def main(self):
        print("Server starting...")
        self.start_server = websockets.serve(self.main_server, self.IP,
                                             self.PORT)

        print("Server started.")
        asyncio.get_event_loop().run_until_complete(self.start_server)
        asyncio.get_event_loop().run_forever()
