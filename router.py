"""
Query Router for RAG System
Automatically routes queries to appropriate sections and albums
"""
import json
import os
import re
from typing import Dict, List, Optional
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


class QueryRouter:
    """Routes queries to appropriate sections and albums based on intent"""
    
    # Available sections in the database
    AVAILABLE_SECTIONS = [
        "tracklist",
        "overview", 
        "musical_characteristics",
        "lyrics_themes",
        "reception_influence",
        "technical_analysis",
        "cultural_context",
        "recording_production",
        "live_history",
        "commercial_performance",
        "philosophy",
        "conclusion",
        "artistic_achievement",
        "basic_info"
    ]
    
    # Available albums
    AVAILABLE_ALBUMS = [
        "The Link",
        "From Mars to Sirius"
    ]
    
    # Section keywords mapping for fallback
    SECTION_KEYWORDS = {
        "tracklist": ["track", "song", "song list", "tracks", "songs", "how many songs"],
        "overview": ["overview", "summary", "general", "about", "introduction"],
        "musical_characteristics": ["musical", "sound", "style", "musical style", "characteristics"],
        "lyrics_themes": ["lyric", "theme", "lyrical", "themes", "meaning", "lyrics", "lyrical themes"],
        "reception_influence": ["reception", "critic", "review", "influence", "reviews", "critical"],
        "technical_analysis": ["technical", "guitar", "drum", "bass", "vocal", "performance", "technique", "instrument"],
        "cultural_context": ["cultural", "culture", "impact", "society", "cultural impact"],
        "recording_production": ["recording", "production", "studio", "producer", "recorded", "mixed"],
        "live_history": ["live", "concert", "performance", "tour", "venue", "live performance"],
        "commercial_performance": ["commercial", "sales", "chart", "success", "sold"],
        "philosophy": ["philosophy", "philosophical", "meaning", "spiritual", "wisdom", "consciousness"],
        "conclusion": ["conclusion", "summary", "overall", "final"],
        "artistic_achievement": ["achievement", "artistic", "accomplishment", "success", "legacy"],
        "basic_info": ["release", "date", "label", "genre", "length", "band members", "producer", "when was", "basic"]
    }
    
    def __init__(self, llm_model: str = "llama3.2:7b"):
        """Initialize router with LLM"""
        # Support environment variable for Ollama URL (useful for Docker)
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.llm = OllamaLLM(model=llm_model, base_url=ollama_base_url)
        self.confidence_threshold = 0.7
    
    def route_query(self, query: str) -> Dict:
        """
        Main routing function - classifies query and returns routing information
        
        Returns:
            {
                "query_type": "single" | "compare" | "multi_section",
                "sections": List[str],
                "albums": List[str],
                "confidence": float,
                "method": "llm" | "keyword_fallback"
            }
        """
        # Try LLM-based routing first
        routing_result = self._classify_with_llm(query)
        
        # Fallback to keyword-based if confidence is low
        if routing_result.get("confidence", 0) < self.confidence_threshold:
            routing_result = self._classify_with_keywords(query)
            routing_result["method"] = "keyword_fallback"
        
        return routing_result
    
    def _classify_with_llm(self, query: str) -> Dict:
        """Uses LLM to classify query intent and extract routing parameters"""
        
        sections_str = ", ".join(self.AVAILABLE_SECTIONS)
        albums_str = ", ".join(self.AVAILABLE_ALBUMS)
        
        prompt = f"""Analyze this query about Gojira albums: "{query}"

Your task is to determine:
1. Query type: Is this comparing albums ("compare"), asking about one specific thing ("single"), or covering multiple sections ("multi_section")?
2. Relevant sections: Which sections would contain the answer? Available: {sections_str}
3. Albums mentioned: Which album(s)? Options: {albums_str}, or "both" if comparing

Detect comparison keywords: compare, comparison, difference, differences, vs, versus, both albums, both, between

For sections, consider:
- Tracklist questions → "tracklist"
- Guitar/drum/bass/technical → "technical_analysis"  
- Musical style/sound → "musical_characteristics"
- Lyrics/meaning/themes → "lyrics_themes"
- Reviews/critical → "reception_influence"
- Recording/production → "recording_production"
- Live/concerts → "live_history"
- Sales/commercial → "commercial_performance"
- Philosophy/spiritual → "philosophy"
- General/about → "overview"

Output ONLY valid JSON in this exact format:
{{
    "query_type": "single" or "compare" or "multi_section",
    "sections": ["section1", "section2"],
    "albums": ["album1"] or ["The Link", "From Mars to Sirius"],
    "confidence": 0.0-1.0
}}

Be specific with sections. If unsure about section, default to ["overview"]. If comparing, include both albums."""

        try:
            raw_response = self.llm.invoke(prompt).strip()
            
            # Clean JSON response (remove markdown code blocks if present)
            response = re.sub(r'```json\n?', '', raw_response)
            response = re.sub(r'```\n?', '', response)
            response = response.strip()
            
            # Try to extract JSON object from response (LLM might add explanatory text)
            # First try: find JSON object with query_type key
            json_match = re.search(r'\{(?:[^{}]|(?:\{[^{}]*\}))*"query_type"(?:[^{}]|(?:\{[^{}]*\}))*\}', response, re.DOTALL)
            
            # Second try: find any complete JSON object (balance braces)
            if not json_match:
                # Find first { and match to matching }
                start = response.find('{')
                if start != -1:
                    brace_count = 0
                    end = start
                    for i in range(start, len(response)):
                        if response[i] == '{':
                            brace_count += 1
                        elif response[i] == '}':
                            brace_count -= 1
                            if brace_count == 0:
                                end = i + 1
                                break
                    if end > start:
                        response = response[start:end]
                    # Otherwise, response stays as-is
            else:
                response = json_match.group(0)
            
            result = json.loads(response)
            
            # Validate and normalize
            result = self._validate_routing_result(result)
            result["method"] = "llm"
            
            return result
            
        except (json.JSONDecodeError, Exception) as e:
            # Fallback to keyword-based routing on LLM failure
            print(f"⚠️  LLM routing failed: {e}, using keyword fallback")
            return self._classify_with_keywords(query)
    
    def _classify_with_keywords(self, query: str) -> Dict:
        """Fallback keyword-based routing when LLM fails or confidence is low"""
        query_lower = query.lower()
        
        # Detect comparison
        compare_keywords = ["compare", "comparison", "difference", "differences", "vs", "versus", "both albums", "both"]
        is_comparison = any(keyword in query_lower for keyword in compare_keywords)
        
        # Detect albums
        albums = []
        if "link" in query_lower and "mars" not in query_lower:
            albums = ["The Link"]
        elif ("mars" in query_lower or "sirius" in query_lower) and "link" not in query_lower:
            albums = ["From Mars to Sirius"]
        elif is_comparison or "both" in query_lower:
            albums = self.AVAILABLE_ALBUMS.copy()
        else:
            # Default to both if unclear
            albums = self.AVAILABLE_ALBUMS.copy()
        
        # Match sections based on keywords
        sections = []
        section_scores = {}
        
        for section, keywords in self.SECTION_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                section_scores[section] = score
        
        if section_scores:
            # Get top matching sections
            sorted_sections = sorted(section_scores.items(), key=lambda x: x[1], reverse=True)
            sections = [section for section, score in sorted_sections[:2]]  # Top 2 matches
        else:
            # Default to overview if no matches
            sections = ["overview"]
        
        query_type = "compare" if is_comparison else "single"
        
        return {
            "query_type": query_type,
            "sections": sections,
            "albums": albums,
            "confidence": 0.6,  # Lower confidence for keyword-based
            "method": "keyword_fallback"
        }
    
    def _validate_routing_result(self, result: Dict) -> Dict:
        """Validates and normalizes routing result"""
        # Ensure query_type is valid
        if result.get("query_type") not in ["single", "compare", "multi_section"]:
            result["query_type"] = "single"
        
        # Ensure sections are valid
        sections = result.get("sections", [])
        valid_sections = [s for s in sections if s in self.AVAILABLE_SECTIONS]
        if not valid_sections:
            valid_sections = ["overview"]  # Default fallback
        result["sections"] = valid_sections
        
        # Ensure albums are valid
        albums = result.get("albums", [])
        # Handle "both" or case variations
        if isinstance(albums, str):
            if albums.lower() in ["both", "both albums"]:
                albums = self.AVAILABLE_ALBUMS.copy()
            else:
                albums = [albums]
        
        valid_albums = []
        for album in albums:
            # Case-insensitive matching
            for available_album in self.AVAILABLE_ALBUMS:
                if album.lower() == available_album.lower():
                    valid_albums.append(available_album)
                    break
        
        if not valid_albums:
            # If comparing, default to both; otherwise default to first
            if result["query_type"] == "compare":
                valid_albums = self.AVAILABLE_ALBUMS.copy()
            else:
                valid_albums = self.AVAILABLE_ALBUMS.copy()
        
        result["albums"] = valid_albums
        
        # Ensure confidence is set
        if "confidence" not in result or not isinstance(result["confidence"], (int, float)):
            result["confidence"] = 0.8 if result.get("method") == "llm" else 0.6
        
        return result


def create_db_connection():
    """Helper function to create database connection"""
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(
        persist_directory="gojiraDB",
        embedding_function=embeddings
    )
    return db

