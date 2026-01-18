"""
Unified Query Script - Handles all query types automatically
- Single queries: "How many songs are in The Link?"
- Comparison queries: "Compare technical analysis between both albums"
- Multi-section queries: "Tell me about production and recording"

The router automatically detects query type, sections, and albums - no manual specification needed!
"""
import sys
from query_handler import QueryHandler

# Initialize query handler (includes router + DB + LLM)
handler = QueryHandler(llm_model="llama3")

# Get query from command line or use default
if len(sys.argv) > 1:
    query = " ".join(sys.argv[1:])
else:
    # Default query (can be single, comparison, or multi-section)
    print("Usage: python query.py 'your question here'")
    print("\nExamples:")
    print("  python query.py 'How many songs are in The Link?'")
    print("  python query.py 'Compare technical analysis between both albums'")
    print("  python query.py 'What is the guitar work like on From Mars to Sirius?'")
    print("\nRunning default query...\n")
    query = "How many songs are in the album The Link?"

# Execute query with automatic routing
# Router will automatically detect if it's a comparison, single, or multi-section query
print(f"\n📝 Query: {query}\n")
response = handler.query(query, k=10, verbose=True)

print("\n🤖 Answer:\n")
print(response)
