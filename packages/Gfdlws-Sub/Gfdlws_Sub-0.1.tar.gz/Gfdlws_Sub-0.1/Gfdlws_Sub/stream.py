# import asyncio
# import websockets
# import json
#
#
# class WebSocketClient:
#     def __init__(self, uri, token):
#         self.uri = uri
#         self.token = token
#         self.connection = None
#
#     async def connect(self):
#         self.connection = await websockets.connect(self.uri)
#         print("Connected to WebSocket")
#
#     async def authenticate(self):
#         # Send authentication message with the provided token
#         auth_message = json.dumps({
#             "MessageType": "Authenticate",
#             "Password": self.token
#         })
#         await self.connection.send(auth_message)
#         print("Sent authentication message")
#
#     async def subscribe_realtime_Greeks(self, exchange, Tokens, unsubscribe=False):
#         # Convert the instrument_identifiers list to a comma-separated string
#         for instrument in Tokens:
#             # Prepare subscription message for each instrument
#             subscribe_message = json.dumps({
#                 "MessageType": "SubscribeRealtimeGreeks",
#                 "Exchange": exchange,
#                 "Token": instrument,
#                 "Unsubscribe": unsubscribe
#             })
#
#             # Send subscription message
#             await self.connection.send(subscribe_message)
#             print(f'SENT:{subscribe_message}')
#         # print(f"Subscribed to {exchange} with instruments: {instrument_identifiers_str} (Unsubscribe: {unsubscribe})")
#
#     async def handle_messages(self):
#         while True:
#             try:
#                 message = await self.connection.recv()
#                 data = json.loads(message)
#                 # self.on_message(data)
#                 return data
#             except websockets.ConnectionClosed:
#                 print("Connection closed")
#                 break
#
#     def on_message(self, data):
#         # Handle messages
#         if data.get("MessageType") != "Echo":
#             print(f"Received message: {data}")
#
#     async def run(self, exchange, Tokens, unsubscribe=False,handle_messages =None):
#         # Connect, authenticate, subscribe, and handle messages
#         await self.connect()
#         await self.authenticate()
#         await self.subscribe_realtime_Greeks(exchange,Tokens, unsubscribe,handle_messages)
#         # await self.unsubscribe_realtime(exchange, instrument_identifiers)
#         await self.handle_messages()
#
#
# # Wrapper function that uses the 'SubscribeRealtime' name explicitly
# async def SubscribeRealtimeGreeks(client, exchange, Tokens, unsubscribe=False,handle_messages =None):
#     await client.run(exchange, Tokens, unsubscribe,handle_messages =None)

import asyncio
import websockets
import json


class WebSocketClient:
    def __init__(self, uri, token):
        self.uri = uri
        self.token = token
        self.connection = None

    async def connect(self):
        self.connection = await websockets.connect(self.uri)
        print("Connected to WebSocket")

    async def authenticate(self):
        auth_message = json.dumps({
            "MessageType": "Authenticate",
            "Password": self.token
        })
        await self.connection.send(auth_message)
        print("Sent authentication message")

    async def subscribe_realtime(self, exchange, instrument_identifiers, unsubscribe=False):
        for instrument in instrument_identifiers:
            subscribe_message = json.dumps({
                "MessageType": "SubscribeRealtime",
                "Exchange": exchange,
                "InstrumentIdentifier": instrument,
                "Unsubscribe": unsubscribe
            })
            await self.connection.send(subscribe_message)
            print(f'SENT: {subscribe_message}')

    async def subscribe_realtime_greeks(self, exchange, tokens, unsubscribe=False):
        for token in tokens:
            subscribe_greeks_message = json.dumps({
                "MessageType": "SubscribeRealtimeGreeks",
                "Exchange": exchange,
                "Token": token,
                "Unsubscribe": unsubscribe
            })
            await self.connection.send(subscribe_greeks_message)
            print(f'SENT: {subscribe_greeks_message}')

    async def handle_messages(self, message_handler):
        while True:
            try:
                message = await self.connection.recv()
                data = json.loads(message)
                await message_handler(data)  # Call the external message handler
            except websockets.ConnectionClosed:
                print("Connection closed")
                break

    async def run(self, subscription_type, exchange, instrument_identifiers, tokens, unsubscribe=False,
                  message_handler=None):
        await self.connect()
        await self.authenticate()

        # Call only the requested subscription type
        if subscription_type == "realtime":
            await self.subscribe_realtime(exchange, instrument_identifiers, unsubscribe)
        elif subscription_type == "realtime_greeks":
            await self.subscribe_realtime_greeks(exchange, tokens, unsubscribe)

        if message_handler:
            await self.handle_messages(message_handler)  # Pass the message handler


# Wrapper function for SubscribeRealtimeGreeks
async def SubscribeRealtimeGreeks(client, exchange, tokens, unsubscribe=False, message_handler=None):
    await client.run(subscription_type="realtime_greeks", exchange=exchange, instrument_identifiers=None, tokens=tokens,
                     unsubscribe=unsubscribe, message_handler=message_handler)


# Wrapper function for SubscribeRealtime
async def SubscribeRealtime(client, exchange, instrument_identifiers, unsubscribe=False, message_handler=None):
    await client.run(subscription_type="realtime", exchange=exchange, instrument_identifiers=instrument_identifiers,
                     tokens=None, unsubscribe=unsubscribe, message_handler=message_handler)

# # Example of a message handler function
# async def message_handler(data):
#     print(f"Received data: {data}")
#
#
# if __name__ == "__main__":
#     uri = "wss://example.websocket.server"
#     token = "your_authentication_token"
#     exchange = "NFO"
#     tokens = ["5368", "458879", "2546841"]
#
#     client = WebSocketClient(uri, token)
#
#     # Use asyncio to run the WebSocket client
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(SubscribeRealtimeGreeks(client, exchange, tokens, unsubscribe=False, message_handler=message_handler))





