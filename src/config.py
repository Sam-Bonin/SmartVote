"""
Centralized configuration for the SmartVote application.
This file contains all hyperparameters and configuration values
shared across different modules.
"""

# API parameters
API_URL = "http://localhost:8000"  # Base URL for the API
API_HOST = "0.0.0.0"  # Host address for the API server
API_PORT = 8000  # Port for the API server

# Retrieval parameters
TOP_N_DOCUMENTS = 3  # Number of documents to retrieve and analyze
SIMILARITY_THRESHOLD = 0.5  # Minimum similarity score to include a document

# Cache settings
MAX_CACHE_SIZE = 100  # Maximum size for query and embedding caches

# Token limits for analyzer
MAX_TOKENS_TOTAL = 4000  # Maximum tokens for the model's context
MAX_TOKENS_OUTPUT = 600  # Maximum tokens for the output
MAX_TOKENS_PROMPT = MAX_TOKENS_TOTAL - MAX_TOKENS_OUTPUT  # Reserve space for output
SYSTEM_MESSAGE_TOKENS = 100  # Approximate token count for system message
PROMPT_TEMPLATE_TOKENS = 200  # Approximate tokens for the prompt template
CHARS_PER_TOKEN = 4  # Rough estimate: 1 token is about 4 characters in English text

# Token limits for embedding
EMBEDDING_MAX_TOKENS = 8000  # Approximate limit for text-embedding-ada-002

# PDF processing parameters
MIN_TEXT_LENGTH = 50  # Minimum length of text to consider a page worth processing

# AI Models
ANALYSIS_MODEL = "gpt-4o-mini"  # Model for analysis generation
EMBEDDING_MODEL = "text-embedding-ada-002"  # Model for embedding generation 