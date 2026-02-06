from langchain_ollama import ChatOllama
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from datetime import datetime
import asyncio
from typing import Dict, List, Optional

class ChatBot:
    """
    Advanced chatbot with memory, context awareness, and multiple features
    """
    
    def __init__(self, session_id: str, model_name: str = "llama3.2:latest"):
        self.session_id = session_id
        self.created_at = datetime.now().isoformat()
        
        # Initialize Ollama LLM
        self.llm = ChatOllama(
            model=model_name,
            temperature=0.7,
            callbacks=[StreamingStdOutCallbackHandler()]
        )
        
        # Create prompt with history placeholder
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful, intelligent AI assistant. You have memory of the conversation and can reference previous messages."),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # Create the base chain (prompt + LLM)
        self.chain = self.prompt | self.llm
        
        # Initialize message history store
        self.store = {}
        
        # Create the conversational chain with message history
        self.conversational_chain = RunnableWithMessageHistory(
            self.chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        
        # User context and preferences
        self.user_context = {}
        self.conversation_topics = []
    
    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        """Get or create chat message history for a session"""
        if session_id not in self.store:
            self.store[session_id] = ChatMessageHistory()
        return self.store[session_id]
    
    async def get_response(
        self, 
        message: str, 
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict:
        """
        Get response from the chatbot with memory
        """
        try:
            # Update temperature if provided
            if temperature is not None:
                # Create a new LLM instance with updated temperature
                self.llm = ChatOllama(
                    model=self.llm.model,
                    temperature=temperature,
                    callbacks=[StreamingStdOutCallbackHandler()]
                )
                # Recreate the chain with updated LLM
                self.chain = self.prompt | self.llm
                self.conversational_chain = RunnableWithMessageHistory(
                    self.chain,
                    self.get_session_history,
                    input_messages_key="input",
                    history_messages_key="history",
                )
            
            # Get response using the new pattern
            response = await asyncio.to_thread(
                self.conversational_chain.invoke,
                {"input": message},
                config={"configurable": {"session_id": self.session_id}}
            )
            
            # Extract the response content
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            # Update context
            self._update_context(message, response_text)
            
            return {
                "response": response_text,
                "metadata": {
                    "session_id": self.session_id,
                    "message_count": len(self.get_session_history(self.session_id).messages),
                    "topics": self.conversation_topics[-5:] if self.conversation_topics else []
                }
            }
        
        except Exception as e:
            return {
                "response": f"Error: {str(e)}",
                "metadata": {"error": True}
            }
    
    def _update_context(self, user_message: str, bot_response: str):
        """
        Update conversation context and extract topics
        """
        # Simple topic extraction (can be enhanced with NLP)
        words = user_message.lower().split()
        potential_topics = [w for w in words if len(w) > 5]
        self.conversation_topics.extend(potential_topics[:2])
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get conversation history
        """
        messages = self.get_session_history(self.session_id).messages
        history = []
        
        for msg in messages:
            role = "user" if msg.type == "human" else "assistant"
            history.append({
                "role": role,
                "content": msg.content,
                "timestamp": datetime.now().isoformat()
            })
        
        if limit:
            return history[-limit:]
        return history
    
    def clear_history(self):
        """
        Clear conversation memory
        """
        # Clear the specific session's history
        self.get_session_history(self.session_id).clear()
        self.conversation_topics = []
        self.user_context = {}
    
    def save_user_preference(self, key: str, value: str):
        """
        Save user preferences/context
        """
        self.user_context[key] = value
    
    def get_summary(self) -> str:
        """
        Get a summary of the conversation
        """
        history = self.get_history()
        if not history:
            return "No conversation history yet."
        
        return f"Session: {self.session_id}, Messages: {len(history)}, Topics: {', '.join(set(self.conversation_topics[-10:]))}"
    
    def change_model(self, model_name: str):
        """
        Switch to a different Ollama model
        """
        # Create new LLM instance with the new model
        self.llm = ChatOllama(
            model=model_name,
            temperature=self.llm.temperature,
            callbacks=[StreamingStdOutCallbackHandler()]
        )
        
        # Recreate the chain with new LLM
        self.chain = self.prompt | self.llm
        self.conversational_chain = RunnableWithMessageHistory(
            self.chain,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )