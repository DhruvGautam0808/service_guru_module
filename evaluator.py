import time
import logging
from retriever import DocumentRetriever

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Evaluator:
    """
    Evaluates the performance and relevancy of the retriever.
    Tracks response time and document scores to prevent model drift.
    """
    def __init__(self):
        # We import the retriever we built earlier!
        self.retriever = DocumentRetriever()
        
    def evaluate_retrieval(self, query: str, index_name: str = "deere-manuals-index") -> float:
        """
        Simulates a retrieval request, measures latency (speed), 
        and calculates the average relevancy score.
        """
        # Start the stopwatch
        start_time = time.time()
        
        # Execute the search
        results = self.retriever.search(index_name=index_name, query_text=query)
        
        # Stop the stopwatch
        end_time = time.time()
        latency = end_time - start_time
        
        # Print our clean evaluation metrics
        print(f"\n--- EVALUATION FOR: '{query}' ---")
        print(f"Latency (Response Time): {latency:.4f} seconds")
        print(f"Valid Blocks Retrieved: {len(results)}")
        
        if results:
            scores = [hit.get('_score', 0.0) for hit in results]
            avg_score = sum(scores) / len(scores)
            print(f"Average Relevance Score: {avg_score:.2f}")
            print(f"Highest Score: {max(scores):.2f}")
        else:
            print("Notice: No valid blocks retrieved to score (Expected if AWS is disconnected).")
            
        return latency

# --- LOCAL TESTING BLOCK ---
if __name__ == "__main__":
    print("Starting Comprehensive Evaluation Suite...")
    evaluator = Evaluator()
    
    # We will test a few common dealer queries
    test_queries = [
        "tractor engine knocking sound", 
        "hydraulic pump pressure low", 
        "transmission fluid leak repair"
    ]
    
    total_latency = 0
    for q in test_queries:
        latency = evaluator.evaluate_retrieval(query=q)
        total_latency += latency
        
    # Calculate our baseline average speed
    avg_latency = total_latency / len(test_queries)
    print(f"\n=====================================")
    print(f"BASELINE AVERAGE LATENCY: {avg_latency:.4f} seconds")
    print(f"=====================================")