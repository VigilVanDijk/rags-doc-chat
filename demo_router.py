"""
Demo script showing the router in action
Tests various query types to demonstrate automatic routing
"""
from query_handler import QueryHandler

# Initialize handler
handler = QueryHandler(llm_model="llama3")

# Test queries demonstrating different routing scenarios
test_queries = [
    # Single album, specific section
    "How many songs are in The Link?",
    
    # Single album, inferred section
    "What is the guitar work like on From Mars to Sirius?",
    
    # Comparison query - automatic detection
    "Compare the technical analysis between The Link and From Mars to Sirius",
    
    # Comparison without explicit "compare" keyword
    "What are the differences in lyrical themes between both albums?",
    
    # Multi-section query
    "Tell me about the production and recording of The Link",
    
    # General query (defaults to overview)
    "What is The Link album about?",
]

print("=" * 70)
print("ROUTER DEMO - Automatic Query Routing")
print("=" * 70)

for i, query in enumerate(test_queries, 1):
    print(f"\n{'='*70}")
    print(f"Test {i}: {query}")
    print(f"{'='*70}")
    
    response = handler.query(query, k=5, verbose=True)
    
    print(f"\n📋 Response Preview:")
    print(response[:300] + "..." if len(response) > 300 else response)
    print("\n" + "-"*70)

print("\n" + "="*70)
print("Demo Complete!")
print("="*70)

