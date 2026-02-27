import logging
from openai import OpenAI
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QueryExpander:
    """
    Expands short user queries into detailed technical queries using OpenAI.
    This improves OpenSearch retrieval scores to meet the > 0.5 threshold.
    """
    def __init__(self):
        self.api_key = settings.openai_api_key
        
        # If no real key is provided, we will gracefully handle it for local testing
        if not self.api_key or self.api_key == "your-openai-key-here":
            logger.warning("No real OPENAI_API_KEY found. Using mock expansion.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)

    def expand_query(self, raw_query: str) -> str:
        """
        Takes a simple query and uses GPT-4o Mini to add technical synonyms.
        """
        if not self.client:
            # Mock behavior for safe local testing
            return f"{raw_query} technical diagnostic repair manual John Deere"

        try:
            # Using the fast, cheap model specified in the architecture diagram
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a John Deere technical assistant. Expand the user's short query into a detailed search query suitable for a vector database. Include relevant technical synonyms."},
                    {"role": "user", "content": raw_query}
                ],
                max_tokens=50,
                temperature=0.3
            )
            expanded = response.choices[0].message.content.strip()
            logger.info(f"Successfully expanded query.")
            return expanded
        except Exception as e:
            logger.error(f"Failed to expand query: {e}")
            return raw_query

# --- LOCAL TESTING BLOCK ---
if __name__ == "__main__":
    print("\n--- QUERY EXPANSION TEST ---")
    expander = QueryExpander()
    
    test_query = "tractor knocking"
    print(f"Original User Query: '{test_query}'")
    
    expanded_query = expander.expand_query(test_query)
    print(f"Expanded Search Query: '{expanded_query}'")
