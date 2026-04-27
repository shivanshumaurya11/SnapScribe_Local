"""
Validation utilities for input validation and error handling.

Handles:
- URL validation
- File path validation
- Parameter validation
"""

import re
from typing import Optional


def validate_youtube_url(url: str) -> bool:
    """
    Validate if URL is a valid YouTube URL.
    
    Args:
        url: URL to validate.
        
    Returns:
        bool: True if valid YouTube URL, False otherwise.
    """
    youtube_patterns = [
        r"(?:https?://)?(?:www\.)?youtube\.com",
        r"(?:https?://)?(?:www\.)?youtu\.be",
        r"youtube\.com/shorts",
        r"youtube\.com/live",
    ]
    return any(re.search(pattern, url) for pattern in youtube_patterns)


def validate_file_path(file_path: str) -> bool:
    """
    Validate if file path is valid and safe.
    
    Args:
        file_path: File path to validate.
        
    Returns:
        bool: True if valid, False otherwise.
    """
    if not file_path or not isinstance(file_path, str):
        return False
    
    # Check for path traversal attacks
    if ".." in file_path:
        return False
    
    return True


def validate_frame_skip(frame_skip: int) -> bool:
    """
    Validate frame skip value.
    
    Args:
        frame_skip: Frame skip value to validate.
        
    Returns:
        bool: True if valid, False otherwise.
    """
    return isinstance(frame_skip, int) and frame_skip > 0


def validate_similarity_threshold(threshold: float) -> bool:
    """
    Validate similarity threshold value.
    
    Args:
        threshold: Similarity threshold (0.0 to 1.0).
        
    Returns:
        bool: True if valid, False otherwise.
    """
    return isinstance(threshold, (int, float)) and 0.0 <= threshold <= 1.0


def extract_video_id_pattern(url: str) -> Optional[str]:
    """
    Extract video ID from various YouTube URL formats using regex patterns.
    
    Supports:
    - youtube.com/shorts/{id}
    - youtu.be/{id}
    - youtube.com/watch?v={id}
    - youtube.com/live/{id}
    
    Args:
        url: YouTube URL.
        
    Returns:
        Optional[str]: Video ID or None if not found.
    """
    patterns = [
        r"shorts/(\w+)",
        r"youtu\.be/([\w\-_]+)(?:\?.*)?",
        r"v=([\w\-_]+)",
        r"live/(\w+)",
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None
