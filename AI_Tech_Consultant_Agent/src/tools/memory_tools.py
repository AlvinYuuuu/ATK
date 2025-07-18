"""
Tools for interacting with the Mem0 knowledge base.

This module provides functions for agents to save, search, and manage
long-term memory using the Mem0 service. It follows the recommended
integration pattern for Google ADK.

Reference: https://docs.mem0.ai/integrations/google-ai-adk
"""

from mem0 import MemoryClient
from src.core.config import settings

# Initialize a single client instance to be reused by the tools.
# It reads the MEM0_API_KEY from env vars and can be configured with a
# custom base URL via the settings object.
mem0_client = MemoryClient(api_base=settings.MEM0_API_BASE)

def search_memory(query: str, user_id: str) -> dict:
    """
    Searches the memory for information relevant to the user's query.

    Args:
        query (str): The search query.
        user_id (str): The unique identifier for the user whose memory is being searched.

    Returns:
        dict: A dictionary containing the search results or a message if no memories are found.
    """
    print(f"Tool: Searching memory for user '{user_id}' with query: '{query}'")
    memories = mem0_client.search(query=query, user_id=user_id)
    if memories:
        # Format memories for the LLM
        memory_context = "\n".join([f"- {mem['memory']}" for mem in memories])
        print(f"Tool: Found memories:\n{memory_context}")
        return {"status": "success", "memories": memory_context}
    
    print("Tool: No relevant memories found.")
    return {"status": "no_memories", "message": "No relevant memories found"}

def save_memory(content: str, user_id: str, metadata: dict = None) -> dict:
    """
    Saves a piece of information to the user's memory.

    Args:
        content (str): The information to save.
        user_id (str): The unique identifier for the user whose memory is being updated.
        metadata (dict, optional): A dictionary of metadata to associate with the memory.

    Returns:
        dict: A dictionary confirming the status of the operation.
    """
    print(f"Tool: Saving memory for user '{user_id}': '{content}'")
    try:
        # The mem0 client expects a list of messages.
        messages_to_add = [{"role": "user", "content": content}]
        mem0_client.add(messages_to_add, user_id=user_id, metadata=metadata)
        print("Tool: Memory saved successfully.")
        return {"status": "success", "message": "Information saved to memory"}
    except Exception as e:
        print(f"Tool: Failed to save memory. Error: {e}")
        return {"status": "error", "message": f"Failed to save memory: {str(e)}"}
