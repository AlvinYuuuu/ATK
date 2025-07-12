"""
Shared Memory system using Mem0 for inter-agent communication and knowledge persistence.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

# Import Mem0 configuration
from .config import MEM0_AVAILABLE

class MockMemory:
    """Mock memory system for development when Mem0 is not available."""
    
    def __init__(self, memory_id: str):
        self.memory_id = memory_id
        self.memories = []
        self.counter = 0
    
    def add(self, memory_id: str, content: str, metadata: Dict[str, Any] = None):
        """Add a memory entry."""
        self.memories.append({
            "id": memory_id,
            "content": content,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        })
        self.counter += 1
    
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Search memories by query."""
        results = []
        for memory in self.memories:
            if query.lower() in memory["content"].lower():
                results.append(memory)
        return results

class SharedMemory:
    """
    Centralized memory system using Mem0 for storing and retrieving information
    between different agents in the AI Tech Consultant system.
    """
    
    def __init__(self, memory_id: str = "ai_tech_consultant"):
        """Initialize the shared memory with Mem0."""
        self.memory_id = memory_id
        
        # Try to initialize Mem0 if available, fallback to mock if it fails
        if MEM0_AVAILABLE:
            try:
                from mem0 import Memory
                # Check if MEM0_API_KEY is properly set
                mem0_api_key = os.environ.get("MEM0_API_KEY")
                mem0_host = os.environ.get("MEM0_HOST")
                print(f"MEM0_API_KEY: {mem0_api_key}")
                print(f"MEM0_HOST: {mem0_host}")
                
                # if not mem0_api_key or mem0_api_key == "your-mem0-api-key-here":
                #     print("⚠️ MEM0_API_KEY not properly configured, using mock memory system")
                #     self.memory = MockMemory(memory_id)
                #     return
                
                # Try to initialize Mem0 with proper error handling
                
                # if mem0_host:
                #     print(f"Attempting to connect to Mem0 at: {mem0_host}")
                #     self.memory = Memory(memory_id, host=mem0_host)
                # else:
                #     print("No MEM0_HOST specified, using default")
                #     self.memory = Memory(memory_id)
                self.memory = Memory.from_config({
                    "version": "v1.1",
                    "vector_store": {
                        "provider": "chroma",
                        "config": {
                            "path": "./chromadb"  # thư mục chứa vector index
                        },
                    },
                    "llm": {
                        "provider": "openai",
                        "config": {
                            "api_key": os.environ.get("GOOGLE_API_KEY"),
                            "model": "gemini-2.0-flash"
                        }
                    }
                })
                    
                print("✅ Mem0 memory system initialized successfully")
            except ImportError as e:
                print(f"⚠️ Mem0 package not available: {e}")
                self.memory = MockMemory(memory_id)
            except Exception as e:
                print(f"⚠️ Mem0 initialization failed: {e}")
                print("   This could be due to:")
                print("   - Invalid MEM0_API_KEY")
                print("   - Mem0 server not running at the specified host")
                print("   - Network connectivity issues")
                print("   - Docker services not started")
                print("   Using mock memory system instead")
                self.memory = MockMemory(memory_id)
        else:
            print("⚠️ Mem0 not configured, using mock memory system")
            self.memory = MockMemory(memory_id)
        
    def store_tender_analysis(self, analysis: Dict[str, Any]) -> str:
        """Store tender analysis results."""
        memory_id = f"tender_analysis_{len(self.memory.search('tender_analysis', user_id='default_user'))}"
        self.memory.add(
            memory_id,
            f"Tender Analysis: {json.dumps(analysis, indent=2)}",
            metadata={"type": "tender_analysis", "data": analysis},
            user_id="default_user"
        )
        return memory_id
    
    def store_solution_strategy(self, strategy: Dict[str, Any]) -> str:
        """Store solution strategy and recommendations."""
        memory_id = f"solution_strategy_{len(self.memory.search('solution_strategy', user_id='default_user'))}"
        self.memory.add(
            memory_id,
            f"Solution Strategy: {json.dumps(strategy, indent=2)}",
            metadata={"type": "solution_strategy", "data": strategy},
            user_id="default_user"
        )
        return memory_id
    
    def store_visualization(self, diagram_type: str, mermaid_code: str, description: str) -> str:
        """Store visualization diagrams."""
        memory_id = f"visualization_{diagram_type}_{len(self.memory.search('visualization', user_id='default_user'))}"
        self.memory.add(
            memory_id,
            f"Visualization ({diagram_type}): {description}\n\nMermaid Code:\n{mermaid_code}",
            metadata={
                "type": "visualization",
                "diagram_type": diagram_type,
                "mermaid_code": mermaid_code,
                "description": description
            },
            user_id="default_user"
        )
        return memory_id
    
    def store_project_plan(self, plan: Dict[str, Any]) -> str:
        """Store project planning information."""
        memory_id = f"project_plan_{len(self.memory.search('project_plan', user_id='default_user'))}"
        self.memory.add(
            memory_id,
            f"Project Plan: {json.dumps(plan, indent=2)}",
            metadata={"type": "project_plan", "data": plan},
            user_id="default_user"
        )
        return memory_id
    
    def store_technical_proposal(self, proposal: Dict[str, Any]) -> str:
        """Store the final technical proposal."""
        memory_id = f"technical_proposal_{len(self.memory.search('technical_proposal', user_id='default_user'))}"
        self.memory.add(
            memory_id,
            f"Technical Proposal: {json.dumps(proposal, indent=2)}",
            metadata={"type": "technical_proposal", "data": proposal},
            user_id="default_user"
        )
        return memory_id
    
    def search_memories(self, query: str, memory_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search memories with optional type filtering."""
        # For Mem0, we need to provide at least one of user_id, agent_id, or run_id
        # We'll use a default user_id for now
        try:
            results = self.memory.search(query, user_id="default_user")
        except Exception as e:
            print(f"Search failed: {e}")
            return []
        
        if memory_type:
            filtered_results = []
            for result in results:
                if result.get("metadata", {}).get("type") == memory_type:
                    filtered_results.append({
                        "id": result.get("id"),
                        "content": result.get("content"),
                        "metadata": result.get("metadata", {})
                    })
            return filtered_results
        
        return [{
            "id": result.get("id"),
            "content": result.get("content"),
            "metadata": result.get("metadata", {})
        } for result in results]
    
    def get_latest_memory(self, memory_type: str) -> Optional[Dict[str, Any]]:
        """Get the most recent memory of a specific type."""
        try:
            results = self.memory.search(memory_type, user_id="default_user")
            if results:
                latest = results[-1]  # Assuming results are ordered by recency
                return {
                    "id": latest.get("id"),
                    "content": latest.get("content"),
                    "metadata": latest.get("metadata", {})
                }
        except Exception as e:
            print(f"Failed to get latest memory for {memory_type}: {e}")
        return None
    
    def get_all_memories(self, memory_type: str) -> List[Dict[str, Any]]:
        """Get all memories of a specific type."""
        try:
            results = self.memory.search(memory_type, user_id="default_user")
            return [{
                "id": result.get("id"),
                "content": result.get("content"),
                "metadata": result.get("metadata", {})
            } for result in results]
        except Exception as e:
            print(f"Failed to get all memories for {memory_type}: {e}")
            return []
    
    def clear_memories(self, memory_type: Optional[str] = None):
        """Clear all memories or memories of a specific type."""
        if isinstance(self.memory, MockMemory):
            if memory_type:
                self.memory.memories = [m for m in self.memory.memories 
                                      if m.get("metadata", {}).get("type") != memory_type]
            else:
                self.memory.memories = []
        else:
            print("Note: Clearing memories not implemented for Mem0")
    
    def get_context_summary(self) -> str:
        """Get a summary of all stored information for context."""
        summary_parts = []
        
        # Get tender analysis
        tender_analysis = self.get_latest_memory("tender_analysis")
        if tender_analysis:
            summary_parts.append("Tender Analysis: Available")
        
        # Get solution strategy
        solution_strategy = self.get_latest_memory("solution_strategy")
        if solution_strategy:
            summary_parts.append("Solution Strategy: Available")
        
        # Get visualizations
        visualizations = self.get_all_memories("visualization")
        if visualizations:
            summary_parts.append(f"Visualizations: {len(visualizations)} diagrams")
        
        # Get project plan
        project_plan = self.get_latest_memory("project_plan")
        if project_plan:
            summary_parts.append("Project Plan: Available")
        
        # Get technical proposal
        technical_proposal = self.get_latest_memory("technical_proposal")
        if technical_proposal:
            summary_parts.append("Technical Proposal: Available")
        
        return "\n".join(summary_parts) if summary_parts else "No information stored yet."

# Global shared memory instance
shared_memory = SharedMemory()
