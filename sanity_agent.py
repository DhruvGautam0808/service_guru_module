import logging
from openai import OpenAI
from config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SanityAgent:
    """
    Acts as an intent router. Evaluates a user query and classifies it as a 
    'Deere Question', 'Non Deere Question', or 'Hybrid Question'.
    """
    def __init__(self):
        self.api_key = settings.openai_api_key
        
        # Safely handle missing keys for local testing
        if not self.api_key or self.api_key == "your-openai-key-here":
            logger.warning("No real OPENAI_API_KEY found. Using mock routing.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)

    def classify_intent(self, user_query: str) -> str:
        """
        Uses GPT-4o-Mini to classify the query.
        Returns: 'DEERE', 'NON_DEERE', or 'HYBRID'
        """
        if not self.client:
            # Mock behavior based on simple keywords for safe local testing
            lower_query = user_query.lower()
            
            # Check for the most complex scenario (Hybrid) FIRST
            if ("weather" in lower_query or "rain" in lower_query) and "tractor" in lower_query:
                return "HYBRID"
            # Then check for standard Deere questions
            elif "tractor" in lower_query or "engine" in lower_query:
                return "DEERE"
            # Everything else gets rejected
            else:
                return "NON_DEERE"

        try:
            # The architecture specifies GPT-4o Mini for the Sanity Agent
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "You are a routing assistant for John Deere technicians. "
                            "Classify the user's query into exactly one of these three categories: "
                            "'DEERE' (technical/repair questions about equipment), "
                            "'NON_DEERE' (unrelated questions like math, history, weather), "
                            "or 'HYBRID' (contains both). "
                            "Respond ONLY with the category word."
                        )
                    },
                    {"role": "user", "content": user_query}
                ],
                max_tokens=10,
                temperature=0.0 # Keep temperature at 0 for strict classification
            )
            category = response.choices[0].message.content.strip().upper()
            logger.info(f"Classified query as: {category}")
            return category
        except Exception as e:
            logger.error(f"Routing failed: {e}")
            return "UNKNOWN"

# --- LOCAL TESTING BLOCK ---
if __name__ == "__main__":
    print("\n--- SANITY AGENT ROUTING TEST ---")
    agent = SanityAgent()
    
    # We will test all three scenarios defined in the architecture
    test_queries = [
        "What is the torque spec for a 5075E tractor engine?", # Should be DEERE
        "Who won the super bowl last year?",                   # Should be NON_DEERE
        "My tractor is broken, is it going to rain today?"     # Should be HYBRID
    ]
    
    for q in test_queries:
        print(f"\nUser Query: '{q}'")
        route = agent.classify_intent(q)
        print(f"Routed To: [{route}]")