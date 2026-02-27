import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Config:
    """
    Centralized configuration to manage environment variables safely.
    """
    def __init__(self):
        # NEW: OpenAI Settings
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")

        # AWS / OpenSearch Settings
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        self.opensearch_endpoint = os.getenv("OPENSEARCH_ENDPOINT", "")
        
        # Ranker Settings
        self.min_retrieval_score = float(os.getenv("MIN_RETRIEVAL_SCORE", "0.5"))
        self.max_retrieval_blocks = int(os.getenv("MAX_RETRIEVAL_BLOCKS", "10"))

        if not self.opensearch_endpoint:
            print("WARNING: OPENSEARCH_ENDPOINT is not set in the .env file.")

# Create a single instance to use across our app
settings = Config()

# --- LOCAL TESTING BLOCK ---
if __name__ == "__main__":
    print("--- CONFIGURATION TEST ---")
    print(f"Region: {settings.aws_region}")
    print(f"Min Score: {settings.min_retrieval_score}")
    print(f"Max Blocks: {settings.max_retrieval_blocks}")