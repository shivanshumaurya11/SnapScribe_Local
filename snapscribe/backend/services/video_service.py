"""
Video processing service module.

Handles:
- Frame extraction from video files
- Unique frame detection using SSIM
- Batch processing of video frames
"""

import logging
from typing import List, Optional
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

from backend.utils.file_utils import ensure_output_directory

logger = logging.getLogger(__name__)


class VideoService:
    """
    Service for video processing operations.
    
    Provides methods to:
    - Extract frames from video files
    - Detect unique frames using SSIM
    - Process video files with configurable parameters
    """

    @staticmethod
    def extract_unique_frames(
        video_path: str,
        output_folder: str,
        frame_skip: int = 100,
        similarity_threshold: float = 1.0,
    ) -> List[str]:
        """
        Extract unique frames from video based on similarity threshold.
        
        Uses Structural Similarity Index (SSIM) to compare consecutive frames
        and extract only frames that differ above the similarity threshold.
        
        Args:
            video_path: Path to video file.
            output_folder: Directory to save extracted frames.
            frame_skip: Number of frames to skip between comparisons.
            similarity_threshold: SSIM threshold (0.0 to 1.0).
                If score < threshold, frame is considered unique.
                0.0 = similar frames, 1.0 = unique frames.
            
        Returns:
            List[str]: Paths to saved frame files.
            
        Raises:
            ValueError: If video file cannot be opened.
            IOError: If frames cannot be written.
        """
        logger.info(f"Starting frame extraction from: {video_path}")
        logger.debug(
            f"Parameters - frame_skip: {frame_skip}, "
            f"similarity_threshold: {similarity_threshold}"
        )
        
        # Ensure output directory exists
        ensure_output_directory(output_folder)
        
        # Open video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            logger.error(f"Failed to open video file: {video_path}")
            raise ValueError(f"Cannot open video file: {video_path}")
        
        prev_frame: Optional[np.ndarray] = None
        frame_count = 0
        saved_frames: List[str] = []
        frames_compared = 0
        frames_saved = 0

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                # Process every nth frame based on frame_skip
                if frame_count % frame_skip == 0:
                    # Convert to grayscale for comparison
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    
                    # Save first frame or compare with previous
                    if prev_frame is None:
                        saved_path = VideoService._save_frame(
                            frame, output_folder, frame_count
                        )
                        if saved_path:
                            saved_frames.append(saved_path)
                            frames_saved += 1
                        prev_frame = gray
                    else:
                        # Compare with previous frame using SSIM
                        frames_compared += 1
                        try:
                            score, _ = ssim(prev_frame, gray, full=True)
                            logger.debug(f"Frame {frame_count} SSIM score: {score:.4f}")
                            
                            # Save if dissimilar enough
                            if score < similarity_threshold:
                                saved_path = VideoService._save_frame(
                                    frame, output_folder, frame_count
                                )
                                if saved_path:
                                    saved_frames.append(saved_path)
                                    frames_saved += 1
                                prev_frame = gray
                        except Exception as e:
                            logger.warning(
                                f"Failed to compare frames at {frame_count}: {e}"
                            )

                frame_count += 1

        finally:
            cap.release()
        
        logger.info(
            f"Frame extraction completed. "
            f"Total frames: {frame_count}, "
            f"Frames compared: {frames_compared}, "
            f"Frames saved: {frames_saved}"
        )
        
        return saved_frames

    @staticmethod
    def _save_frame(frame: np.ndarray, output_folder: str, frame_number: int) -> Optional[str]:
        """
        Save individual frame to disk.
        
        Args:
            frame: OpenCV frame (BGR format).
            output_folder: Directory to save frame.
            frame_number: Frame sequence number for filename.
            
        Returns:
            Optional[str]: Path to saved frame or None if save failed.
        """
        try:
            frame_filename = f"frame_{frame_number}.jpg"
            frame_path = f"{output_folder}/{frame_filename}"
            
            success = cv2.imwrite(frame_path, frame)
            if success:
                logger.debug(f"Saved frame: {frame_path}")
                return frame_path
            else:
                logger.warning(f"Failed to write frame: {frame_path}")
                return None
                
        except Exception as e:
            logger.error(f"Error saving frame {frame_number}: {e}", exc_info=True)
            return None

    @staticmethod
    def get_video_duration(video_path: str) -> Optional[float]:
        """
        Get video duration in seconds.
        
        Args:
            video_path: Path to video file.
            
        Returns:
            Optional[float]: Duration in seconds or None if unavailable.
        """
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                return None
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            cap.release()
            
            if fps > 0:
                duration = frame_count / fps
                logger.debug(f"Video duration: {duration:.2f}s")
                return duration
            
            return None
            
        except Exception as e:
            logger.warning(f"Failed to get video duration: {e}")
            return None


# Singleton instance for global use
video_service = VideoService()
