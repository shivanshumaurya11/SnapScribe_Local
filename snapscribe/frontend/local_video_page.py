"""
Local Video Processing page.

Handles:
- Processing local video files from file path
- Frame extraction
- PDF generation
"""

import logging
import os
import tempfile
import streamlit as st

from backend.services.video_service import video_service
from backend.services.pdf_service import pdf_service
from config.settings import settings
from backend.utils.validators import validate_file_path

logger = logging.getLogger(__name__)


def render() -> None:
    """
    Render local video processing page.
    
    Allows users to:
    - Input path to local video file
    - Configure extraction parameters
    - Extract frames and create PDF
    - Download generated PDF
    """
    st.set_page_config(
        page_title="Offline Video Processor", page_icon="🎩✨"
    )

    st.title("🎩 Offline Video Processor: Generate PDF from Video Frames")
    st.write(
        "Note: Provide the complete path to your video file for fast local processing."
    )

    file_path = st.text_input("Enter the complete file path to the video file")

    col1, col2 = st.columns(2)

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
                "Similarity Threshold (0.0 to 1.0):",
                min_value=0.0,
                max_value=1.0,
                value=1.0,
                step=0.1,
                help="0=similar frames, 1=unique frames",
            )
        )

    # Check if the file exists
    if st.button("Process Video"):
        if not file_path:
            st.error("Please enter a file path")
            return

        if not validate_file_path(file_path):
            st.error("Invalid file path")
            return

        if not os.path.isfile(file_path):
            st.error(f"File not found: {file_path}")
            return

        with st.spinner("Processing video..."):
            try:
                st.video(file_path)
                st.info(f"Processing video: {file_path}")

                with tempfile.TemporaryDirectory() as temp_folder:
                    frames = video_service.extract_unique_frames(
                        file_path, temp_folder, frame_skip, similarity_threshold
                    )

                    if frames:
                        st.success(f"Extracted {len(frames)} unique frames")

                        # Create output filename from input path
                        base_name = os.path.splitext(os.path.basename(file_path))[0]
                        output_pdf_name = f"{base_name}.pdf"
                        output_pdf_path = os.path.join(
                            settings.OUTPUT_PDFS_DIR, output_pdf_name
                        )

                        st.info("Creating PDF from frames...")
                        success = pdf_service.frames_to_pdf(
                            output_pdf_path, frames, base_name
                        )

                        if success:
                            st.success(
                                f"✅ Extracted frames have been saved to {output_pdf_path}"
                            )

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
                        st.error("No frames extracted from video")

            except Exception as e:
                logger.error(f"Error processing video: {e}", exc_info=True)
                st.error(f"Error processing video: {e}")

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
