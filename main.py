import logging
from sanity_agent import SanityAgent
from retriever import DocumentRetriever

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AMServiceAssistant:
    """
    The main orchestrator for the AM Service AI Assistant.
    Routes queries, expands them, and retrieves optimized documents.
    """
    def __init__(self):
        logger.info("Initializing AM Service Assistant Pipeline...")
        self.sanity_agent = SanityAgent()
        # The DocumentRetriever automatically initializes our QueryExpander!
        self.retriever = DocumentRetriever()
        self.index_name = "deere-manuals-index"

    def process_query(self, user_query: str) -> dict:
        """
        Processes a user query end-to-end based on the Agentic Framework.
        """
        print(f"\n==================================================")
        logger.info(f"NEW REQUEST RECEIVED")
        logger.info(f"User Query: '{user_query}'")
        
        # Step 1: Intent Identification (Sanity Agent)
        intent = self.sanity_agent.classify_intent(user_query)
        
        # Step 2: Routing based on intent
        if intent == "NON_DEERE":
            logger.warning("Query blocked by Sanity Agent. Saving tokens.")
            return {
                "status": "rejected",
                "reason": "Non-Deere query",
                "message": "I am a Service Guru assistant specialized in John Deere equipment. I cannot assist with this topic.",
                "blocks": []
            }
        
        # Step 3: Retrieval for DEERE and HYBRID questions
        logger.info(f"Query approved ({intent}). Proceeding to Retrieval pipeline...")
        # Note: The retriever automatically expands the query before hitting OpenSearch
        results = self.retriever.search(index_name=self.index_name, query_text=user_query)
        
        return {
            "status": "success",
            "intent": intent,
            "message": f"Successfully retrieved {len(results)} highly relevant document blocks.",
            "blocks": results
        }

# --- LOCAL END-TO-END TESTING BLOCK ---
if __name__ == "__main__":
    print("\n=== AM SERVICE AI - END-TO-END PIPELINE TEST ===")
    assistant = AMServiceAssistant()
    
    # We will test our pipeline with one bad query and one good query
    test_queries = [
        "What is the capital of France?",
        "tractor engine repair"
    ]
    
    for q in test_queries:
        response = assistant.process_query(q)
        print(f"--> Final Assistant Status: {response['status'].upper()}")
        print(f"--> Final Assistant Message: {response['message']}")