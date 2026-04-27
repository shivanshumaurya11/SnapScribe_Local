"""
Video to Visual Summaries page.

Handles:
- Local video file upload
- Frame extraction from uploaded videos
- PDF generation from extracted frames
"""

import logging
import os
import tempfile
import streamlit as st

from backend.services.video_service import video_service
from backend.services.pdf_service import pdf_service
from config.settings import settings

logger = logging.getLogger(__name__)


def render() -> None:
    """
    Render video upload and processing page.
    
    Allows users to:
    - Upload video files
    - Configure frame extraction parameters
    - Extract frames and create PDF
    - Download generated PDF
    """
    st.set_page_config(
        page_title="Local Video Processor | SnapScribe",
        page_icon="🎬",
        layout="centered",
    )

    st.title("🎬 Local Video Processor: Generate PDF from Video Frames")

    uploaded_file = st.file_uploader(
        "Upload a video file", type=["mp4", "mov", "avi", "mkv"]
    )

    frame_skip = int(
        st.number_input(
            "Frame Skip Value (Higher value means faster processing but may miss some frames):",
            value=200,
            min_value=1,
        )
    )

    similarity_threshold = float(
        st.number_input(
            "Similarity Threshold (0.0 to 1.0, lower means more frames):",
            value=0.9,
            min_value=0.0,
            max_value=1.0,
            step=0.1,
        )
    )

    if st.button("Process Video") and uploaded_file is not None:
        # Create temp file for upload
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=os.path.splitext(uploaded_file.name)[1]
        ) as temp_video_file:
            temp_video_file.write(uploaded_file.read())
            temp_video_file_path = temp_video_file.name

        try:
            st.video(temp_video_file_path)

            with tempfile.TemporaryDirectory() as temp_folder:
                st.info("Extracting frames from video...")
                frames = video_service.extract_unique_frames(
                    temp_video_file_path, temp_folder, frame_skip, similarity_threshold
                )

                if frames:
                    output_pdf_path = os.path.join(
                        settings.OUTPUT_PDFS_DIR,
                        os.path.splitext(uploaded_file.name)[0] + ".pdf",
                    )

                    st.info(f"Creating PDF with {len(frames)} frames...")
                    success = pdf_service.frames_to_pdf(output_pdf_path, frames)

                    if success:
                        st.success(f"✅ PDF created successfully!")
                        st.write(f"Extracted {len(frames)} frames into PDF")

                        with open(output_pdf_path, "rb") as pdf_file:
                            st.download_button(
                                label="⬇️ Download Generated PDF",
                                data=pdf_file.read(),
                                file_name=os.path.basename(output_pdf_path),
                                mime="application/pdf",
                            )
                        st.balloons()
                    else:
                        st.error("Failed to create PDF from frames")
                else:
                    st.error("No frames were extracted from the video")

        except Exception as e:
            logger.error(f"Error processing video: {e}", exc_info=True)
            st.error(f"Error processing video: {e}")

        finally:
            # Clean up temp file
            try:
                if os.path.exists(temp_video_file_path):
                    os.remove(temp_video_file_path)
            except Exception as e:
                logger.warning(f"Failed to clean up temp file: {e}")

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
