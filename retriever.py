import logging
import boto3
from typing import List, Dict, Any
from opensearchpy import OpenSearch, RequestsHttpConnection, AWSV4SignerAuth
from config import settings  

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentRetriever:
    """
    Handles retrieving and ranking documents from AWS OpenSearch.
    Enforces a strict threshold to reduce downstream token consumption.
    """
    def __init__(self):
        self.min_score = settings.min_retrieval_score
        self.max_blocks = settings.max_retrieval_blocks
        
        # Clean up the endpoint string if it contains https://
        self.host = settings.opensearch_endpoint.replace("https://", "")
        self.region = settings.aws_region

        # Initialize AWS OpenSearch connection
        try:
            # This looks for AWS credentials on your local machine
            credentials = boto3.Session().get_credentials()
            
            if not credentials:
                logger.warning("No AWS credentials found. OpenSearch will not connect.")
                self.client = None
            else:
                auth = AWSV4SignerAuth(credentials, self.region, 'es')
                self.client = OpenSearch(
                    hosts=[{'host': self.host, 'port': 443}],
                    http_auth=auth,
                    use_ssl=True,
                    verify_certs=True,
                    connection_class=RequestsHttpConnection
                )
                logger.info("OpenSearch client initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to setup OpenSearch client: {e}")
            self.client = None

    def filter_and_rank_blocks(self, raw_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filters raw results based on the acceptance criteria: > min_score and <= max_blocks.
        """
        valid_blocks = []
        for hit in raw_results:
            score = hit.get('_score', 0.0)
            if score > self.min_score:
                valid_blocks.append(hit)
            if len(valid_blocks) >= self.max_blocks:
                break
                
        logger.info(f"Filtered {len(raw_results)} raw results down to {len(valid_blocks)} valid blocks.")
        return valid_blocks

    def search(self, index_name: str, query_text: str) -> List[Dict[str, Any]]:
        """
        Queries OpenSearch and automatically applies our token-saving filter.
        """
        if not self.client:
            logger.error("Cannot perform search: OpenSearch client is not connected.")
            return []
            
        # Standard OpenSearch vector query format
        query_body = {
            "query": {
                "match": {
                    "text_field": query_text
                }
            }
        }
        
        try:
            response = self.client.search(body=query_body, index=index_name)
            raw_hits = response.get('hits', {}).get('hits', [])
            return self.filter_and_rank_blocks(raw_hits)
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

# --- LOCAL TESTING BLOCK ---
if __name__ == "__main__":
    print("\n--- AWS CONNECTION TEST ---")
    retriever = DocumentRetriever()
    
    # We will attempt a search. Since we don't have real Deere credentials, 
    # we expect this to gracefully fail rather than crashing!
    results = retriever.search(index_name="deere-manuals-index", query_text="tractor engine repair")
    
    print(f"\nSearch attempt finished. Blocks returned: {len(results)}")