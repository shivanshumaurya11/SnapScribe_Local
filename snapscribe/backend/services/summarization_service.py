"""
Summarization service module.

Handles:
- Text summarization using HuggingFace Transformers
- HuggingFace Inference API integration
- Batch processing of long texts
"""

import logging
from typing import List, Optional
from transformers import pipeline
from huggingface_hub import InferenceClient

from config.settings import settings

logger = logging.getLogger(__name__)


class SummarizationService:
    """
    Service for text summarization.
    
    Provides methods to:
    - Summarize text using local transformer models
    - Summarize using HuggingFace Inference API
    - Handle long texts through chunking
    """

    def __init__(self) -> None:
        """Initialize summarization service."""
        self._local_summarizer = None
        self._hf_client = None

    def _get_local_summarizer(self):
        """
        Get or initialize local summarization pipeline.
        
        Returns:
            Transformer pipeline for summarization.
        """
        if self._local_summarizer is None:
            logger.info("Initializing local summarization model")
            self._local_summarizer = pipeline(
                "summarization",
                model=settings.HF_SUMMARIZATION_MODEL,
            )
        return self._local_summarizer

    def _get_hf_client(self) -> Optional[InferenceClient]:
        """
        Get or initialize HuggingFace Inference client.
        
        Returns:
            Optional[InferenceClient]: HF client or None if token unavailable.
        """
        if self._hf_client is None:
            token = settings.get_hf_token()
            if not token:
                logger.error("HuggingFace token not available")
                return None
            
            try:
                logger.info("Initializing HuggingFace Inference client")
                self._hf_client = InferenceClient(
                    provider=settings.HF_INFERENCE_PROVIDER,
                    api_key=token,
                )
            except Exception as e:
                logger.error(f"Failed to initialize HF client: {e}", exc_info=True)
                return None
        
        return self._hf_client

    def summarize_text(
        self,
        text: str,
        method: str = "local",
    ) -> Optional[List[str]]:
        """
        Summarize long text by splitting into chunks.
        
        Splits text into chunks of defined size and summarizes each chunk,
        then returns list of summaries.
        
        Args:
            text: Text to summarize.
            method: Summarization method ("local" or "api").
            
        Returns:
            Optional[List[str]]: List of summary texts or None if fails.
        """
        logger.info(f"Starting text summarization (method: {method})")
        logger.debug(f"Input text length: {len(text)} characters")
        
        if not text or len(text.strip()) == 0:
            logger.warning("Empty text provided for summarization")
            return None
        
        # Split text into chunks
        chunk_size = settings.MAX_TRANSCRIPT_CHUNK_SIZE
        chunks = self._chunk_text(text, chunk_size)
        logger.info(f"Split text into {len(chunks)} chunks")
        
        if method == "local":
            return self._summarize_local(chunks)
        elif method == "api":
            return self._summarize_api(chunks)
        else:
            logger.error(f"Unknown summarization method: {method}")
            return None

    def _chunk_text(self, text: str, chunk_size: int) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to chunk.
            chunk_size: Size of each chunk.
            
        Returns:
            List[str]: List of text chunks.
        """
        chunks = []
        for i in range(0, len(text), chunk_size):
            chunk = text[i : i + chunk_size]
            if chunk.strip():
                chunks.append(chunk)
        return chunks

    def _summarize_local(self, chunks: List[str]) -> Optional[List[str]]:
        """
        Summarize chunks using local transformer model.
        
        Args:
            chunks: List of text chunks.
            
        Returns:
            Optional[List[str]]: List of summaries or None if fails.
        """
        logger.info(f"Summarizing {len(chunks)} chunks using local model")
        
        try:
            summarizer = self._get_local_summarizer()
            summaries = []
            
            for i, chunk in enumerate(chunks):
                logger.debug(f"Summarizing chunk {i + 1}/{len(chunks)}")
                try:
                    result = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
                    summary_text = result[0].get("summary_text", "")
                    if summary_text:
                        summaries.append(summary_text)
                        logger.debug(f"Chunk {i + 1} summarized: {len(summary_text)} chars")
                except Exception as e:
                    logger.warning(f"Failed to summarize chunk {i + 1}: {e}")
                    continue
            
            if summaries:
                logger.info(f"Successfully summarized {len(summaries)}/{len(chunks)} chunks")
                return summaries
            else:
                logger.error("No summaries generated")
                return None
                
        except Exception as e:
            logger.error(f"Local summarization failed: {e}", exc_info=True)
            return None

    def _summarize_api(self, chunks: List[str]) -> Optional[List[str]]:
        """
        Summarize chunks using HuggingFace Inference API.
        
        Args:
            chunks: List of text chunks.
            
        Returns:
            Optional[List[str]]: List of summaries or None if fails.
        """
        logger.info(f"Summarizing {len(chunks)} chunks using HF Inference API")
        
        client = self._get_hf_client()
        if not client:
            logger.error("HuggingFace client not available")
            return None
        
        try:
            summaries = []
            
            for i, chunk in enumerate(chunks):
                logger.debug(f"Summarizing chunk {i + 1}/{len(chunks)} via API")
                try:
                    result = client.summarization(
                        chunk,
                        model=settings.HF_SUMMARIZATION_MODEL,
                    )
                    summary_text = result.get("summary_text", "")
                    if summary_text:
                        summaries.append(summary_text)
                        logger.debug(f"Chunk {i + 1} summarized via API")
                except Exception as e:
                    logger.warning(f"Failed to summarize chunk {i + 1} via API: {e}")
                    continue
            
            if summaries:
                logger.info(f"Successfully summarized {len(summaries)}/{len(chunks)} chunks")
                return summaries
            else:
                logger.error("No summaries generated from API")
                return None
                
        except Exception as e:
            logger.error(f"API summarization failed: {e}", exc_info=True)
            return None


# Singleton instance for global use
summarization_service = SummarizationService()
