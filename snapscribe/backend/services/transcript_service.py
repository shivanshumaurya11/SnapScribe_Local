"""
Transcript extraction service module.

Handles:
- YouTube transcript fetching
- Transcript formatting and processing
"""

import logging
from typing import Optional
from youtube_transcript_api import YouTubeTranscriptApi

from backend.services.youtube_service import youtube_service

logger = logging.getLogger(__name__)


class TranscriptService:
    """
    Service for transcript extraction from YouTube videos.
    
    Provides methods to:
    - Fetch transcripts from YouTube videos
    - Format transcript data
    - Handle missing transcripts
    """

    @staticmethod
    def extract_transcript(youtube_url: str) -> Optional[str]:
        """
        Extract transcript text from YouTube video.
        
        Args:
            youtube_url: YouTube video URL.
            
        Returns:
            Optional[str]: Transcript text or None if extraction fails.
            
        Raises:
            Exception: If transcript API fails.
        """
        logger.info(f"Extracting transcript from: {youtube_url}")
        
        # Get video ID from URL
        video_id = youtube_service.get_video_id(youtube_url)
        if not video_id:
            logger.error(f"Could not extract video ID from: {youtube_url}")
            return None
        
        logger.debug(f"Video ID: {video_id}")
        
        try:
            # Fetch raw transcript data
            yt_api = YouTubeTranscriptApi()
            transcript_data = yt_api.fetch(video_id).to_raw_data()
            logger.info(f"Successfully fetched transcript with {len(transcript_data)} entries")
            
            # Combine transcript entries into single text
            transcript_text = ""
            for entry in transcript_data:
                transcript_text += " " + entry.get("text", "")
            
            transcript_text = transcript_text.strip()
            logger.debug(f"Transcript length: {len(transcript_text)} characters")
            
            return transcript_text
            
        except Exception as e:
            logger.error(f"Failed to extract transcript: {e}", exc_info=True)
            return None

    @staticmethod
    def is_transcript_available(video_id: str) -> bool:
        """
        Check if transcript is available for video.
        
        Args:
            video_id: YouTube video ID.
            
        Returns:
            bool: True if transcript available, False otherwise.
        """
        try:
            yt_api = YouTubeTranscriptApi()
            yt_api.fetch(video_id)
            logger.info(f"Transcript available for video: {video_id}")
            return True
        except Exception as e:
            logger.warning(f"Transcript not available for {video_id}: {e}")
            return False


# Singleton instance for global use
transcript_service = TranscriptService()
