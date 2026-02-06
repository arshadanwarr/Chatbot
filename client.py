import requests
import json
from typing import Optional, Dict, List
import time

class ChatbotClient:
    """
    Python client for interacting with the chatbot API
    """
    
    def __init__(self, base_url: str = "http://localhost:8000", session_id: Optional[str] = None):
        self.base_url = base_url
        self.session_id = session_id or f"client_{int(time.time())}"
    
    def send_message(
        self, 
        message: str, 
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Dict:
        """Send a message to the chatbot"""
        url = f"{self.base_url}/api/chat"
        payload = {
            "message": message,
            "session_id": self.session_id,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_history(self, limit: Optional[int] = None) -> Dict:
        """Get conversation history"""
        url = f"{self.base_url}/api/history/{self.session_id}"
        params = {"limit": limit} if limit else {}
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def clear_history(self) -> Dict:
        """Clear conversation history"""
        url = f"{self.base_url}/api/clear/{self.session_id}"
        
        response = requests.delete(url)
        response.raise_for_status()
        return response.json()
    
    def get_sessions(self) -> List[Dict]:
        """Get all active sessions"""
        url = f"{self.base_url}/api/sessions"
        
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    def delete_session(self) -> Dict:
        """Delete the current session"""
        url = f"{self.base_url}/api/sessions/{self.session_id}"
        
        response = requests.delete(url)
        response.raise_for_status()
        return response.json()
    
    def chat(self):
        """Interactive chat interface"""
        print(f"🤖 Chatbot Client Started (Session: {self.session_id})")
        print("Type 'exit' to quit, 'history' to view conversation, 'clear' to reset")
        print("-" * 60)
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() == 'exit':
                    print("Goodbye! 👋")
                    break
                
                if user_input.lower() == 'history':
                    history = self.get_history()
                    print("\n📜 Conversation History:")
                    for msg in history.get('messages', []):
                        print(f"{msg['role'].capitalize()}: {msg['content'][:100]}...")
                    continue
                
                if user_input.lower() == 'clear':
                    self.clear_history()
                    print("✅ Conversation history cleared!")
                    continue
                
                # Send message and get response
                print("🤔 Thinking...", end='\r')
                result = self.send_message(user_input)
                print(f"Bot: {result['response']}")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main function to run the client"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Chatbot API Client")
    parser.add_argument("--url", default="http://localhost:8000", help="API base URL")
    parser.add_argument("--session", default=None, help="Session ID")
    
    args = parser.parse_args()
    
    client = ChatbotClient(base_url=args.url, session_id=args.session)
    client.chat()

if __name__ == "__main__":
    main()