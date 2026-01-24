"""
Unified Query Handler
Handles both single and comparison queries using the router
"""
import os
from typing import Dict, List
from langchain_ollama import OllamaLLM
from langchain_chroma import Chroma
from router import QueryRouter, create_db_connection


class QueryHandler:
    """Handles query execution with automatic routing"""
    
    def __init__(self, llm_model: str = "llama3.2:3b"):
        """Initialize handler with router and LLM"""
        self.router = QueryRouter(llm_model=llm_model)
        self.db = create_db_connection()
        # Support environment variable for Ollama URL (useful for Docker)
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.llm = OllamaLLM(model=llm_model, base_url=ollama_base_url)
    
    def query(self, query: str, k: int = 10, verbose: bool = True) -> str:
        """
        Main query function - automatically routes and executes query
        
        Args:
            query: User's question
            k: Number of documents to retrieve per section/album
            verbose: Print routing information
            
        Returns:
            Generated response string
        """
        # Route the query
        routing = self.router.route_query(query)
        
        if verbose:
            print(f"\n🔀 Routing Result:")
            print(f"   Type: {routing['query_type']}")
            print(f"   Sections: {routing['sections']}")
            print(f"   Albums: {routing['albums']}")
            print(f"   Confidence: {routing.get('confidence', 0):.2f}")
            print(f"   Method: {routing.get('method', 'unknown')}\n")
        
        # Execute retrieval based on routing
        if routing["query_type"] == "compare":
            context = self._retrieve_for_comparison(query, routing, k)
            response = self._generate_comparison_response(query, context, routing)
        else:
            context = self._retrieve_single_or_multi(query, routing, k)
            response = self._generate_single_response(query, context, routing)
        
        return response
    
    def _retrieve_for_comparison(self, query: str, routing: Dict, k: int) -> Dict[str, List]:
        """
        Retrieve documents for comparison queries
        Returns dict with keys like "The Link_technical_analysis"
        """
        results = {}
        
        for album in routing["albums"]:
            for section in routing["sections"]:
                key = f"{album}_{section}"
                
                docs = self.db.similarity_search(
                    query,
                    k=k,
                    filter={"$and": [
                        {"album": album},
                        {"section": section}
                    ]}
                )
                
                results[key] = docs
        
        return results
    
    def _retrieve_single_or_multi(self, query: str, routing: Dict, k: int) -> List:
        """Retrieve documents for single or multi-section queries"""
        filters = []
        
        # Build filter conditions
        if routing["albums"] and len(routing["albums"]) == 1:
            filters.append({"album": routing["albums"][0]})
        elif routing["albums"] and len(routing["albums"]) > 1:
            # Multiple albums - use $in operator
            filters.append({"album": {"$in": routing["albums"]}})
        
        if routing["sections"] and len(routing["sections"]) == 1:
            filters.append({"section": routing["sections"][0]})
        elif routing["sections"] and len(routing["sections"]) > 1:
            # Multiple sections - use $in operator
            filters.append({"section": {"$in": routing["sections"]}})
        
        # Execute retrieval
        if filters:
            search_filter = {"$and": filters}
        else:
            search_filter = None
        
        docs = self.db.similarity_search(
            query,
            k=k,
            filter=search_filter
        )
        
        return docs
    
    def _generate_comparison_response(self, query: str, context: Dict[str, List], routing: Dict) -> str:
        """Generate response for comparison queries"""
        # Build context string with clear separation
        context_str = ""
        
        # Group by album
        for album in routing["albums"]:
            album_context_parts = []
            for section in routing["sections"]:
                key = f"{album}_{section}"
                if key in context and context[key]:
                    section_content = "\n\n".join(doc.page_content for doc in context[key])
                    album_context_parts.append(f"[{section.upper()}]\n{section_content}")
            
            if album_context_parts:
                context_str += f"\n\n=== {album.upper()} ===\n"
                context_str += "\n\n".join(album_context_parts)
        
        sections_str = ", ".join(routing["sections"])
        albums_str = " and ".join(routing["albums"])
        
        prompt = f"""You are an expert music analyst comparing Gojira albums. You have detailed information about {albums_str} from their {sections_str} sections. Provide a confident, detailed comparison.

INSTRUCTIONS:
1. Compare {albums_str} based on the {sections_str} information provided below.
2. State similarities and differences directly and confidently.
3. Be specific and detailed - you have comprehensive information available.
4. Structure your response clearly, organizing by aspect (guitar, drums, vocals, etc.) or by album as appropriate.

CONTEXT:
{context_str}

QUESTION:
{query}

ANSWER:
Provide a confident, detailed comparison using the information from both albums. Present your analysis as clear, factual observations.
"""

        response = self.llm.invoke(prompt)
        return response
    
    def _generate_single_response(self, query: str, context: List, routing: Dict) -> str:
        """Generate response for single queries"""
        context_str = "\n\n".join(doc.page_content for doc in context)
        
        sections_str = ", ".join(routing["sections"])
        
        prompt = f"""You are an expert assistant with comprehensive knowledge about Gojira albums from the provided knowledge base. Answer questions directly and confidently using the information provided.

INSTRUCTIONS:
1. Provide direct, confident answers based on the CONTEXT below.
2. The context comes from the {sections_str} section(s) of the knowledge base - you have accurate information to answer the question.
3. For counting questions:
   - Find the complete numbered or itemized list in the context (e.g., "1. Item", "2. Item", ... "11. Item")
   - Count ALL items in the full list - count every numbered item you see
   - Present the count confidently: "There are [number] songs/tracks/items."
4. Be specific and detailed in your answer.
5. Use the exact information from the context - you have the facts needed.

CONTEXT:
{context_str}

QUESTION:
{query}

ANSWER:
Provide a clear, confident answer directly addressing the question. State facts from the context as certainties.
"""

        response = self.llm.invoke(prompt)
        return response

