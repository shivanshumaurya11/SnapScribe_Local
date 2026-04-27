"""
YouTube service module.

Handles:
- YouTube video metadata extraction
- Video downloading
- Playlist processing
- Video ID extraction
"""

import logging
from typing import Optional, List
import yt_dlp

from backend.utils.validators import extract_video_id_pattern

logger = logging.getLogger(__name__)


class YouTubeService:
    """
    Service for YouTube-related operations.
    
    Provides methods to:
    - Extract video metadata
    - Download videos
    - Handle playlists
    - Extract video IDs
    """

    # Default yt_dlp options for downloads
    DEFAULT_DOWNLOAD_OPTS = {
        "outtmpl": "",
        "format": "bv*[height<=720]+bestaudio/best[height<=720]",
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "no_warnings": True,
        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-us,en;q=0.5",
            "Sec-Fetch-Mode": "navigate",
        },
        "retries": 5,
        "fragment_retries": 5,
        "ignoreerrors": True,
        "ratelimit": 1000000,
    }

    @staticmethod
    def get_video_id(url: str) -> Optional[str]:
        """
        Extract video ID from YouTube URL.
        
        Supports multiple URL formats:
        - YouTube Shorts
        - youtu.be shortened URLs
        - Regular YouTube URLs
        - YouTube live streams
        
        Args:
            url: YouTube URL.
            
        Returns:
            Optional[str]: Video ID or None if extraction fails.
        """
        logger.debug(f"Extracting video ID from URL: {url}")
        video_id = extract_video_id_pattern(url)
        
        if video_id:
            logger.info(f"Successfully extracted video ID: {video_id}")
        else:
            logger.warning(f"Failed to extract video ID from: {url}")
        
        return video_id

    @staticmethod
    def get_video_title(url: str) -> Optional[str]:
        """
        Fetch video title from YouTube.
        
        Args:
            url: YouTube video URL.
            
        Returns:
            Optional[str]: Video title (sanitized) or None if fetch fails.
            
        Raises:
            Exception: If yt_dlp fails to fetch metadata.
        """
        logger.info(f"Fetching video title for: {url}")
        
        ydl_opts = {
            "skip_download": True,
            "ignoreerrors": True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                video_info = ydl.extract_info(url, download=False)
                title = video_info.get("title", "video")
                
                # Sanitize title for file system
                invalid_chars = r'<>:"/\\|?*'
                for char in invalid_chars:
                    title = title.replace(char, "-")
                title = title.strip(".")
                
                logger.info(f"Successfully fetched title: {title}")
                return title
                
        except Exception as e:
            logger.error(f"Failed to fetch video title: {e}", exc_info=True)
            return None

    @staticmethod
    def download_video(url: str, output_path: str) -> Optional[str]:
        """
        Download YouTube video.
        
        Downloads in H.264 video with AAC audio, max 720p resolution,
        merged into MP4 container.
        
        Args:
            url: YouTube video URL.
            output_path: Path where video will be saved (without extension).
            
        Returns:
            Optional[str]: Output path if successful, None otherwise.
            
        Raises:
            Exception: If download fails.
        """
        logger.info(f"Starting video download: {url}")
        logger.debug(f"Output path: {output_path}")
        
        ydl_opts = YouTubeService.DEFAULT_DOWNLOAD_OPTS.copy()
        ydl_opts["outtmpl"] = output_path
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            logger.info(f"Video downloaded successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Video download failed: {e}", exc_info=True)
            return None

    @staticmethod
    def get_playlist_videos(playlist_url: str, max_videos: int = 1000) -> List[str]:
        """
        Extract all video URLs from a YouTube playlist.
        
        Args:
            playlist_url: Playlist URL.
            max_videos: Maximum number of videos to fetch.
            
        Returns:
            List[str]: List of video URLs.
            
        Raises:
            Exception: If playlist extraction fails.
        """
        logger.info(f"Extracting videos from playlist: {playlist_url}")
        
        ydl_opts = {
            "ignoreerrors": True,
            "playlistend": max_videos,
            "extract_flat": True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                playlist_info = ydl.extract_info(playlist_url, download=False)
                video_urls = [entry["url"] for entry in playlist_info["entries"]]
                logger.info(f"Successfully extracted {len(video_urls)} videos")
                return video_urls
                
        except Exception as e:
            logger.error(f"Playlist extraction failed: {e}", exc_info=True)
            return []


# Singleton instance for global use
youtube_service = YouTubeService()
