"""
Configuration module for SnapScribe application.

Handles:
- Environment variable loading
- HuggingFace token management
- Directory constants
- Application settings
"""

import os
from typing import Optional
from dotenv import load_dotenv
import streamlit as st

# Load environment variables from .env file
load_dotenv()


class Settings:
    """
    Central configuration class for SnapScribe application.
    
    Manages environment variables, API tokens, and directory paths.
    """

    # Directory paths
    OUTPUT_PDFS_DIR: str = "output_pdfs"
    OUTPUT_DEEPREAD_DIR: str = "output_pdf_deepread"
    VIDEO_FILES_DIR: str = "video_files"

    # HuggingFace settings
    HF_SUMMARIZATION_MODEL: str = "facebook/bart-large-cnn"
    HF_INFERENCE_PROVIDER: str = "auto"

    # Video processing settings
    DEFAULT_FRAME_SKIP: int = 100
    DEFAULT_SIMILARITY_THRESHOLD: float = 1.0

    # Transcript extraction
    MAX_TRANSCRIPT_CHUNK_SIZE: int = 1020

    def __init__(self) -> None:
        """Initialize settings and create required directories."""
        self._ensure_directories()

    @staticmethod
    def _ensure_directories() -> None:
        """Create required output directories if they don't exist."""
        for directory in [
            Settings.OUTPUT_PDFS_DIR,
            Settings.OUTPUT_DEEPREAD_DIR,
            Settings.VIDEO_FILES_DIR,
        ]:
            os.makedirs(directory, exist_ok=True)

    @staticmethod
    def get_hf_token() -> Optional[str]:
        """
        Retrieve HuggingFace API token from multiple sources.
        
        Priority order:
        1. Environment variable (HF_TOKEN)
        2. Streamlit secrets
        3. Session state (user input)
        4. User input via sidebar (for Streamlit Cloud)
        
        Returns:
            Optional[str]: HuggingFace API token or None if not found.
        """
        # 1. Try environment variable (local machine / GitHub Actions)
        token = os.getenv("HF_TOKEN")

        # 2. Try Streamlit secrets (Streamlit Cloud deployment)
        if not token:
            try:
                token = st.secrets["HF_TOKEN"]
            except Exception:
                pass

        # 3. Try session state (user has entered it)
        if not token:
            token = st.session_state.get("HF_TOKEN")

        # 4. Ask user via sidebar if still missing
        if not token:
            token_input = st.sidebar.text_input(
                "🔐 Enter Hugging Face Token:",
                type="password",
                key="hf_token_input",
            )
            if token_input:
                st.session_state["HF_TOKEN"] = token_input
                token = token_input
                st.sidebar.success("Token added to this session.")

        return token


# Global settings instance
settings = Settings()
