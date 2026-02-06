import asyncio
import websockets
import json
from datetime import datetime

class WebSocketChatClient:
    """
    WebSocket client for real-time chat with the bot
    """
    
    def __init__(self, url: str = "ws://localhost:8000", session_id: str = "websocket_client"):
        self.url = f"{url}/ws/{session_id}"
        self.session_id = session_id
        self.websocket = None
    
    async def connect(self):
        """Connect to the WebSocket server"""
        self.websocket = await websockets.connect(self.url)
        print(f"✅ Connected to chatbot (Session: {self.session_id})")
    
    async def send_message(self, message: str, temperature: float = 0.7):
        """Send a message via WebSocket"""
        if not self.websocket:
            raise Exception("Not connected. Call connect() first.")
        
        payload = {
            "message": message,
            "temperature": temperature,
            "max_tokens": 2000
        }
        
        await self.websocket.send(json.dumps(payload))
    
    async def receive_message(self):
        """Receive a message from the WebSocket"""
        if not self.websocket:
            raise Exception("Not connected. Call connect() first.")
        
        response = await self.websocket.recv()
        return json.loads(response)
    
    async def chat(self):
        """Interactive chat loop"""
        await self.connect()
        
        print("🤖 Real-time Chatbot Ready!")
        print("Type 'exit' to quit")
        print("-" * 60)
        
        async def send_messages():
            """Handle sending messages"""
            while True:
                try:
                    user_input = await asyncio.get_event_loop().run_in_executor(
                        None, input, "\nYou: "
                    )
                    
                    if user_input.strip().lower() == 'exit':
                        await self.websocket.close()
                        return
                    
                    if user_input.strip():
                        await self.send_message(user_input.strip())
                
                except Exception as e:
                    print(f"Error sending: {e}")
                    break
        
        async def receive_messages():
            """Handle receiving messages"""
            while True:
                try:
                    response = await self.receive_message()
                    print(f"\nBot: {response['response']}")
                    print(f"[{response['timestamp']}]")
                
                except websockets.exceptions.ConnectionClosed:
                    print("\n🔌 Connection closed")
                    break
                except Exception as e:
                    print(f"Error receiving: {e}")
                    break
        
        # Run send and receive concurrently
        await asyncio.gather(send_messages(), receive_messages())
    
    async def close(self):
        """Close the WebSocket connection"""
        if self.websocket:
            await self.websocket.close()

async def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="WebSocket Chatbot Client")
    parser.add_argument("--url", default="ws://localhost:8000", help="WebSocket URL")
    parser.add_argument("--session", default="websocket_client", help="Session ID")
    
    args = parser.parse_args()
    
    client = WebSocketChatClient(url=args.url, session_id=args.session)
    
    try:
        await client.chat()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())