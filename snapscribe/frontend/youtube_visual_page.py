"""
YouTube to Visual Summaries page.

Handles:
- YouTube video/playlist URL input
- Video downloading
- Frame extraction
- PDF generation from frames
"""

import logging
import os
import tempfile
import streamlit as st

from backend.services.youtube_service import youtube_service
from backend.services.video_service import video_service
from backend.services.pdf_service import pdf_service
from config.settings import settings
from backend.utils.validators import validate_youtube_url

logger = logging.getLogger(__name__)


def render() -> None:
    """
    Render YouTube video to visual summaries page.
    
    Allows users to:
    - Input YouTube video/playlist URL
    - Download videos
    - Extract key frames
    - Create PDF visual summaries
    - Download PDF
    """
    st.set_page_config(
        page_title="SnapScribe : YouTube Visual Converter",
        page_icon="🎥",
        layout="wide",
    )

    st.title("SnapScribe : Next-Gen YouTube to Visual Summaries Converter")
    st.write(
        "Convert YouTube videos and playlists into summarized visual PDFs with key frames."
    )

    url = st.text_input("Enter YouTube Playlist/Video URL")

    col1, col2, col3 = st.columns(3)

    with col1:
        frame_skip = int(
            st.number_input(
                "Frame Skip Value:",
                value=100,
                min_value=1,
                help="Higher = faster but may miss frames",
            )
        )

    with col2:
        similarity_threshold = float(
            st.number_input(
                "Similarity Threshold:",
                value=1.0,
                min_value=0.0,
                max_value=1.0,
                step=0.1,
                help="0=similar, 1=unique frames",
            )
        )

    with col3:
        keep_video = st.checkbox(
            "Keep downloaded video",
            value=False,
            help="Uncheck to delete video after processing",
        )

    if st.button("🎬 Generate Visual Notes"):
        if not url:
            st.error("Please enter a YouTube URL")
            return

        if not validate_youtube_url(url):
            st.error("Please enter a valid YouTube URL")
            return

        with st.spinner("Processing YouTube content..."):
            video_id = youtube_service.get_video_id(url)

            if video_id:
                # Single video
                _process_single_video(
                    url, video_id, frame_skip, similarity_threshold, keep_video
                )
            else:
                # Try as playlist
                _process_playlist(
                    url, frame_skip, similarity_threshold, keep_video
                )

    # ---------------------- FOOTER ----------------------
    st.markdown(
        """
        <div style="text-align:center; margin-top:38px; color:black; font-size:15px;">
            Made with ❤️ by <b>SnapScribe</b> • Secure • Fast • Beautiful<br>
            <span style="font-size:13px;opacity:0.8;color:black;">Your files are never stored. All processing is done securely.</span>
        </div>
    """,
        unsafe_allow_html=True,
    )


def _process_single_video(
    url: str,
    video_id: str,
    frame_skip: int,
    similarity_threshold: float,
    keep_video: bool,
) -> None:
    """
    Process a single YouTube video.
    
    Args:
        url: Video URL
        video_id: Extracted video ID
        frame_skip: Frame skip value
        similarity_threshold: Similarity threshold
        keep_video: Whether to keep downloaded video
    """
    st.video(f"https://www.youtube.com/watch?v={video_id}")

    title = youtube_service.get_video_title(url)
    if not title:
        st.error("Failed to fetch video title")
        return

    st.info(f"Downloading video: {title}")
    video_file = youtube_service.download_video(
        url, f"{settings.VIDEO_FILES_DIR}/{title}.mp4"
    )

    if not video_file:
        st.error("Failed to download video")
        return

    st.info(f"Extracting frames from: {title}")

    with tempfile.TemporaryDirectory() as temp_folder:
        frames = video_service.extract_unique_frames(
            video_file, temp_folder, frame_skip, similarity_threshold
        )

        if frames:
            st.success(f"Extracted {len(frames)} unique frames")
            output_pdf_name = f"{title}.pdf"
            output_pdf_path = os.path.join(settings.OUTPUT_PDFS_DIR, output_pdf_name)

            st.info("Creating PDF...")
            success = pdf_service.frames_to_pdf(output_pdf_path, frames, title)

            if success:
                st.success(f"✅ PDF saved: {output_pdf_path}")

                with open(output_pdf_path, "rb") as pdf_file:
                    st.download_button(
                        "📥 Download PDF",
                        data=pdf_file.read(),
                        file_name=output_pdf_name,
                        mime="application/pdf",
                    )
                st.balloons()
            else:
                st.error("Failed to create PDF")
        else:
            st.warning("No frames extracted from video")

    # Cleanup video if not keeping
    if not keep_video and os.path.exists(video_file):
        try:
            os.remove(video_file)
            st.info("Video file deleted")
        except Exception as e:
            logger.warning(f"Failed to delete video: {e}")


def _process_playlist(
    playlist_url: str,
    frame_skip: int,
    similarity_threshold: float,
    keep_video: bool,
) -> None:
    """
    Process all videos in a YouTube playlist.
    
    Args:
        playlist_url: Playlist URL
        frame_skip: Frame skip value
        similarity_threshold: Similarity threshold
        keep_video: Whether to keep downloaded videos
    """
    st.info("Extracting videos from playlist...")
    video_urls = youtube_service.get_playlist_videos(playlist_url)

    if not video_urls:
        st.error("Failed to extract videos from playlist")
        return

    st.info(f"Found {len(video_urls)} videos in playlist")

    for i, video_url in enumerate(video_urls):
        st.subheader(f"Video {i + 1}/{len(video_urls)}")

        video_id = youtube_service.get_video_id(video_url)
        if not video_id:
            st.warning(f"Failed to extract video ID from: {video_url}")
            continue

        _process_single_video(
            video_url, video_id, frame_skip, similarity_threshold, keep_video
        )

    st.success("✅ Playlist processing completed!")
